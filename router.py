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




# Sample Flask route to initiate the simulation
@app.route('/simulate_flow', methods=['POST'])
def simulate_flow():
    data = request.get_json()
    start_text = data['start_text']  # The initial message text
    current_node = data['current_node']  # The starting node for the simulation

    GenerateText.simulate_message_flow(graph, api_url, start_text, current_node)
    return jsonify({"message": "Simulation started"}), 200



if __name__ == '__main__':
    app.run(debug=True)
    