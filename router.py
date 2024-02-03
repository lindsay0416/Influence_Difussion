from flask import Flask, request, jsonify
import random, json
from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
import openai
import configparser
from embedding_utils import Text2Vector
import requests
from generates_methods import GenerateText
from flask_sockets import Sockets
import os

app = Flask(__name__)
sockets = Sockets(app)

graph = {
    'graph-1':{
        'N1': {'N2': 0.7, 'N4': 0.6},
        'N2': {'N1': 0.7, 'N3': 0.3, 'U': 0.9},
        'N3': {'N2': 0.3, 'N4': 0.6, 'B': 0.3},
        'N4': {'N1': 0.6, 'N3': 0.6, 'U': 0.5, 'B': 0.6},
        'B': {'N3': 0.3, 'N4': 0.6, 'A': 0.2},
        'U': {'N2': 0.9, 'N4': 0.5},
        'A': {'B': 0.2}
        },
    'graph-2':{
        'N1': {'N2': 0.7, 'N4': 0.6},
        'N2': {'N1': 0.7, 'N3': 0.3, 'U': 0.9},
        'N3': {'N2': 0.3, 'N4': 0.6, 'B': 0.3},
        'N4': {'N1': 0.6, 'N3': 0.6, 'U': 0.5, 'B': 0.6},
        'B': {'N3': 0.3, 'N4': 0.6, 'A': 0.2},
        'U': {'N2': 0.9, 'N4': 0.5},
        'A': {'B': 0.2}
        },
     'graph-3':{
        'N1': {'N2': 0.7, 'N4': 0.6},
        'N2': {'N1': 0.7, 'N3': 0.3, 'U': 0.9},
        'N3': {'N2': 0.3, 'N4': 0.6, 'B': 0.3},
        'N4': {'N1': 0.6, 'N3': 0.6, 'U': 0.5, 'B': 0.6},
        'B': {'N3': 0.3, 'N4': 0.6, 'A': 0.2},
        'U': {'N2': 0.9, 'N4': 0.5},
        'A': {'B': 0.2}
        }
    }

# graph  = {
#     'N1': {'N2': 0.7, 'N4': 0.6},
#     'N2': {'N1': 0.7, 'N3': 0.3, 'U': 0.9},
#     'N3': {'N2': 0.3, 'N4': 0.6, 'B': 0.3},
#     'N4': {'N1': 0.6, 'N3': 0.6, 'U': 0.5, 'B': 0.6},
#     'B': {'N3': 0.3, 'N4': 0.6, 'A': 0.2},
#     'U': {'N2': 0.9, 'N4': 0.5},
#     'A': {'B': 0.2}
#     }


# Function to convert graph data to frontend format
def prepare_graph_for_frontend(graph_id):
    # Ensure that we're accessing the correct graph dictionary
    selected_graph = graph.get(graph_id)
    if selected_graph:
        nodes = [{'id': key, 'label': key} for key in selected_graph.keys()]
        edges = [{'from': from_node, 'to': to_node, 'label': str(weight)}
                 for from_node, connections in selected_graph.items()
                 for to_node, weight in connections.items()]
        return {'nodes': nodes, 'edges': edges}
    return {}


@sockets.route('/graph')
def graph_socket(ws):
    while not ws.closed:
        message = ws.receive()
        print(f"websocket received message: {message}")
        if message:
            message_data = json.loads(message)
            graph_id = message_data.get('id')
            if graph_id and graph_id in graph:
                frontend_data = prepare_graph_for_frontend(graph_id)
                ws.send(json.dumps(frontend_data))


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

@app.route('/')
def index():
    print('Index loaded!')
    return render_template('index.html')

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
    # data = request.get_json()
    # # print(f"simulate_flow is called, and the requested data is {data}")
    # start_text = data.get('start_text')  # The initial message text
    # current_node = data.get('current_node')  # The starting node for the simulation
    # graph_id = data.get('graph_id')  # The ID of the graph to be used
    #
    # # nodes, edges = construct_graph_update(graph)
    # # send_update_to_frontend('init', nodes, edges)
    #
    # if graph_id in graph:
    #     GenerateText.simulate_message_flow(graph, api_url, start_text, current_node, graph_id)
    #     return jsonify({"message": "Simulation started"}), 200
    # else:
    #     return jsonify({"error": "Invalid graph ID"}), 400
    start_text = request.form['start_text']
    current_node = request.form['current_node']
    graph_id = request.form.get('network-radio')

    # print(f"start_text: {start_text}")
    # print(f"current_node: {current_node}")
    # print(f"graph_id: {graph_id}")

    if graph_id in graph:
        GenerateText.simulate_message_flow(graph, api_url, start_text, current_node, graph_id)
        return jsonify({"message": "Simulation started"}), 200
    else:
        return jsonify({"error": "Invalid graph ID"}), 400


if __name__ == '__main__':

    app.run(debug=True)
    