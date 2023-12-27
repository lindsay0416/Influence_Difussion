from sentence_transformers import SentenceTransformer


class Text2Vector:
    
    @staticmethod
    def get_embedding(text):
        # Initialize the Sentence Transformer model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        # Generate the embedding for the text
        embedding = model.encode(text).tolist()

        print(embedding)   
        return embedding
    
    # Received text vector
    @staticmethod
    def received_text_cosine_similarity(index_name, query_vector, es):
        script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['received_text_vector']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }
        response = es.search(index=index_name, body={"query": script_query, "size": 10})
        return response
    
    # Sent text vector
    @staticmethod
    def sent_text_cosine_similarity(index_name, query_vector, es):
        script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['sent_text_vector']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }
        response = es.search(index=index_name, body={"query": script_query, "size": 10})
        return response


            


 