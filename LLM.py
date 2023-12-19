from flask import Flask, request, jsonify
from langchain.llms import OpenAI
import configparser

app = Flask(__name__)

# Read API key from config
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['openai']['api_key']

# Initialize OpenAI model with GPT-3.5
gpt = OpenAI(openai_api_key=api_key, model="gpt-3.5-turbo-1106")  # Replace with the correct GPT-3.5 model identifier


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

    return jsonify({"generated_text": generated_text})

if __name__ == '__main__':
    app.run(debug=True)
