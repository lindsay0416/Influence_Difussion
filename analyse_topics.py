from elasticsearch import Elasticsearch
import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')

def fetch_texts(index_name, es):
    # Define the search query to retrieve all documents
    # Adjust the size parameter as needed to fetch more documents
    query = {
        "size": 10000,  # Example to retrieve up to 10,000 documents
        "query": {
            "match_all": {}
        }
    }

    # Perform the search query
    response = es.search(index=index_name, body=query)
    texts = []

    # Iterate through the hits and extract received and sent texts
    for hit in response['hits']['hits']:
        doc = hit["_source"]
        received_text = doc.get("received_text", "")
        sent_text = doc.get("sent_text", "")
        texts.append((received_text, sent_text))
    
    return texts


def main():
    # Connect to local Elasticsearch instance
    es = Elasticsearch("http://localhost:9200")

    # Check if Elasticsearch is running
    if es.ping():
        print("Connected to Elasticsearch")
    else:
        print("Could not connect to Elasticsearch")
    
    # Anaylse sent_text_test01 Elasticsearch index
    index_name = 'sent_text_test01'
    texts = fetch_texts(index_name, es)

    # # Output or process the texts as needed
    # for received, sent in texts:
    #     print("Received Text:", received)
    #     print("Sent Text:", sent)
    #     print("---")

   

if __name__ == '__main__':
    main()