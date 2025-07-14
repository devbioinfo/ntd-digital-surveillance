# scripts/youtube_comments.py

import os
import pandas as pd
from youtube_comment_downloader import YoutubeCommentDownloader

# Load video URLs from the CSV file
videos = pd.read_csv("data/raw/youtube_links.csv")["url"].tolist()

# Keywords to match in comments (case-insensitive)
terms = ["dengue", "chikungunya", "kala-azar", "filariasis"]

downloader = YoutubeCommentDownloader()

def main():
    records = []
    for url in videos:
        print(f"\nScraping comments from {url}")
        try:
            for c in downloader.get_comments_from_url(url):
                txt = c["text"].lower()
                for term in terms:
                    if term in txt:
                        records.append({
                            "video": url,
                            "time": c.get("time"),
                            "text": c["text"],
                            "likes": c.get("likes"),
                            "term": term
                        })
        except Exception as e:
            print(f"  Error scraping {url}: {e}")

    df = pd.DataFrame(records)
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/youtube_comments.csv", index=False)
    print(f"\nSaved {len(df)} comments → data/raw/youtube_comments.csv")

if __name__ == "__main__":
    main()
