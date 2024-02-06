from flask import Flask, request, jsonify
import random, json
from flask import Flask, request, jsonify, render_template

import openai
import configparser

import requests
from generates_methods import GenerateText
from flask_socketio import SocketIO
from graph_data import graph
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')
# socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins='*')


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

@app.route('/')
def index():
    print('Index loaded!')
    return render_template('index.html')


@socketio.on('simulate')
def simulate_flow(message):
    start_text = message['start_text']
    current_node = message['current_node']
    graph_id = message['current_network']

    print(f"start_text: {start_text}")
    print(f"current_node: {current_node}")
    print(f"graph_id: {graph_id}")

    socketio.emit("light_node", {'nid': current_node})

    # TODO: after getting the initial information including a message, starting node, and the network,
    #  call a simulation function passing the initial information to start the simulation at backend.
    #  Each time a node is activated, return the node information to light it up.

    if graph_id in graph:
        GenerateText.simulate_message_flow(graph, start_text, current_node, graph_id, socketio)
        # return jsonify({"message": "Simulation started"}), 200
    else:
        # return jsonify({"error": "Invalid graph ID"}), 400
        pass

    print(f"start_text: {start_text}")
    print(f"current_node: {current_node}")
    print(f"graph_id: {graph_id}")

    

    # nodes = graph[graph_id].keys()
    # for node in nodes:
    #     time.sleep(1)
    #     socketio.emit("light_node", {'nid': node})

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
    # socketio.run(app, debug=True, host='0.0.0.0', port=5555, use_reloader=False, log_output=True)