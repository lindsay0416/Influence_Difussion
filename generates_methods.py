
import requests
import os
# from router import socketio

class GenerateText:
    # Function to post data to the /generate_text API and receive the generated text
    @staticmethod
    def get_generated_text(api_url, prompt):
        response = requests.post(f"{api_url}/generate_text", json={'prompt': prompt})
        return response.json().get('generated_text', 'No generation result found.') if response.ok else None
    

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
    def simulate_message_flow(graphs, api_url, start_text, current_node, graph_id):
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
            text_to_send = GenerateText.get_generated_text(api_url, prompt)
            if not text_to_send:
                print("Text generation failed, ending simulation.")
                break
            # text_to_send = "Debug test text to send."
            # print("text_to_send", text_to_send)

            for neighbour, weight in current_graph[current_node].items():
                if neighbour not in visited_nodes:
                    queue.append((text_to_send, neighbour))
                    # Add sent record
                    senders.add(current_node)
                    GenerateText.add_record_to_elasticsearch(current_node, neighbour, api_url, text_to_send, weight, is_received=False)
                    print("Sent from Node:", current_node, "to Node:", neighbour)

                     # Store sent message in the node's corresponding text file
                    sent_message =  f"sent:{text_to_send}"
                    node_file_path = os.path.join("user_profile", f"{current_node}.txt")
                    with open(node_file_path, "a") as node_file:
                        node_file.write(sent_message + "\n")
                
                    # Add received record
                    receivers.add(neighbour)
                    GenerateText.add_record_to_elasticsearch(current_node, neighbour, api_url, text_to_send, weight, is_received=True)
                    print("Received at Node:", neighbour, "from Node:", current_node, "Weight:", weight)
                    # socketio.emit("light_node", {'nid': neighbour})

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

    @staticmethod
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
        