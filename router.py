from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from langchain.llms import OpenAI
import configparser
from embedding_utils import Text2Vector


app = Flask(__name__)


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


# Add received records 
@app.route('/add_received_record', methods=['POST'])
def add_received_record():
    index_name = request.json.get('index')
    file_name = request.json.get('file_name') 
    # document_id = request.json.get('id') 
    document_body = request.json.get('body')

    # Get the next ID
    document_id = get_next_id(index_name)

    if not document_id or not document_body or not file_name or not index_name:
        return jsonify({"error": "Document ID and body are required"}), 400

    # Ensure 'body' contains the required sub-fields
    if not all(k in document_body for k in ['node', 'received_text_weight', 'from', 'received_text', 'received_text_vector']):
        return jsonify({"error": "Incomplete body data"}), 400
    
    try:
        response = es.index(index=index_name, id=document_id, document=document_body)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Add sent records 
@app.route('/add_sent_record', methods=['POST'])
def add_sent_record():
    index_name = request.json.get('index')
    file_name = request.json.get('file_name') 
    # document_id = request.json.get('id')
    document_body = request.json.get('body')

    # Get the next ID
    document_id = get_next_id(index_name)

    if not document_id or not document_body or not file_name or not index_name:
        return jsonify({"error": "Document ID and body are required"}), 400

    # Ensure 'body' contains the required sub-fields
    if not all(k in document_body for k in ['node', 'to', 'sent_text', 'sent_text_vector']):
        return jsonify({"error": "Incomplete body data"}), 400
    
    try:
        response = es.index(index=index_name, id=document_id, document=document_body)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Read API key from config
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['openai']['api_key']

# Initialize OpenAI model
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

    return jsonify({
        "prompt": prompt,
        "prompt_vector": Text2Vector.get_embedding(prompt),
        "generated_text": generated_text,
        "generated_text_vector": Text2Vector.get_embedding(generated_text)
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


if __name__ == '__main__':
    app.run(debug=True)
    