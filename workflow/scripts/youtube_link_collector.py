# scripts/youtube_link_collector.py

import os  # <-- Add this line!
from youtubesearchpython import VideosSearch
import pandas as pd

queries = [
    "dengue india", "डेंगू भारत",
    "chikungunya india", "चिकनगुनिया भारत",
    "kala-azar india", "कालाजार भारत",
    "filariasis india", "फाइलेरिया भारत"
]
max_per_query = 25

all_records = []

for q in queries:
    print(f"\nSearching for: {q}")
    try:
        videosSearch = VideosSearch(q, limit=max_per_query)
        results = videosSearch.result().get('result', [])
        for v in results:
            url = v['link']
            title = v['title']
            published = v.get('publishedTime', '')
            views = v.get('viewCount', {}).get('short', '')
            all_records.append({
                "query": q,
                "title": title,
                "url": url,
                "published": published,
                "views": views
            })
    except Exception as e:
        print(f"  Skipping '{q}' due to error: {e}")

df = pd.DataFrame(all_records).drop_duplicates(subset=["url"])
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/youtube_links.csv", index=False)

print(f"\nSaved {len(df)} unique YouTube links to data/raw/youtube_links.csv")
