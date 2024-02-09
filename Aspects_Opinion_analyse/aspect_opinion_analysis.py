import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.chunk.regexp import RegexpParser
from collections import Counter

# Ensure the necessary NLTK datasets are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

extracted_aspects = ["Enhanced Traffic Flow", "Economic Growth", "Environmental Improvements", "Safety Enhancements",\
                     "Short-term Traffic Disruptions", "Financial Considerations", "Environmental and Community Impact"]


def preprocess(document):
    document = document.lower()  # Lowercase the document
    sentences = sent_tokenize(document)  # Tokenize into sentences
    stop_words = set(stopwords.words('english'))
    cleaned_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        # Remove stopwords and non-alphanumeric words
        cleaned_words = [word for word in words if word.isalnum() and word not in stop_words]
        cleaned_sentences.append(cleaned_words)
    return cleaned_sentences


def extract_aspects(sentences):
    aspects = []
    grammar = "NP: {<DT>?<JJ>*<NN>}"  # Define a chunk grammar for noun phrases
    cp = RegexpParser(grammar)
    for sentence in sentences:
        tagged_sentence = pos_tag(sentence)  # Tag parts of speech
        tree = cp.parse(tagged_sentence)  # Chunk sentence based on the defined grammar
        for subtree in tree.subtrees():
            if subtree.label() == 'NP':
                aspect = " ".join(word for word, tag in subtree.leaves())
                aspects.append(aspect)
    return aspects


# Example text from your document
text = """ The government's initiative to expand the Harbour Bridge marks a significant turning point for our city's infrastructure, \
        aiming to reshape our daily commutes and overall urban landscape. This ambitious project, \
        set to unfold over the next three years, promises to bring a multitude of long-term benefits, \
        despite the anticipated short-term disruptions and the substantial financial investments required. We are eager to delve into your perspectives, \
        concerns, and suggestions regarding this transformative venture. Benefits of the Harbour Bridge Expansion \
        1.	Enhanced Traffic Flow: The expansion is designed to alleviate congestion, enabling smoother and faster commutes. By adding more lanes, the bridge will accommodate a larger volume of vehicles, reducing travel times and contributing to a more efficient transportation network. \
        2.	Economic Growth: Improved accessibility could spur economic development in surrounding areas, attracting businesses and boosting local economies. The ease of transportation may lead to increased tourism and create new job opportunities, contributing to the city's prosperity. \
        3.	Environmental Improvements: With traffic flow optimization, we can expect a reduction in vehicle emissions, contributing to cleaner air. The project also presents an opportunity to incorporate green infrastructure elements, such as pedestrian paths and cycling lanes, promoting sustainable transport options. \
        4.	Safety Enhancements: The expansion will address current safety concerns by implementing modern design standards and possibly adding dedicated lanes for buses and emergency vehicles, ensuring a safer travel experience for everyone. Impact on Daily Life in Recent Years In recent years, \
        our community has grappled with growing traffic congestion, leading to longer commutes and increased pollution. The expansion of the Harbour Bridge is a response to these challenges, aiming to transform our city's mobility and quality of life. \
        However, the path to improvement comes with its set of obstacles. Concerns and Ideas for Minimizing Disruption 1.	Short-term Traffic Disruptions: The construction phase will inevitably impact daily commutes. Strategies such as alternative routes, \
        enhanced public transportation options, and clear communication about construction schedules can help mitigate these effects. \
        2.	Financial Considerations: The significant investment required for the expansion raises questions about budget allocation and potential impacts on other public services. \
        Transparency in financial planning and exploring funding options, such as grants or public-private partnerships, may address these concerns. \
        3.	Environmental and Community Impact: Construction activities may temporarily affect the local environment and nearby communities. Implementing noise and dust control measures, scheduling construction during off-peak hours, and maintaining open green spaces can help minimize negative impacts.
        I have a text document like this, could you write python code to extract the aspects inside this document? including the data preprocessing please """


def main():
    cleaned_sentences = preprocess(text)  # Preprocess the document
    aspects = extract_aspects(cleaned_sentences)  # Extract aspects

    # Count the occurrences of each aspect and keep the top 6
    aspect_counts = Counter(aspects)
    top_aspects = aspect_counts.most_common(10)

    # Print top 6 extracted aspects
    print("Top 6 Extracted Aspects:")
    for aspect, count in top_aspects:
        print(f"{aspect}: {count} times")



if __name__ == '__main__':
    main()

