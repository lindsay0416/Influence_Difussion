from transformers import pipeline
import os

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

# Define the path to your conversation_flow directory
directory_path = "conversation_flow"

# Function to summarize the content of a given file
def summarize_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Adjust max_length and min_length according to your needs
        summary = summarizer(content, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']

# Loop through the files and summarize each
for i in range(1, 11):
    file_name = f"round{i:02}.txt"
    file_path = os.path.join(directory_path, file_name)
    if os.path.exists(file_path):
        print(f"Summarizing {file_name}...")
        summary_text = summarize_file(file_path)
        print(f"Summary for {file_name}:")
        print(summary_text)
        print("\n")
    else:
        print(f"{file_name} does not exist.")
