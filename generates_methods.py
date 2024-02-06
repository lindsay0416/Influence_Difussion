
import requests
from flask import Flask, request, jsonify, render_template
import os
import openai
import configparser
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from embedding_utils import Text2Vector



# Read API key from config
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['openai']['api_key']
# Set the OpenAI API key
openai.api_key = api_key

# print(api_key)

# Connect to local Elasticsearch instance
es = Elasticsearch("http://localhost:9200")

# Check if Elasticsearch is running
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Could not connect to Elasticsearch")

class GenerateText:
    # @staticmethod
    # def es_client():
    #     # Check if Elasticsearch is running
    #     es = Elasticsearch("http://localhost:9200")

    #     if es.ping():
    #         print("Connected to Elasticsearch")
    #     else:
    #         print("Could not connect to Elasticsearch")
    #     # Assuming you have a method or a property to get the Elasticsearch client
    #     # This is a placeholder. You need to replace it with actual code to get your Elasticsearch client instance.
    #     return es

    # Function to post data to the /generate_text API and receive the generated text
    @staticmethod
    def get_generated_text(prompt):
        generated_text = ""
        # prompt = data['prompt']
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
        except Exception as e:
            print(f"An error occurred: {e}")

        return generated_text, prompt
        

    @staticmethod
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

    @staticmethod
    def simulate_message_flow(graphs, start_text, current_node, graph_id, socketio):
        if graph_id not in graphs:
            print(f"Graph ID {graph_id} not found.")
            return

        current_graph = graphs[graph_id]
        visited_nodes = set()
        skip_next_round = set()
        senders = set()
        receivers = set()

        print("Start simulation")
        text_to_send = start_text

        queue = [(start_text, current_node)]

        while queue:
            text, current_node = queue.pop(0)

            if current_node not in current_graph:
                print(f"Node {current_node} not found in graph {graph_id}.")
                continue

            visited_nodes.add(current_node)

            if current_node in skip_next_round:
                skip_next_round.remove(current_node)
                continue

            # Read user profile text from the corresponding file
            user_profile_filename = f"user_profile/{current_node}.txt"
            with open(user_profile_filename, "r") as user_profile_file:
                user_profile_text = user_profile_file.read()
            
            # Include user profile text in the prompt
            prompt = f"According to the personality {user_profile_text}, \
                    how will {current_node} reply to the latest received text: {text}. \
                    please generate a possible response with 20 words."
            print("Prompt: ", prompt) 

            # Generate text using the OpenAI ChatCompletion endpoint
            text_to_send, given_text = GenerateText.get_generated_text(prompt)
            print("text_to_send", text_to_send)
            if not text_to_send:
                print("Text generation failed, ending simulation.")
                break
            # response = requests.post(f"{api_url}/generate_text", json={'prompt': prompt}, timeout=(5,10))
            # print("response", response)
            # text_to_send = "Debug test text to send."
            # print("text_to_send", text_to_send)

            for neighbour, weight in current_graph[current_node].items():
                print("***********", neighbour, weight)
                if neighbour not in visited_nodes:
                    # socketio.emit("light_node", {'nid': neighbour})
                    print("visited Node: ", visited_nodes)
                    print("neighbour: ", neighbour)
                    queue.append((text_to_send, neighbour))
                    # Add sent record
                    senders.add(current_node)
                    GenerateText.add_record_to_elasticsearch(current_node, neighbour, text_to_send, weight, is_received=False)
                    print("Sent from Node:", current_node, "to Node:", neighbour)

                     # Store sent message in the node's corresponding text file
                    sent_message =  f"sent:{text_to_send}"
                    node_file_path = os.path.join("user_profile", f"{current_node}.txt")
                    with open(node_file_path, "a") as node_file:
                        node_file.write(sent_message + "\n")
                
                    # Add received record
                    receivers.add(neighbour)
                    GenerateText.add_record_to_elasticsearch(current_node, neighbour, text_to_send, weight, is_received=True)
                    print("Received at Node:", neighbour, "from Node:", current_node, "Weight:", weight)
                    print(receivers.add(neighbour), neighbour)
                    socketio.emit("light_node", {'nid': neighbour})

                    # Store received message in the node's corresponding text file
                    received_message = f"received:{text_to_send}"
                    node_file_path = os.path.join("user_profile", f"{neighbour}.txt")
                    with open(node_file_path, "a") as node_file:
                        node_file.write(received_message + "\n")

                    if weight <= 0.3:
                        skip_next_round.add(neighbour)

        # Print nodes that never sent/received messages
        never_senders = set(current_graph.keys()) - senders
        never_receivers = set(current_graph.keys()) - receivers
        print("End simulation")
        print("Nodes that never sent any messages:", never_senders)
        print("Nodes that never received any messages:", never_receivers)
       # Calculate influence coverage
        total_nodes = len(current_graph)
        influence_coverage = (total_nodes-len(never_receivers)) / total_nodes

        # Print influence coverage
        print("Influence coverage:", influence_coverage)

        return list(never_senders), list(never_receivers)

    # Add received records to elasticsearch
    @staticmethod
    def add_received_record(index_name, document_body):
        # es = GenerateText.es_client()  # Get Elasticsearch client
        received_text = document_body.get('received_text')
        if received_text:
            document_body['received_text_vector'] = Text2Vector.get_embedding(received_text)
        response = es.index(index=index_name, document=document_body)
        return response  # Return raw response or process as needed


    @staticmethod
    def add_sent_record(index_name, document_body):
        # es = GenerateText.es_client()  # Get Elasticsearch client
        sent_text = document_body.get('sent_text')
        if sent_text:
            document_body['sent_text_vector'] = Text2Vector.get_embedding(sent_text)
        response = es.index(index=index_name, document=document_body)
        return response  # Return raw response or process as needed

        
    @staticmethod
    def add_record_to_elasticsearch(node, connected_node, text, weight, is_received):
        document_body = {
            "node": connected_node if is_received else node,
            "from": node if is_received else None,
            "to": connected_node if not is_received else None,
            "received_text": text if is_received else None,
            "sent_text": text if not is_received else None,
            "received_text_weight": str(weight) if is_received else None,
        }
        document_body = {k: v for k, v in document_body.items() if v is not None}
        index_name = "received_text_test01" if is_received else "sent_text_test01"

        # Decide whether to add a received or sent record based on is_received flag
        if is_received:
            response = GenerateText.add_received_record(index_name, document_body)
        else:
            response = GenerateText.add_sent_record(index_name, document_body)

        # Print or log the response as needed
        print(f"{'Received' if is_received else 'Sent'}: {document_body}")
        print("Response from Elasticsearch:", response)
        return response  # Return raw response or process as needed
        