import random
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
import openai
import configparser
from embedding_utils import Text2Vector
from graph_data import graph
import requests
from generates_methods import GenerateText


app = Flask(__name__)


graph = {
    'N1': {'N2': 0.7, 'N4': 0.6},
    'N2': {'N1': 0.7, 'N3': 0.3, 'U': 0.9},
    'N3': {'N2': 0.3, 'N4': 0.6, 'B': 0.3},
    'N4': {'N1': 0.6, 'N3': 0.6, 'U': 0.5, 'B': 0.6},
    'B': {'N3': 0.3, 'N4': 0.6, 'A': 0.2},
    'U': {'N2': 0.9, 'N4': 0.5},
    'A': {'B': 0.2}
}

api_url = "http://127.0.0.1:5000"

# Connect to local Elasticsearch instance
es = Elasticsearch("http://localhost:9200")

# Check if Elasticsearch is running
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Could not connect to Elasticsearch")

# Read API key from config
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['openai']['api_key']
# Set the OpenAI API key
openai.api_key = api_key


# Give prompts and generate the text from LLM
@app.route('/generate_text', methods=['POST'])
def generate_text():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "Prompt is required"}), 400

    prompt = data['prompt']

    try:
        # Generate text using the OpenAI ChatCompletion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract the generated text and remove newlines and extra white spaces
        generated_text = response.choices[0].message.content.strip().replace("\n\n", " ").replace("\n", " ")
    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

    # # Debug: Print the generated text
    # print("Generated text:", generated_text)
    
    return jsonify({
        "prompt": prompt,
        "generated_text": generated_text,
    })

@app.route('/get_record/<index_name>/<document_id>', methods=['GET'])
def get_record(index_name, document_id):
    try:
        response = es.get(index=index_name, id=document_id)
        return jsonify(response['_source']), 200
    except NotFoundError:
        return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Add received records to elasticsearch
@app.route('/add_received_record', methods=['POST'])
def add_received_record():
    data = request.get_json()
    index_name = data.get('index')
    document_body = data.get('body')

    # Generate text vector
    received_text = document_body.get('received_text')
    if received_text:
        document_body['received_text_vector'] = Text2Vector.get_embedding(received_text)

    # Index in Elasticsearch
    response = es.index(index=index_name, document=document_body)
    return jsonify(response)


# Add sent records to elasticsearch
@app.route('/add_sent_record', methods=['POST'])
def add_sent_record():
    data = request.get_json()
    index_name = data.get('index')
    document_body = data.get('body')

    # Generate text vector
    sent_text = document_body.get('sent_text')
    if sent_text:
        document_body['sent_text_vector'] = Text2Vector.get_embedding(sent_text)

    # Index in Elasticsearch
    response = es.index(index=index_name, document=document_body)
    return jsonify(response)


# add received and sent records to elasticsearch
def add_record_to_elasticsearch(node, connected_node, api_url, text, weight, is_received):
    # Define the API endpoint
    endpoint = '/add_received_record' if is_received else '/add_sent_record'
    url = api_url + endpoint

    # Prepare the document body
    document_body = {
        "node": connected_node if is_received else node,
        "from": node if is_received else None,
        "to": connected_node if not is_received else None,
        "received_text": text if is_received else None,
        "sent_text": text if not is_received else None,
        "received_text_weight": str(weight) if is_received else None,
    }

    # Remove None fields
    document_body = {k: v for k, v in document_body.items() if v is not None}

    # Set the correct index name
    index_name = "received_text_test01" if is_received else "sent_text_test01"

    # Prepare request data
    request_data = {
        "index": index_name,
        "file_name": "_doc",
        "body": document_body
    }

    # Make the POST request to the API
    response = requests.post(url, json=request_data)

    # print(f"Sent from Node: {node} to Node: {connected_node}")
    # print(f"Received at Node: {connected_node} from Node: {node}, Weight: {weight}")
    print(f"{'Received' if is_received else 'Sent'}: {document_body}")
    print(response.json())  # Print the response from the API call
    return response


def simulate_message_flow(graph, api_url, start_text, current_node):
    visited_nodes = set()
    skip_next_round = set()
    senders = set()
    receivers = set()

    print("Start simulation")
    text_to_send = start_text

    queue = [(start_text, current_node)]

    while queue:
        text, current_node = queue.pop(0)
        visited_nodes.add(current_node)

        if current_node in skip_next_round:
            skip_next_round.remove(current_node)
            continue

        text_to_send = GenerateText.get_generated_text(api_url, text_to_send)
        if not text_to_send:
            print("Text generation failed, ending simulation.")
            break

        for neighbour, weight in graph[current_node].items():
            if neighbour not in visited_nodes:
                queue.append((text_to_send, neighbour))
                # Add sent record
                senders.add(current_node)
                add_record_to_elasticsearch(current_node, neighbour, api_url, text, weight, is_received=False)
                print("Sent from Node:", current_node, "to Node:", neighbour)

            
                # Add received record
                receivers.add(neighbour)
                add_record_to_elasticsearch(current_node, neighbour, api_url, text, weight, is_received=True)
                print("Received at Node:", neighbour, "from Node:", current_node, "Weight:", weight)

                # If the weight is less than or equal to 0.3, mark the neighbour to skip the next round as a sender
                if weight <= 0.3:
                    skip_next_round.add(neighbour)

                # Continue the simulation with the neighbour as the current node
                queue.append((text, neighbour))

    # Nodes that have never sent any messages
    never_senders = graph.keys() - senders
    # Nodes that have never received any messages
    never_receivers = graph.keys() - receivers

    print("End simulation")
    print("Nodes that never sent any messages:", never_senders)
    print("Nodes that never received any messages:", never_receivers)

    return list(never_senders), list(never_receivers)

# Sample Flask route to initiate the simulation
@app.route('/simulate_flow', methods=['POST'])
def simulate_flow():
    data = request.get_json()
    start_text = data['start_text']  # The initial message text
    current_node = data['current_node']  # The starting node for the simulation

    simulate_message_flow(graph, api_url, start_text, current_node)
    return jsonify({"message": "Simulation started"}), 200



if __name__ == '__main__':
    app.run(debug=True)
    