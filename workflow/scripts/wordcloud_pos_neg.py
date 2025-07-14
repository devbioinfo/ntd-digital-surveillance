# scripts/wordcloud_pos_neg.py

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/sentiment/youtube_sentiment.csv")

for sentiment in ["positive", "negative"]:
    text = " ".join(df[df['sentiment'] == sentiment]['clean_text'].astype(str).tolist())
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"YouTube Comments: Most Frequent Words ({sentiment.title()})")
    plt.tight_layout()
    plt.savefig(f"output/figures/yt_wordcloud_{sentiment}.png", dpi=300)
    plt.close()
