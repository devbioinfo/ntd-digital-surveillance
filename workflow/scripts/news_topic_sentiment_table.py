# scripts/news_topic_sentiment_table.py

import pandas as pd

topic_keywords = {
    1: ["india", "kalaazar", "dengue", "health", "lymphatic", "filariasis", "eliminate", "cases"],
    2: ["india", "dengue", "times", "chikungunya", "vaccine", "filariasis", "disease", "lymphatic"],
    3: ["india", "chikungunya", "dengue", "leishmaniasis", "fever", "virus", "frontiers", "visceral"],
    4: ["india", "dengue", "health", "filariasis", "times", "world", "organization", "cases"]
}

df = pd.read_csv("data/sentiment/news_sentiment.csv")

def assign_topic(row):
    text = str(row['clean_title'])
    for topic, kws in topic_keywords.items():
        if any(kw in text for kw in kws):
            return topic
    return None

df['topic'] = df.apply(assign_topic, axis=1)

summary = pd.crosstab(df['topic'], df['title_sentiment'], normalize='index') * 100
summary = summary.round(1).fillna(0)

print("News Sentiment per Topic (%):\n")
print(summary)
summary.to_csv("output/figures/news_sentiment_per_topic.csv")
