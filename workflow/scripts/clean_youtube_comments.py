# scripts/clean_youtube_comments.py

import pandas as pd
import re

df = pd.read_csv('data/raw/youtube_comments.csv')

# Drop duplicates
df = df.drop_duplicates(subset=["text"])

def clean_text(text):
    text = str(text)
    text = re.sub(r"http\S+", "", text)          # remove URLs
    text = re.sub(r"@\w+", "", text)             # remove mentions
    text = re.sub(r"[^\w\s]", "", text)          # remove punctuation
    text = text.strip().lower()
    return text

df['clean_text'] = df['text'].apply(clean_text)

df.to_csv('data/clean/youtube_comments_clean.csv', index=False)
print(f"Saved cleaned comments to data/clean/youtube_comments_clean.csv")
