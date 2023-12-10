from sentence_transformers import SentenceTransformer



def get_embedding(text):
    # Initialize the Sentence Transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # Generate the embedding for the text
    embedding = model.encode(text).tolist()

    print(embedding)   
    return embedding


