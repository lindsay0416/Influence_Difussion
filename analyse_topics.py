from elasticsearch import Elasticsearch
import nltk
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import matplotlib.pyplot as plt
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary
import numpy as np
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

# Assuming fetch_texts function is defined as shown previously

# Preprocess text
def preprocess_text(text):
    """Preprocess a single text document."""
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    text = re.sub(r'\W', ' ', text.lower())
    text = re.sub(r'\s+', ' ', text)
    words = [lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words]
    return words

def perform_lda(texts):
    """Perform LDA topic modeling on a list of preprocessed text documents."""
    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda_model = LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15, random_state=42)
    return lda_model, dictionary

def global_topic_distribution(index_name, es):
    """Analyze and visualize the global topic distribution across all texts in Elasticsearch."""
    # Placeholder for fetch_texts, assuming it returns a list of tuples (received_text, sent_text)
    texts = fetch_texts(index_name, es)  # Implement fetch_texts to retrieve data from Elasticsearch
    aggregated_texts = [preprocess_text(received + " " + sent) for received, sent in texts]
    
    lda_model, dictionary = perform_lda(aggregated_texts)
    
    # Aggregate topic distribution
    topic_distribution = np.zeros(lda_model.num_topics)
    for text in aggregated_texts:
        bow = dictionary.doc2bow(text)
        for topic, prob in lda_model.get_document_topics(bow):
            topic_distribution[topic] += prob
            
    # Normalize to get average distribution
    topic_distribution /= len(aggregated_texts)
    
    # Visualization
    plt.figure(figsize=(10, 5))
    plt.bar(range(lda_model.num_topics), topic_distribution, tick_label=[f"Topic {i}" for i in range(lda_model.num_topics)])
    plt.xlabel('Topic ID')
    plt.ylabel('Average Probability')
    plt.title('Global Topic Distribution Across All Texts')
    plt.show()



    

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

    global_topic_distribution(index_name, es)

    #---- Test fetch text -------
    # texts = fetch_texts(index_name, es)

    # ---- Output or process the texts as needed ----
    # for received, sent in texts:
    #     print("Received Text:", received)
    #     print("Sent Text:", sent)
    #     print("---")
   

if __name__ == '__main__':
    main()


# Topic Coherence Over Iterations

# from gensim.models.coherencemodel import CoherenceModel
# import matplotlib.pyplot as plt

# # Assuming 'texts' is your preprocessed text data and 'dictionary' is a Gensim dictionary created from 'texts'
# coherence_scores = []
# iterations = range(10, 101, 10)  # Example: Iterating over 10 to 100 in steps of 10

# for iter_count in iterations:
#     lda_model = LdaModel(corpus=[dictionary.doc2bow(text) for text in texts], num_topics=5, iterations=iter_count, id2word=dictionary)
#     coherence_model = CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
#     coherence_scores.append(coherence_model.get_coherence())

# # Plotting
# plt.plot(iterations, coherence_scores)
# plt.xlabel('Iterations')
# plt.ylabel('Coherence Score')
# plt.title('Topic Coherence Over Iterations')
# plt.show()
