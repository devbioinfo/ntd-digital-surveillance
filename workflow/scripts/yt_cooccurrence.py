# scripts/yt_cooccurrence.py

import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/clean/youtube_comments_clean.csv')
words = [w for text in df['clean_text'].dropna() for w in text.split()]
top_words = [w for w, _ in Counter(words).most_common(15)]

matrix = np.zeros((len(top_words), len(top_words)), dtype=int)

for text in df['clean_text'].dropna():
    tokens = set(text.split())
    for i, w1 in enumerate(top_words):
        for j, w2 in enumerate(top_words):
            if w1 != w2 and w1 in tokens and w2 in tokens:
                matrix[i, j] += 1

plt.figure(figsize=(10,8))
sns.heatmap(matrix, annot=True, xticklabels=top_words, yticklabels=top_words, fmt='d', cmap='Blues')
plt.title('Co-occurrence of Top 15 Words in YouTube Comments')
plt.tight_layout()
plt.savefig('output/figures/youtube_cooccurrence_heatmap.png')
plt.show()
