# scripts/sentiment_youtube.py

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

os.makedirs("data/sentiment", exist_ok=True)

df = pd.read_csv('data/clean/youtube_comments_clean.csv')
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = analyzer.polarity_scores(str(text))
    if score['compound'] >= 0.05:
        return 'positive'
    elif score['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

df['sentiment'] = df['clean_text'].apply(get_sentiment)
df.to_csv('data/sentiment/youtube_sentiment.csv', index=False)
print(f"Saved sentiment-labeled comments to data/sentiment/youtube_sentiment.csv")
