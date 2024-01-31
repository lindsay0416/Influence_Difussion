
import requests

class GenerateText:
    # Function to post data to the /generate_text API and receive the generated text
    @staticmethod
    def get_generated_text(api_url, prompt):
        response = requests.post(f"{api_url}/generate_text", json={'prompt': prompt})
        return response.json().get('generated_text', 'No generation result found.') if response.ok else None
    

    @staticmethod
    # Check the id of a document in each index.
    # Make the id a unique number in Elasticsearch
    def get_next_id(index_name):
        # Document ID for the counter
        counter_id = 'counter'

        # Try to get the current counter value
        try:
            current_counter = es.get(index=index_name, id=counter_id)['_source']
            next_id = current_counter['last_id'] + 1
        except NotFoundError:
            # If not found, start from 1
            next_id = 1

        # Update the counter
        es.index(index=index_name, id=counter_id, document={'last_id': next_id})

        return next_id