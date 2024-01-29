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


# # Python Function to Send Request:
# def add_record_to_elasticsearch(api_url, index_name, text, is_received=True):
#     endpoint = '/add_received_record' if is_received else '/add_sent_record'
#     url = api_url + endpoint

#     node = f"N{random.randint(1, 10)}"
#     weight = random.uniform(0, 1) if is_received else None

#     document_body = {
#         "node": node,
#         "from": f"N{random.randint(1, 10)}",
#         "received_text": text if is_received else None,
#         "received_text_weight": str(weight) if is_received else None,
#         "sent_text": None if is_received else text
#     }

#     document_body = {k: v for k, v in document_body.items() if v is not None}
#     request_data = {"index": index_name, "file_name": "_doc", "body": document_body}

#     response = requests.post(url, json=request_data)
#     return response


def add_record_to_elasticsearch(node, api_url, index_name, text, graph, is_received=True):
    # Choose a random node from the graph
    # node = random.choice(list(graph.keys()))

    # Choose a connected node and the corresponding weight
    connected_node, weight = random.choice(list(graph[node].items()))

    # Define the API endpoint
    endpoint = '/add_received_record' if is_received else '/add_sent_record'
    url = api_url + endpoint

    # Prepare the document body
    if is_received:
        document_body = {
            "node": connected_node,
            "from": node,
            "received_text": text,
            "received_text_weight": str(weight),
        }
    else:
        document_body = {
            "node": node,
            "to": connected_node,
            "sent_text": text,
        }

    index_name = "received_text_test01" if is_received else "sent_text_test01"
   # Prepare the request data
    request_data = {
        "index": index_name,
        "file_name": "_doc",
        "body": document_body
    }

    # Make the POST request to the API
    response = requests.post(url, json=request_data)

    # Print the entire response
    print("Response from Elasticsearch:")
    print(response.json())

    return response


def simulate_message_flow(graph, api_url, start_text, current_node):
    print("Start simulation")

    visited_nodes = set()
    queue = [(start_text, current_node)]

    while queue:
        text, current_node = queue.pop(0)
        visited_nodes.add(current_node)

        for neighbour, weight in graph[current_node].items():
            if neighbour not in visited_nodes:     
                # Add sent record
                add_record_to_elasticsearch(current_node, api_url, "sent_text_test01", text, graph, is_received=False)
                print("Sent", f"Node: {current_node}, To: {neighbour}")

                  # Add received record
                add_record_to_elasticsearch(current_node, api_url, "received_text_test01", text, graph, is_received=True)
                print("Received: ", f"Node: {neighbour}, From: {current_node}, Weight: {weight}")
                queue.append((text, neighbour))
    print("End simulation")


@app.route('/simulate_flow', methods=['POST'])
def simulate_flow():
    data = request.get_json()
    start_text = data.get('start_text') # this is the node initial text
    current_node = data.get('current_node') # this is the first start node 

    # Call the simulate message flow function
    simulate_message_flow(graph, api_url, start_text, current_node)
    return jsonify({"message": "Simulation started"}), 200



 

# # Add received records 
# @app.route('/add_received_record', methods=['POST'])
# def add_received_record():
#     index_name = request.json.get('index')
#     file_name = request.json.get('file_name') 
#     # document_id = request.json.get('id') 
#     document_body = request.json.get('body')

#     # Get the next ID
#     document_id = get_next_id(index_name)

#     if not document_id or not document_body or not file_name or not index_name:
#         return jsonify({"error": "Document ID and body are required"}), 400

#     # Ensure 'body' contains the required sub-fields
#     if not all(k in document_body for k in ['node', 'received_text_weight', 'from', 'received_text', 'received_text_vector']):
#         return jsonify({"error": "Incomplete body data"}), 400
    
#     try:
#         response = es.index(index=index_name, id=document_id, document=document_body)
#         return jsonify(response), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # Add sent records 
# @app.route('/add_sent_record', methods=['POST'])
# def add_sent_record():
#     index_name = request.json.get('index')
#     file_name = request.json.get('file_name') 
#     # document_id = request.json.get('id')
#     document_body = request.json.get('body')

#     # Get the next ID
#     document_id = get_next_id(index_name)

#     if not document_id or not document_body or not file_name or not index_name:
#         return jsonify({"error": "Document ID and body are required"}), 400

#     # Ensure 'body' contains the required sub-fields
#     if not all(k in document_body for k in ['node', 'to', 'sent_text', 'sent_text_vector']):
#         return jsonify({"error": "Incomplete body data"}), 400
    
#     try:
#         response = es.index(index=index_name, id=document_id, document=document_body)
#         return jsonify(response), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


## Sample usage for add_record_to_elasticsearch
# api_url = "http://localhost:5000"
# index_name = "received_text_test01"
# text = "Sample text for testing"
# response = add_record_to_elasticsearch(api_url, index_name, text, is_received=True)
# print(response.json())



# Example usage
# api_url = "http://localhost:5000"
# index_name = "sent_text_test01"
# text = "Sample text for testing sent record"
# response = add_sent_record_to_elasticsearch(api_url, index_name, text)
# print(response.json())


if __name__ == '__main__':
    app.run(debug=True)
    