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
from flask_socketio import SocketIO
import os

app = Flask(__name__)

socketio = SocketIO(app)

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
        "N1": {"N12": 0.29, "N10": 0.92},
        "N2": {"N15": 0.31, "N4": 0.95, "N9": 0.76},
        "N3": {"N15": 0.66, "N4": 0.63, "N7": 0.88},
        "N4": {"N2": 0.95, "N3": 0.63, "N12": 0.24, "N14": 0.69},
        "N5": {"N12": 0.14, "N6": 0.89, "N14": 0.95},
        "N6": {"N5": 0.89},
        "N7": {"N3": 0.88, "N15": 0.84},
        "N8": {"N14": 0.77, "N15": 0.43},
        "N9": {"N2": 0.76, "N13": 0.48, "N12": 0.87},
        "N10": {"N1": 0.92},
        "N11": {"N12": 0.79, "N14": 0.83},
        "N12": {"N1": 0.29, "N4": 0.24, "N5": 0.14, "N9": 0.87, "N11": 0.79},
        "N13": {"N9": 0.48, "N15": 0.51},
        "N14": {"N4": 0.69, "N5": 0.95, "N8": 0.77, "N11": 0.83},
        "N15": {"N2": 0.31, "N3": 0.66, "N7": 0.84, "N8": 0.43, "N13": 0.51}
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
        print({'nodes': nodes, 'edges': edges})
    return {}


## graph websocket
@socketio.on('request_graph')
def graph_socket(ws):
    while not ws.closed:
        # Wait for a message from the client
        message = ws.receive()
        if message:
            # Parse the message to get the graph_id
            data = json.loads(message)
            graph_id = data.get('graph_id')
            selected_graph = graph.get(graph_id)
            
            if not selected_graph:
                ws.send(json.dumps({"error": "Graph not found"}))
            else:
                nodes = [{'id': key, 'label': key} for key in selected_graph.keys()]
                edges = [{'from': from_node, 'to': to_node, 'label': str(weight)}
                         for from_node, connections in selected_graph.items()
                         for to_node, weight in connections.items()]
                
                # Send the graph data back to the client
                ws.send(json.dumps({
                    "nodes": nodes,
                    "edges": edges,
                }))
                

## graph http request
# @app.route('/graph', methods=['GET'])
# def get_graph():
#     data = request.get_json()
#     graph_id = data['graph_id']
#     selected_graph = graph.get(graph_id)
#     if not selected_graph:
#         return jsonify({"error": "Graph not found"}), 404

#     nodes = [{'id': key, 'label': key} for key in selected_graph.keys()]
#     edges = [{'from': from_node, 'to': to_node, 'label': str(weight)}
#              for from_node, connections in selected_graph.items()
#              for to_node, weight in connections.items()]
#     print("Nodes: ", nodes, "Edges: ", edges)
#     return jsonify({
#         "nodes": nodes,
#         "edges": edges,
#         })



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



# ## This function is used for test FE.
# # Sample Flask route to initiate the simulation
# @app.route('/simulate_flow', methods=['POST'])
# def simulate_flow():
#     start_text = request.form['start_text']
#     current_node = request.form['current_node']
#     graph_id = request.form.get('network-radio')

#     if graph_id in graph:
#         GenerateText.simulate_message_flow(graph, api_url, start_text, current_node, graph_id)
#         return jsonify({"message": "Simulation started"}), 200
#     else:
#         return jsonify({"error": "Invalid graph ID"}), 400


# Sample Flask route to initiate the simulation
@app.route('/simulate_flow', methods=['POST'])
def simulate_flow():
    data = request.get_json()
    start_text = data.get('start_text')  # The initial message text
    current_node = data.get('current_node')  # The starting node for the simulation
    graph_id = data.get('id')  # The ID of the graph to be used
    
    # nodes, edges = construct_graph_update(graph)
    # send_update_to_frontend('init', nodes, edges)
    
    if graph_id in graph:
        GenerateText.simulate_message_flow(graph, api_url, start_text, current_node, graph_id)
        return jsonify({"message": "Simulation started"}), 200
    else:
        return jsonify({"error": "Invalid graph ID"}), 400

    print(f"start_text: {start_text}")
    print(f"current_node: {current_node}")
    print(f"graph_id: {graph_id}")

    if graph_id in graph:
        GenerateText.simulate_message_flow(graph, api_url, start_text, current_node, graph_id)
        return jsonify({"message": "Simulation started"}), 200
    else:
        return jsonify({"error": "Invalid graph ID"}), 400


if __name__ == '__main__':

    app.run(debug=True)
    