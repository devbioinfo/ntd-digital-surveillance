# scripts/news_sentiment_trend.py

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/sentiment/news_sentiment.csv')
df['published'] = pd.to_datetime(df['published'], errors='coerce')
df = df.dropna(subset=['published'])

df['month'] = df['published'].dt.to_period('M')
trend = df.groupby(['month', 'title_sentiment']).size().unstack(fill_value=0)

trend.plot(kind='line', marker='o', figsize=(12,6))
plt.ylabel('Number of Headlines')
plt.title('Google News Headline Sentiment Trend Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('output/figures/news_sentiment_trend.png')
plt.show()
