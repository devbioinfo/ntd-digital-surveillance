# scripts/clean_google_news.py

import pandas as pd
import re
import os

os.makedirs("data/clean", exist_ok=True)

df = pd.read_csv('data/raw/google_news.csv')
df = df.drop_duplicates(subset=["title", "snippet"])

def clean_text(text):
    text = str(text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = text.strip().lower()
    return text

df['clean_title'] = df['title'].apply(clean_text)
df['clean_snippet'] = df['snippet'].apply(clean_text)

df.to_csv('data/clean/google_news_clean.csv', index=False)
print(f"Saved cleaned news to data/clean/google_news_clean.csv")
