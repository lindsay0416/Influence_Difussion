from sentence_transformers import SentenceTransformer
from elasticsearch import RequestError

class Text2Vector:
    
    @staticmethod
    def get_embedding(text):
        # Initialize the Sentence Transformer model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        # Generate the embedding for the text
        embedding = model.encode(text).tolist()
        return embedding
    
    # Received text vector
    @staticmethod
    def received_text_cosine_similarity(index_name, query_vector, es):
        script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": """
                if (!doc['received_text_vector'].empty) {
                    return cosineSimilarity(params.query_vector, 'received_text_vector') + 1.0;
                } else {
                    return 0.0; // Default score if vector is missing
                }
                """,
                "params": {"query_vector": query_vector}
                }
            }
        }
        try:
            response = es.search(index=index_name, body={"query": script_query, "size": 10})
            return response
        except RequestError as e:
            print("RequestError occurred:", e.info)
            raise
    
    # Sent text vector
    @staticmethod
    def sent_text_cosine_similarity(index_name, query_vector, es):   
        script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'sent_text_vector') + 1.0",
                "params": {"query_vector": query_vector}
                }
            }
        }
        try:
            response = es.search(index=index_name, body={"query": script_query, "size": 1})
            return response
        except RequestError as e:
            print("RequestError occurred:", e.info)
            raise

    # return the similarity score
    @staticmethod
    def get_similarity_score(SimilarityResp):
        scores = []
        for hit in SimilarityResp['hits']['hits']:
            score = hit['_score'] - 1.0  # Subtracting 1.0 because we added 1.0 in the script
            scores.append(score)
        return scores
        
    # Test, return the detail of an index.
    @staticmethod
    def test_script(index_name, es):
        script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "1"  # Just returns a constant score
            }
        }
    }
        response = es.search(index=index_name, body={"query": script_query, "size": 10})
        return response

            


 