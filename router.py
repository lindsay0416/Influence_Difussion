import random
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from langchain.llms import OpenAI
import configparser
from embedding_utils import Text2Vector
from graph_data import graph
import requests
from collections import deque


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

# Check the id of a document in each index.
# Make the id a unique number in Elasticsearch
def get_next_id(index_name):
    # Document ID for the counter
    counter_id = 'counter'

    # Try to get the current counter value
    try:
        current_counter = es.get(index=index_name, id=counter_id)['_source']
        next_id = current_counter['last_id'] + 1
    except NotFoundError:
        # If not found, start from 1
        next_id = 1

    # Update the counter
    es.index(index=index_name, id=counter_id, document={'last_id': next_id})

    return next_id

# Read API key from config
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['openai']['api_key']

# Initialize OpenAI model with GPT-3.5
# gpt = OpenAI(openai_api_key=api_key, model="gpt-3.5-turbo-1106")
gpt = OpenAI(openai_api_key=api_key)

# Give prompts and generate the text from LLM
@app.route('/generate_text', methods=['POST'])
def generate_text():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "Prompt is required"}), 400

    prompt = data['prompt']
    prompt_list = [prompt]

    # Generate text using the list of prompts
    generated_text_result = gpt.generate(prompt_list)
    # Debug: Print the LLMResult object
    print("LLMResult object:", generated_text_result)
    print("Type of LLMResult:", type(generated_text_result))

    # Inspect the attributes of the LLMResult object
    print("LLMResult attributes:", dir(generated_text_result))

    # Extract the generated text and remove leading newlines
    if generated_text_result and generated_text_result.generations:
        generated_text = generated_text_result.generations[0][0].text.strip()
    else:
        generated_text = "No generation result found."
    
    # Randomly select a node from the graph
    random_node = random.choice(list(graph.keys()))

    return jsonify({
        "prompt": prompt,
        "prompt_vector": Text2Vector.get_embedding(prompt),
        "generated_text": generated_text,
        "generated_text_vector": Text2Vector.get_embedding(generated_text),
        "Node": random_node # Randomly choose a node to receive the text.
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
    print("Start simulation")

    visited_nodes = set()
    skip_next_round = set()
    senders = set()
    receivers = set()

    queue = [(start_text, current_node)]

    while queue:
        text, current_node = queue.pop(0)
        visited_nodes.add(current_node)

        if current_node in skip_next_round:
            skip_next_round.remove(current_node)
            continue

        for neighbour, weight in graph[current_node].items():
            if neighbour not in visited_nodes:
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

# def simulate_message_flow(graph, api_url, start_text, current_node):
#     print("Start simulation")
#     visited_nodes = set()
#     queue = [(start_text, current_node)]

#     while queue:
#         text, node = queue.pop(0)
#         if node not in visited_nodes:
#             visited_nodes.add(node)
#             for connected_node, weight in graph[node].items():
#                 # Add sent record
#                 add_record_to_elasticsearch(node, connected_node, api_url, text, weight, is_received=False)

#                 # Add received record
#                 add_record_to_elasticsearch(node, connected_node, api_url, text, weight, is_received=True)

#                 if connected_node not in visited_nodes:
#                     queue.append((text, connected_node))

#     print("End simulation")

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
    