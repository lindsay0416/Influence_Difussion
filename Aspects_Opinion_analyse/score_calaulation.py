from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt

# Aspects and their summaries
# Correctly separated aspects
aspects = [
    "Gathering initial reactions to SmartGadget Pro.",
    "Identifying exciting features and areas for enhancement.",
    "Focusing on key performance metrics for evaluation.",
    "Discussing the balance between aesthetics and functionality.",
    "Determining acceptable pricing for the features offered.",
    "Soliciting feedback for improvement.",
    "Crafting resonant marketing messages for the target audience."

]

summaries = {
 "Gathering initial reactions to SmartGadget Pro.":
        [
            "Excitement and anticipation are the primary reactions, with users looking forward to providing feedback and being part of the innovation journey."
            "Individuals express excitement and anticipation for providing feedback on SmartGadget Pro, highlighting their eagerness to see its integration into daily life and its potential to enhance efficiency."
            "Users are excited and eagerly anticipate the opportunity to contribute their insights, indicating positive initial reactions."
            "There's a universal sense of thrill and excitement among tech enthusiasts about the upcoming launch of SmartGadget Pro, with many eagerly anticipating the chance to share their feedback and contribute to its success."
            "Participants express strong enthusiasm and anticipation for providing feedback on SmartGadget Pro, highlighting an overall positive and excited initial reaction."
            "Participants express strong excitement and anticipation about trying out SmartGadget Pro and sharing their feedback, indicating positive initial reactions and high expectations for the device."
            "There is strong excitement and anticipation from individuals looking forward to being a part of the revolution introduced by SmartGadget Pro. The repeated use of "
            "There is overwhelming excitement and anticipation for the launch of SmartGadget Pro, with individuals eager to share their feedback and be part of the innovation."
            "There's palpable excitement and anticipation for the launch of SmartGadget Pro, with individuals expressing eagerness to contribute their insights and see how the device integrates into daily life."
        ],
 "Identifying exciting features and areas for enhancement.":
        [
            "Users express eagerness to share their feedback on SmartGadget Pro's features, indicating an interest in both praising and suggesting improvements."
            "Respondents are particularly interested in how SmartGadget Pro will transform daily routines and enhance efficiency, indicating a focus on its practical applications and potential areas for improvement based on user experience."
            "Although specific features are not detailed, the enthusiasm to provide feedback suggests an eagerness to explore the device's capabilities and suggest areas for improvement."
            "While specific features are not detailed, the eagerness to share insights suggests a readiness to identify both exciting aspects and potential areas for improvement."
            "a game-changing device in the tech industry they've been waiting for, and look forward to providing valuable feedback for enhancement."
            "Participants are looking forward to discovering how SmartGadget Pro will transform daily routines and enhance efficiency, suggesting a keen interest in its features and potential areas for improvement."
            "Respondents are thrilled to explore how SmartGadget Pro will enhance daily life and efficiency, indicating a focus on its features and potential areas for further improvement based on user experience."
            "While specific features are not detailed, the eagerness to share insights and feedback suggests a readiness to identify both exciting aspects and potential areas for improvement once they have the opportunity to experience the device."
            "There's a strong sense of anticipation to share thoughts on what might make SmartGadget Pro a game-changer, suggesting users are ready to identify standout features and potential areas for improvement."
        ],
    "Focusing on key performance metrics for evaluation.":
        [
            "While not explicitly mentioned, the enthusiasm for contributing feedback implies a readiness to assess SmartGadget Pro's performance."
            "The text does not specify key performance metrics, but the commitment to provide feedback implies a readiness to assess the device's performance critically."
            "The excitement around contributing feedback implies an interest in evaluating the device's performance, though specific metrics are not mentioned. The focus is more on the overall experience and the innovative features of SmartGadget Pro."
            "While not directly mentioned, the eagerness to contribute insights implies a readiness to evaluate the device's performance against expectations."
            "The anticipation to contribute feedback and be part of the tech revolution indicates a desire to evaluate SmartGadget Pro on key performance metrics, particularly its impact on technology and daily life."
            "While specific key performance metrics are not directly mentioned, the general excitement and willingness to provide feedback imply an interest in evaluating the device's performance in terms of integration and efficiency enhancement."
            "The excitement around contributing feedback implies an interest in evaluating the device's performance, though specific metrics are not mentioned."
            "The excitement to see how SmartGadget Pro enhances efficiency suggests that users are keen on evaluating its performance metrics, particularly its impact on daily life and productivity."
            "Although not explicitly stated, the enthusiasm to provide feedback implies a readiness among tech enthusiasts to evaluate the device's performance and its potential to enhance daily routines."
        ],

    "Discussing the balance between aesthetics and functionality.":
    [
            "The anticipation surrounding SmartGadget Pro suggests that users are keen on evaluating how well it integrates design with practical utility."
            "While direct mentions of aesthetics or functionality are absent, the general excitement indicates an interest in how SmartGadget Pro will integrate and enhance daily life, hinting at considerations of both design and utility."
        "The excitement around contributing insights may also extend to discussions on how SmartGadget Pro balances its design with practical utility."
            "While specific details on aesthetics and functionality are not directly mentioned, the overall excitement hints at high expectations for a balance between sleek design and practical utility."
            "While the text does not explicitly discuss the balance between aesthetics and functionality, the expressed enthusiasm implies an expectation for SmartGadget Pro to excel in both design and utility."
            "The text implies a positive anticipation towards the device's functionality, with an emphasis on seamless integration into daily life, suggesting that users value both aesthetics and practical utility."
            "Participants look forward to seeing how SmartGadget Pro integrates into daily life, suggesting an interest in discussing the balance between the device's aesthetics and its practical utility."
        "The anticipation of sharing feedback and contributing to the innovation process hints at a forthcoming discussion on how SmartGadget Pro balances its design with practical utility."
        "The text does not directly discuss aesthetics or functionality, but the anticipation to experience SmartGadget Pro and its innovative features suggests an interest in how the device will balance these aspects."
    ],
    "Determining acceptable pricing for the features offered.":
        [
            "Pricing is not directly addressed, but the eagerness to engage with SmartGadget Pro hints at users' interest in determining value for money."
            "Pricing is not directly mentioned, but the eagerness to participate in the feedback process and the innovation journey hints at a user base that values the device's features and is likely considerate of their cost-effectiveness."
            "Pricing discussions are not explicitly mentioned, but the eagerness to participate in the feedback process suggests a user base that values innovation, potentially indicating an openness to discuss pricing in relation to offered features."
            "Pricing discussions are not directly addressed, but the overall enthusiasm suggests an interest in how the device's value proposition aligns with its cost."
            "The text does not explicitly address pricing concerns, but the eagerness to engage with SmartGadget Pro and provide feedback suggests that users are interested in assessing the value proposition of its features."
            "Although not explicitly mentioned, the enthusiasm for providing feedback and participating in the device's development process indicates a user base that might be considerate of the value proposition offered by SmartGadget Pro's features versus its pricing."
            "There's no direct mention of pricing discussions, but the overall eagerness to contribute suggests an interest in assessing the value proposition of SmartGadget Pro."
            "There's no direct mention of pricing discussions, but the overall eagerness to contribute suggests an interest in assessing the value proposition of SmartGadget Pro once more details are known."
            "Pricing discussions are not mentioned explicitly, but the eagerness to participate in the feedback process indicates a user base that values innovation, potentially influencing discussions on pricing relative to the device's features."

    ],
    "Soliciting feedback for improvement.":
        [
            "Users are excited about the opportunity to provide feedback, indicating a willingness to help refine and enhance SmartGadget Pro."
            "The repeated invitations to share insights underscore a proactive approach to gathering feedback for potential improvements to SmartGadget Pro."
            "The messages highlight a strong solicitation for feedback, with both the company and users showing a proactive stance towards utilizing feedback to refine and perfect SmartGadget Pro, indicating a collaborative approach to its improvement."
            "The repeated expressions of excitement to provide feedback underscore a proactive approach to soliciting input for potential improvements to SmartGadget Pro."
            "The repeated mentions of looking forward to giving feedback highlight a proactive approach from both the community and the company towards using customer insights for continuous improvement."
            "There is a strong emphasis on soliciting and providing feedback, demonstrating a proactive approach from both the company and users towards using feedback to refine and enhance SmartGadget Pro."
            "The repeated expressions of excitement to provide feedback underscore a proactive approach to soliciting input for potential improvements to SmartGadget Pro."
            "There is a strong indication of soliciting feedback for improvement, with several mentions of excitement to share insights, thoughts, and contribute to the innovation process, demonstrating a proactive approach to refining SmartGadget Pro."
            
        "There is a clear indication of soliciting feedback for improvement, with multiple mentions of excitement to share insights, thoughts, and contribute to the innovation process, demonstrating a proactive approach to refining SmartGadget Pro."
    ],
    "Crafting resonant marketing messages for the target audience.":
    [
            "The shared enthusiasm and use of the hashtag #SmartGadgetProFeedback suggest that engaging, community-driven messages resonate well with the audience."
            "The communications effectively resonate with the target audience by acknowledging their enthusiasm for innovation and inviting them to contribute to the tech revolution, reflecting a deep understanding of how to engage tech enthusiasts."
            "The communications effectively engage the target audience by expressing appreciation for their enthusiasm and inviting them to contribute to the tech revolution, showcasing an understanding of how to craft messages that resonate with tech enthusiasts and potential users."
            "The communication strategy effectively engages the target audience by appreciating their enthusiasm and inviting them to contribute to the tech revolution, demonstrating an understanding of crafting messages that resonate with tech enthusiasts and potential users."
            "The text reflects ongoing efforts to engage a tech-enthusiast audience with resonant marketing messages, emphasizing innovation, participation in a tech revolution, and the collaborative shaping of SmartGadget Pro's future."
            "The text reflects an ongoing effort to engage a tech-enthusiast audience with resonant marketing messages, emphasizing innovation, participation in a tech revolution, and the collaborative shaping of SmartGadget Pro's future."
            "The consistent emphasis on excitement, innovation, and being part of the revolution suggests an ongoing effort to craft marketing messages that resonate deeply with tech enthusiasts and potential users, highlighting the innovative aspects of SmartGadget Pro."
            "The consistent emphasis on excitement, innovation, and being part of the revolution suggests efforts to craft marketing messages that resonate deeply with tech enthusiasts and potential users."
        "The consistent use of #SmartGadgetProFeedback and emphasis on innovation and revolutionizing the tech world suggest efforts to craft marketing messages that resonate with tech enthusiasts and potential users."
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
    "First Impressions",
    "Features",
    "Performance Parameters",
    "Design Dialogue",
    "Price Point Perspective",
    "Constructive Critiques",
    "Marketing Messages"
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