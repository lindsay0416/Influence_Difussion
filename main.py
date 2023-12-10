from embedding_utils import Text2Vector
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
    Text2Vector.get_embedding(text)

if __name__ == '__main__':
    main()