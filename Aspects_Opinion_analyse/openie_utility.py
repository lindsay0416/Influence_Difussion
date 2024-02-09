from openie import StanfordOpenIE


summaries = {
    "Enhanced Traffic Flow": [],
    "Economic Growth": [],
    "Environmental Improvements": [],
    "Safety Enhancements": [],
    "Short-term Traffic Disruptions": [
        "Alternative routes and clear communication can mitigate disruptions.",
        "Community engagement and updates on schedules are essential for alleviating disruptions.",
        "Acknowledgment of concerns with a commitment to minimizing disruptions."
    ],
    "Financial Considerations": [
        "Budget allocation should not negatively impact other services.",
        "Community feedback on budget allocation is crucial for implementation success.",
        "Actively working on minimizing disruptions and effective budget management.",
        "Engaging the community and exploring partnerships to address financial concerns."
    ],
    "Environmental and Community Impact": [
        "Community engagement is key to addressing concerns and ensuring project success.",
        "Involving the community and clear communication are critical, especially regarding public services.",
        "Commitment to engaging the community through various means for project success.",
        "Importance of community feedback and involvement in addressing potential impacts."
    ]
}


class OpenieUtility:
    client = StanfordOpenIE()

    @staticmethod
    def sentence_to_triple(sentence):
        triples = []
        # client =  StanfordOpenIE()
        for triple in OpenieUtility.client.annotate(sentence):
            # print('|-', triple)
            triples.append(triple)
        return triples



def main():
    input_text = "Almond is brown colour"
    aa = OpenieUtility.sentence_to_triple(input_text)
    print(aa)


if __name__ == "__main__":
    main()