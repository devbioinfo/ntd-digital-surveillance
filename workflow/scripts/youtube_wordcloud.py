# scripts/youtube_wordcloud.py

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

df = pd.read_csv('data/clean/youtube_comments_clean.csv')
text = " ".join(df['clean_text'].astype(str).tolist())
wc = WordCloud(width=800, height=400, background_color='white').generate(text)

plt.figure(figsize=(12,6))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
os.makedirs("output/figures", exist_ok=True)
plt.savefig("output/figures/youtube_wordcloud.png")
plt.show()
