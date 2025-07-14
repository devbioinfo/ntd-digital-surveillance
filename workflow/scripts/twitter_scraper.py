# scripts/twitter_scraper.py

import os
import pandas as pd
from dotenv import load_dotenv
import tweepy
from keywords import search_terms

def authenticate():
    load_dotenv()  # loads .env file
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        raise ValueError("Missing TWITTER_BEARER_TOKEN in .env")
    return tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

def fetch_tweets(client, query):
    tweets = []
    # Adjust max_results, start_time, end_time as needed
    for resp in client.search_all_tweets(
        query=query,
        tweet_fields=['created_at','lang','geo'],
        expansions=['geo.place_id'],
        max_results=500,
        start_time="2019-01-01T00:00:00Z",
        end_time="2024-05-31T23:59:59Z"
    ):
        for t in resp.data or []:
            tweets.append({
                "id": t.id,
                "text": t.text,
                "created_at": t.created_at,
                "lang": t.lang,
                "place_id": t.geo.get("place_id") if t.geo else None
            })
    return pd.DataFrame(tweets)

def main():
    client = authenticate()
    print("Fetching tweets…")
    df = fetch_tweets(client, search_terms)
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/twitter_posts.csv", index=False)
    print(f"Saved {len(df)} tweets to data/raw/twitter_posts.csv")

if __name__ == "__main__":
    main()

