# scripts/youtube_topic_sentiment_table.py

import pandas as pd

# Define keywords per topic (from your LDA output)
topic_keywords = {
    1: ["treatment", "filariasis", "lymphatic", "dengue", "patients", "contact", "sir", "iad"],
    2: ["dengue", "treatment", "filariasis", "lymphoedema", "patients", "limb", "hai", "सकत"],
    3: ["dengue", "fever", "filariasis", "lymphatic", "nhi", "bhi", "hai", "sir"],
    4: ["treatment", "mein", "aur", "dengue", "yeh", "hai", "filariasis", "liye"]
}

# Load sentiment-labeled data
df = pd.read_csv("data/sentiment/youtube_sentiment.csv")

def assign_topic(row):
    text = str(row['clean_text'])
    for topic, kws in topic_keywords.items():
        if any(kw in text for kw in kws):
            return topic
    return None

df['topic'] = df.apply(assign_topic, axis=1)

summary = pd.crosstab(df['topic'], df['sentiment'], normalize='index') * 100
summary = summary.round(1).fillna(0)

print("YouTube Sentiment per Topic (%):\n")
print(summary)
summary.to_csv("output/figures/youtube_sentiment_per_topic.csv")
