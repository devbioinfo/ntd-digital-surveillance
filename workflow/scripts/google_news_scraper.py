# scripts/google_news_scraper.py

import feedparser
import pandas as pd
import os
from datetime import datetime

# Search queries for your NTDs
queries = [
    'dengue India',
    'chikungunya India',
    'kala-azar India',
    'filariasis India'
]

# Google News RSS URL template
rss_template = (
    "https://news.google.com/rss/search?q={query}+after:2019-01-01+before:2024-05-31"
    "&hl=en-IN&gl=IN&ceid=IN:en"
)

records = []

for q in queries:
    url = rss_template.format(query=q.replace(" ", "+"))
    print(f"Fetching news for: {q}")
    feed = feedparser.parse(url)
    for entry in feed.entries:
        # Parse date
        try:
            published = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
        except:
            published = entry.get("published", "")
        records.append({
            "query": q,
            "title": entry.title,
            "link": entry.link,
            "published": published,
            "snippet": entry.summary
        })

# Save to CSV
os.makedirs("data/raw", exist_ok=True)
df = pd.DataFrame(records)
df.to_csv("data/raw/google_news.csv", index=False)
print(f"\nSaved {len(df)} news headlines/snippets to data/raw/google_news.csv")
