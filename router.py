from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError


app = Flask(__name__)

# Connect to local Elasticsearch instance
es = Elasticsearch("http://localhost:9200")

# Check if Elasticsearch is running
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Could not connect to Elasticsearch")


@app.route('/add_record', methods=['POST'])
def add_record():
    index_name = request.json.get('index')
    document_id = request.json.get('id')
    document_body = request.json.get('body')

    if not index_name or not document_id or not document_body:
        return jsonify({"error": "Index name, document ID, and body are required"}), 400

    try:
        response = es.index(index=index_name, id=document_id, document=document_body)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_record/<index_name>/<document_id>', methods=['GET'])
def get_record(index_name, document_id):
    try:
        response = es.get(index=index_name, id=document_id)
        return jsonify(response['_source']), 200
    except NotFoundError:
        return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    