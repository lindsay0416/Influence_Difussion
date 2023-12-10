from embedding_utils import get_embedding
from elasticsearch import Elasticsearch



def main():
    # Connect to local Elasticsearch instance
    es = Elasticsearch("http://localhost:9200")

    # Check if Elasticsearch is running
    if es.ping():
        print("Connected to Elasticsearch")
    else:
        print("Could not connect to Elasticsearch")

    # text to vector 
    text = "Stores the text and its embedding into Elasticsearch."
    get_embedding(text)

if __name__ == '__main__':
    main()