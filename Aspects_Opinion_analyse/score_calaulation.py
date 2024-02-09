from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt

# Aspects and their summaries
aspects = [
    "The expansion aims to alleviate congestion and enable smoother, faster commutes by adding more lanes, allowing for increased vehicle volume and reduced travel times.",
    "Improved accessibility from the expansion is expected to attract businesses and boost local economies, potentially increasing tourism and creating new job opportunities.",
    "The project aims to reduce vehicle emissions through traffic flow optimization and includes the addition of green infrastructure like pedestrian paths and cycling lanes.",
    "By implementing modern design standards and adding dedicated lanes for buses and emergency vehicles, the expansion seeks to improve safety and address the community's growing concerns about traffic congestion and pollution.",
    "The construction phase is anticipated to impact daily commutes, with strategies like alternative routes, enhanced public transportation, and clear communication planned to mitigate these effects.",
    "The significant investment required for the expansion prompts questions about budget allocation and the potential impact on other public services, highlighting the need for transparent financial planning and the exploration of funding options.",
    "Construction activities may temporarily affect the local environment and communities, with measures like noise and dust control, off-peak construction scheduling, and the maintenance of green spaces aimed at minimizing negative impacts."
]

summaries = {
    "The expansion aims to alleviate congestion and enable smoother, faster commutes by adding more lanes, allowing for increased vehicle volume and reduced travel times.":
        [
            "It's important to prioritize clear communication and consider alternative routes to minimize disruptions during the construction phase."
            "Clear communication and considering alternative routes can help manage traffic effectively and alleviate congestion during construction."
            "I think it's important to prioritize clear communication and explore alternative transportation options to minimize disruptions."
            "Clear communication and exploring alternative transportation options are key to minimizing disruptions during the Harbour Bridge expansion."
            "I believe the Harbour Bridge expansion is a necessary step to improve commutes and promote sustainability."
        ],
    "Improved accessibility from the expansion is expected to attract businesses and boost local economies, potentially increasing tourism and creating new job opportunities.":
        [

            "None directly mention economic growth, but the emphasis on improving accessibility suggests acknowledgment of its potential to boost local economies."
            "None of the provided feedback directly mentions economic growth or how the expansion might attract businesses or boost local economies."
        ],
    "The project aims to reduce vehicle emissions through traffic flow optimization and includes the addition of green infrastructure like pedestrian paths and cycling lanes.":
        [
            "The feedback does not directly address reducing vehicle emissions or incorporating green infrastructure, such as pedestrian paths and cycling lanes."
            "None directly addressing environmental improvements in the provided feedback."
             "Thank you for the information. It's important to consider the potential impacts and find ways to mitigate disruptions. Have they considered any green initiatives for the project?"
            "Considering the potential impacts on public services and prioritizing clear communication can help address concerns over budget allocation and short-term disruptions."
            "While direct mentions of environmental improvements are absent, the project's aim to reduce emissions and incorporate green infrastructure aligns with sustainability goals expressed in the feedback."
        ],
    "By implementing modern design standards and adding dedicated lanes for buses and emergency vehicles, the expansion seeks to improve safety and address the community's growing concerns about traffic congestion and pollution.":
        [
            "Safety enhancements through modern design standards or dedicated lanes for buses and emergency vehicles are not directly mentioned in the feedback."
            "Clear communication and exploring alternative transportation options are key to minimizing disruptions during the Harbour Bridge expansion."
            "The feedback lacks direct comments on safety enhancements through modern design standards or the addition of dedicated lanes for buses and emergency vehicles."
            "None explicitly address safety enhancements, but the project's focus on modern design standards and dedicated lanes for emergency vehicles indirectly ties to feedback appreciating efforts to improve commutes and sustainability."
        ],
    "The construction phase is anticipated to impact daily commutes, with strategies like alternative routes, enhanced public transportation, and clear communication planned to mitigate these effects.":
        [
           "Several comments focus on mitigating short-term disruptions through enhanced communication, alternative routes, and seeking community feedback, aligning with the project's strategies to manage the impact on daily commutes."
           "Feedback frequently addresses minimizing short-term disruptions through enhanced communication, alternative routes, and suggests public-private partnerships for funding, which could help manage the construction phase's impact."
           "We appreciate your concerns and are actively exploring solutions to minimize disruptions."
            "Actively working to minimize disruptions and prioritize budget allocation is key, and we welcome any suggestions."
            "Considering community feedback, clear communication, and public transportation options are crucial for mitigating disruptions."
            "We are actively working to minimize disruptions and address budget allocation, and welcome suggestions."
           "Community involvement is crucial in addressing concerns and finding solutions."
           "It's great to see the focus on long-term benefits and community feedback. Clear communication about construction schedules and exploring alternative routes can help ease short-term disruptions."
           "Clear communication and exploring alternative transportation options are key to minimizing disruptions during the Harbour Bridge expansion."
           "Thank you for sharing your thoughts on the Harbour Bridge expansion. It's essential to prioritize clear communication and explore alternative routes to minimize short-term disruptions."
           
"Engaging in open dialogue and transparent communication with the community will help address concerns and find solutions."
           "Thank you for addressing the community's concerns. We understand the need for alternative routes, public transportation improvements, and transparent communication during construction."
           "It's great to see efforts being made to improve congestion and promote sustainability. Enhancing communication about construction schedules and considering alternative routes can help minimize disruptions."
           "Many comments suggest minimizing disruptions through clear communication, alternative routes, and considering public-private partnerships for funding which indirectly could alleviate financial pressures possibly affecting the project's execution and thus, indirectly, short-term traffic disruptions."
        ],
    "The significant investment required for the expansion prompts questions about budget allocation and the potential impact on other public services, highlighting the need for transparent financial planning and the exploration of funding options.":
        [
            "While there's acknowledgment of the project's significant investment and concerns about budget allocation, specific feedback on exploring funding options like public-private partnerships is not directly mentioned in relation to financial considerations."
            "Several comments suggest exploring public-private partnerships for funding, reflecting concerns about budget allocation and the need for transparent financial planning highlighted by the project."
            "Public-private partnerships could be a viable solution to fund the expansion while minimizing financial concerns."
            "Suggestions to improve communication and minimize disruptions for residents emphasize the need for efficient budget allocation."
            "Thank you for sharing your thoughts. It's crucial to ensure effective communication, consider alternative routes, and address budget concerns to optimize the long-term benefits of the Harbour Bridge expansion."
            "Exploring innovative funding options for the Harbour Bridge expansion project could address potential budget allocation impacts."
            "Engaging with the community and implementing clear communication strategies will be crucial for minimizing disruptions during the Harbour Bridge expansion."
            "Considering the potential impacts on public services and prioritizing clear communication can help address concerns over budget allocation and short-term disruptions."
            "Considering the long-term benefits, it's important to prioritize clear communication, strategize alternative routes, and address concerns about budget allocation for the Harbour Bridge expansion. Any specific concerns or questions you'd like to address?"
            "Community involvement is crucial in addressing concerns and finding solutions. Open dialogue, transparent communication, and exploring alternative transportation options can help navigate the short-term disruptions and budget considerations."
        ],
     "Construction activities may temporarily affect the local environment and communities, with measures like noise and dust control, off-peak construction scheduling, and the maintenance of green spaces aimed at minimizing negative impacts.":
        [
            "While specific actions like noise and dust control measures aren't directly mentioned, the emphasis on clear communication and community engagement suggests a concern for mitigating negative impacts on the community, which can be related to environmental and community impact indirectly."
            "Feedback does not specifically address the temporary environmental and community impacts of construction activities or measures to minimize these impacts."
             "Feedback does not specifically address the temporary environmental and community impacts of construction activities or measures to minimize these impacts."
            "Feedback does not specifically address the temporary effects of construction activities on the local environment and communities, nor does it mention measures like noise and dust control or off-peak construction scheduling."
            "Although not explicitly mentioned, the feedback's focus on community engagement, clear communication, and addressing budget concerns suggests an indirect connection to minimizing negative environmental and community impacts during construction."

    ]
}


# Function to calculate cosine similarity
def calculate_similarity(aspect, summaries):
    if not summaries:  # If no summaries, return None
        return [None]
    texts = [aspect] + summaries  # Combine aspect and summaries for TF-IDF
    print("texts: ", texts)
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    return cosine_similarities


# Calculate similarities for each aspect and its summaries
similarity_results = {}
for aspect in aspects:
    similarity_results[aspect] = calculate_similarity(aspect, summaries[aspect])

print(similarity_results)


# Correcting the aspect names in the similarity calculation to match the chart labels
corrected_aspect_names = [
    "Enhanced Traffic Flow",
    "Economic Growth",
    "Environmental Improvements",
    "Safety Enhancements",
    "Short-term Traffic Disruptions",
    "Financial Considerations",
    "Environmental and Community Impact"
]

# Calculating average similarity for each aspect
average_similarities = {}
for aspect, similarities in similarity_results.items():
    if similarities[0] is not None:
        average_similarities[aspect] = np.mean(similarities)
    else:
        average_similarities[aspect] = 0  # Assigning 0 where there are no summaries


# Preparing data for plotting
labels = corrected_aspect_names
values = [average_similarities.get(aspect, 0) for aspect in aspects]
print("Average: ", values)

# Plotting a bar chart
plt.figure(figsize=(10, 6))
plt.bar(labels, values, color='skyblue')
plt.xlabel('Aspect')
plt.ylabel('Average Similarity')
plt.xticks(rotation=45, ha='right')
plt.title('Average Similarity Scores for Each Aspect')
plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels

# Showing the plot
plt.show()