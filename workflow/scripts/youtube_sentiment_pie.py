# scripts/youtube_sentiment_pie.py

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/sentiment/youtube_sentiment.csv')
counts = df['sentiment'].value_counts()

plt.figure(figsize=(6,6))
counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#99ff99','#ff9999'])
plt.ylabel('')
plt.title('YouTube Comments Sentiment Distribution')
plt.savefig("output/figures/youtube_sentiment_pie.png")
plt.show()
