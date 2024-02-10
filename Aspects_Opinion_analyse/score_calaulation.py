from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt

# Aspects and their summaries
# Correctly separated aspects
aspects = [
    "include specific programming languages Python, R, SQL and general areas like machine learning algorithms",
    "data cleaning, data wrangling challenges, and visualization tools.",
    "statistical questions, key concepts and statistical traps.",
    "Machine Learning Mastery",
    "Industry Insight",
    "Portfolio Power",
    "out of left field questions or tasks",
    "Behavioral Balance, technical expertise, soft skills, and team player"
]

summaries = {
 "include specific programming languages Python, R, SQL and general areas like machine learning algorithms":
        [
            "Brush up on Python, R, SQL, and machine learning." 
            "Be confident in your technical skills."
            "Stay confident and showcase your technical skills." 
            "Your preparation so far shows great dedication." 
            "You're on the right track! Keep focusing on technical skills like Python, R, SQL, and machine learning." 
            "Remember to showcase your strong technical skills in Python, R, and SQL."
        ],
 "data cleaning, data wrangling challenges, and visualization tools.":
        [
            "Show your data wrangling and visualization skills." 
            "Share impressive data wrangling challenges and unique visualization tools." 
            "Make sure to showcase your data wrangling challenges and impressive projects during the interview."
        ],
    "statistical questions, key concepts and statistical traps.":
        [


        ],
    "Machine Learning Mastery":
        [
            "Brush up on Python, R, SQL, and machine learning." 
            "Show your data wrangling and visualization skills, statistical knowledge, industry insights, and impressive projects."
            "Polish your technical skills, showcase data wrangling challenges and visualization tools, be familiar with key statistical concepts and machine learning topics, and highlight your portfolio projects."

        ],

    "Behavioral Balance, technical expertise, soft skills, and team player":
    [
            "Be confident in your technical skills."
            "Your preparation so far shows great dedication." 
            "Remember to showcase your strong technical skills in Python, R, and SQL." 
            "Make sure to demonstrate not just technical skills, but also your ability to communicate effectively and work well in a team."
            "Good luck with your interview! Your preparation and enthusiasm will surely make a positive impression." 
            "Remember to highlight your problem-solving skills and real-world applications of your knowledge."
    ],
    "Industry Insight":
        [
            "Stay updated on industry trends." 
            "Brush up on the latest industry trends."

        ],
    "Portfolio Power":
        [
            "Showcase your project portfolio." 
            "Highlight your portfolio."
            "Showcase impressive projects from your portfolio."

        ],
    "out of left field questions or tasks":
        [
            "Be open to unexpected questions."
            "Remember to stay confident and be open to unexpected questions."
            "Stay confident and good luck!"
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
    "Technical Proficiency",
    "Data Wrangling and Visualization",
    "Statistical Savvy",
    "Machine Learning Mastery",
    "Machine Learning Mastery",
    "Industry Insight",
    "Portfolio Power",
    "Out-of-Left-Field Questions or Tasks"
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