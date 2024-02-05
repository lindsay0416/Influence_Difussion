## This is a script of generate user profile.
## To run this file, 1. run "python router.py" 2. run "python generate_user_profile_script.py" 
## The result will store in the folder called "user_profile" 
## # Call the /generate_text route x times and save the generated text to files, change the parameter in this line: for i in range(1, 51)
import os
from flask import Flask, request, jsonify
import configparser
import requests

app = Flask(__name__)

# Ensure the user_profile folder exists
user_profile_folder = "user_profile"
os.makedirs(user_profile_folder, exist_ok=True)

# Define the prompt you want to use for text generation
prompt = "Please Generate one personality for me, the format is as follows: \
        Name, Age, Occupation, Background, Personality Traits, Hobbies and Interests, Communication Style, Goals, Challenges, Ideal Environment. \
        And generate some information the person likes to share on the social media. \
        I will run this promopts for many times, please do not use same name and please choose more different Occupations and backgroud.\
        The age can be between 18 to 65 years old. The personlity and hobbies should be related to their age and bacgroud. \
        Please also genertate few possible message the person likes to share on the social media."

# Function to save generated text to a file
def save_generated_text_to_file(generated_text, filename):
    try:
        file_path = os.path.join(user_profile_folder, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(generated_text)
        return True
    except Exception as e:
        print(f"Error while saving text to file {filename}: {str(e)}")
        return False

# Call the /generate_text route x times and save the generated text to files
for i in range(51, 52): 
    response = requests.post("http://127.0.0.1:5000/generate_text", json={'prompt': prompt})
    
    if response.status_code == 200:
        data = response.json()
        generated_text = data.get('generated_text', '')
        filename = f"N{i}.txt"
        saved = save_generated_text_to_file(generated_text, filename)
        if saved:
            print(f"Generated text saved to {user_profile_folder}/{filename}")
        else:
            print(f"Failed to save generated text to {user_profile_folder}/{filename}")
    else:
        print(f"Error calling /generate_text: Status code {response.status_code}")
