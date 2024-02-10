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
    socketio.emit("response", prepare_graph_for_frontend('graph'))


@socketio.on('connect')
def connect():
    print("connect..")


# if __name__ == '__main__':
#     socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

def main():
    # start_text = ("The Harbour Bridge expansion aims to alleviate congestion, \
    # boost the economy, enhance safety, and promote sustainability, despite short-term disruptions and financial concerns. \
    # We seek community feedback on navigating these challenges and capitalizing on the project's long-term benefits to improve commutes, environmental quality, and urban development.\
    #  There are some Short-term Traffic Disruptions: The construction phase will inevitably impact daily commutes. Strategies such as alternative routes, enhanced public transportation options, \
    #  and clear communication about construction schedules can help mitigate these effects. And require the significant investment required for the expansion raises questions about budget allocation and potential impacts on other public services. How do you think about this idea? Could you provide some suggestions? Or do you have some question for it?")

    # start_text = ("I stand at the threshold of a fantastic journey - next week marks my job interview for a coveted Data Scientist role, and I'm buzzing with a mix of excitement and nerves.In the spirit of collaboration and knowledge-sharing that defines this community, \
    # I'm reaching out to gather pearls of wisdom that might help me ace this challenge. Whether it's the hard-hitting technical questions, the probing inquiries into industry trends, or the enigmatic behavioral puzzles, I'm all ears for your advice.\
    #               Here's what I'm pondering over: Technical Proficiency: What are the most critical technical skills I should be polishing? I’m brushing up on my Python, R, and SQL, and diving deep into machine learning algorithms. But is there anything else that's crucial?\
    #               Data Wrangling and Visualization: It goes without saying that data cleaning is a huge part of the job, but what are some examples of data wrangling challenges you've faced? Also, what visualization tools have made your presentations stand out?\
    #               Statistical Savvy: I anticipate statistical questions will be a central part of the interview. Any tips on key concepts or common statistical traps to watch out for?\
    #               Machine Learning Mastery: From your experience, which machine learning topics are interviewers most interested in? Are there any projects or applications I should definitely be familiar with?\
    #               Behavioral Balance: How do you blend the narrative of your technical expertise with the soft skills that show you’re a team player?\
    #               Industry Insight: Given the vast applications of data science across sectors, are there any industry-specific trends or news I should be clued up on?\
    #               Portfolio Power: I’ve got my portfolio ready to showcase my projects, but I’m curious - what kinds of projects have really impressed your interviewers?\
    #               The Unexpected: Finally, have there been any out-of-left-field questions or tasks in your interviews that took you by surprise?\
    #               I’m compiling all the advice I can get, and I’d be incredibly grateful for any stories, suggestions, or insights you can share. Your input could be the secret sauce to my success!\
    #               Let's connect the dots and chart the course to a triumphant interview! ")

    start_text = ("We at Tech Innovations Inc. are thrilled to announce the upcoming launch of our latest breakthrough - SmartGadget Pro! \
    As we gear up to bring this cutting-edge device to the market, we believe that your insights and opinions are invaluable. SmartGadget Pro isn't just another gadget; \
    it’s the next step in smart technology evolution, designed to seamlessly integrate into your daily life, making it more efficient and connected than ever before. \
    Before we make the big leap, we're turning to you - our potential customers and the greatest tech enthusiasts out there - to help us refine and perfect what we've built. \
    Here’s how you can contribute: 1.	First Impressions: What are your initial thoughts on SmartGadget Pro? Share your raw, unfiltered first impressions. 2.	Features Frenzy: From its sleek design to its AI-driven capabilities - which features excite you the most? \
    Which features do you think could be enhanced? 3.	Use-Case Curiosity: We all love gadgets that make life easier. How do you envision using SmartGadget Pro in your daily routine? 4.	Performance Parameters: For the tech-savvy - \
    what performance metrics would you focus on when assessing SmartGadget Pro? 5.	Design Dialogue: Aesthetics meet function - what does your ideal smart gadget look like and how does SmartGadget Pro compare? 6.	Price Point Perspective: Value for money is key.\
     What would be an acceptable price range for a gadget with these features? 7.	The ‘Wow’ Factor: Every product has something that makes it stand out. What ‘wow’ factor would you want in SmartGadget Pro? \
     8.	Constructive Critiques: We're not just here for the praises - constructive criticism is what drives progress. If you could change one thing about SmartGadget Pro, what would it be? \
     9.	Marketing Messages: If you're as excited as we are, what kind of messaging do you think would best resonate with people like you in our marketing campaigns? \
     10.	The Big Question: Would you recommend SmartGadget Pro to your friends and family? Why or why not? Let’s make SmartGadget Pro not just a product but a game-changer. Use the hashtag #SmartGadgetProFeedback to share your thoughts, and let's innovate together! \
     Your feedback is more than just appreciated – it's essential. Ready to revolutionize the tech world? Let's do this! 💡📱")

    current_node = "N1"
    graph_id = "graph-1"

    GenerateText.simulate_message_flow(graph, start_text, current_node, graph_id, socketio)


if __name__ == '__main__':
    main()