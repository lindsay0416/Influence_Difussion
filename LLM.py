from flask import Flask, request, jsonify
from langchain.llms import OpenAI
import configparser

app = Flask(__name__)

# Read API key from config
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['openai']['api_key']

# Initialize OpenAI model
gpt = OpenAI(openai_api_key=api_key)

@app.route('/generate_text', methods=['POST'])
def generate_text():
    data = request.get_json()  # Get the JSON data from the request
    if not data or 'prompt' not in data:
        return jsonify({"error": "Prompt is required"}), 400

    prompt = data['prompt']
    # Convert prompt to a list as expected by the generate method
    prompt_list = [prompt]

    # Generate text using the list of prompts
    generated_text = gpt.generate(prompt_list)
    return jsonify({"generated_text": generated_text[0] if generated_text else "No response"})

if __name__ == '__main__':
    app.run(debug=True)
