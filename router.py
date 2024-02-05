import random, json, time
from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
import openai
import configparser
from embedding_utils import Text2Vector
import requests
from generates_methods import GenerateText
from flask_socketio import SocketIO
from graph_data import graph

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, cors_allowed_origins='*')
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins='*')


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
# api_key = config['openai']['api_key']
# Set the OpenAI API key
openai.api_key = "api_key"

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

@app.route('/simulate_flow', methods=['POST'])
def simulate_flow_backend():
    data = request.get_json()
    start_text = data.get('start_text')  # The initial message text
    current_node = data.get('current_node')  # The starting node for the simulation
    graph_id = data.get('graph_id')  # The ID of the graph to be used
    
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



@socketio.on('simulate')
def simulate_flow(message):
    start_text = message['start_text']
    current_node = message['current_node']
    graph_id = message['current_network']

    print(f"start_text: {start_text}")
    print(f"current_node: {current_node}")
    print(f"graph_id: {graph_id}")

    # TODO: after getting the initial information including a message, starting node, and the network,
    #  call a simulation function passing the initial information to start the simulation at backend.
    #  Each time a node is activated, return the node information to light it up.

    nodes = graph[graph_id].keys()
    for node in nodes:
        time.sleep(1)
        socketio.emit("light_node", {'nid': node})

    socketio.emit("simulate_done", "Done")


@socketio.on('message')
def handle_message(message):
    print(f"Received message: {message}")
    print(f"{message['graph']} is selected.")

    socketio.emit("response", prepare_graph_for_frontend(message['graph']))


@socketio.on('connected')
def handle_message(connected):
    print(f"{connected['data']}")

    # initialize the graph showing the first one in the data
    socketio.emit("response", prepare_graph_for_frontend('graph-1'))


@socketio.on('connect')
def connect():
    print("connect..")


if __name__ == '__main__':

    # app.run(debug=True)
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
    # socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=False, log_output=True)
