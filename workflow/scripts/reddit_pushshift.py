# scripts/reddit_pushshift.py

import os, time
import requests
import pandas as pd
from datetime import datetime, timedelta

# Keywords to search (in title/selftext)
terms = ["dengue","chikungunya","kala-azar","filariasis"]
# Subreddits to scan
subreddits = ["india","health","publichealth"]  

def fetch_chunk(sub, term, after_ts, before_ts, size=500):
    url = "https://api.pushshift.io/reddit/search/submission/"
    params = {
        "subreddit": sub,
        "q": term,
        "after": after_ts,
        "before": before_ts,
        "size": size
    }
    resp = requests.get(url, params=params).json()
    return pd.DataFrame(resp.get("data", []))

def main():
    start = datetime(2019,1,1)
    end   = datetime(2024,5,31)
    all_posts = []

    for term in terms:
        print(f"\n--- Reddit term: {term} ---")
        cur = start
        while cur < end:
            nxt = min(cur + timedelta(days=30), end)
            df = fetch_chunk(
                sub="india", 
                term=term, 
                after_ts=int(cur.timestamp()), 
                before_ts=int(nxt.timestamp()), 
                size=500
            )
            df["term"] = term
            print(f"{cur.date()} → {nxt.date()}: {len(df)} posts")
            all_posts.append(df)
            cur = nxt
            time.sleep(1)  # be polite

    result = pd.concat(all_posts, ignore_index=True) if all_posts else pd.DataFrame()
    os.makedirs("data/raw", exist_ok=True)
    result.to_csv("data/raw/reddit_posts.csv", index=False)
    print(f"\nSaved {len(result)} Reddit posts → data/raw/reddit_posts.csv")

if __name__ == "__main__":
    main()
