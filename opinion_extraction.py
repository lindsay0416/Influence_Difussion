from transformers import pipeline
import os

# Initialize the summarization pipeline with a specific model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

directory_path = "conversation_flow"  # Directory containing the text files

def read_and_split_file(file_path, max_chunk_length=500):
    """Reads a file and splits it into chunks of words that are roughly within the max_chunk_length limit."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        words = content.split()
        chunks = []
        current_chunk = []
        current_length = 0
        for word in words:
            word_length = len(word) + 1  # Adding 1 for space
            if current_length + word_length > max_chunk_length:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        chunks.append(" ".join(current_chunk))  # Add the last chunk
        return chunks

def summarize_chunks(chunks, max_length=8, min_length=30):
    """Summarizes each chunk of text and combines the summaries into a single output."""
    summaries = []
    for chunk in chunks:
        # Guard against empty chunks
        if not chunk.strip():
            continue
        summary = summarizer(chunk, max_length=8, min_length=5, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    combined_summary = ' '.join(summaries)
    return combined_summary

def summarize_file(file_path):
    """Reads, chunks, and summarizes the content of a single file."""
    chunks = read_and_split_file(file_path)
    summary = summarize_chunks(chunks)
    return summary

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
