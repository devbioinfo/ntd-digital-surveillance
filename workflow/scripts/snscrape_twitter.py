# scripts/snscrape_twitter.py

import os
import pandas as pd
import snscrape.modules.twitter as sntwitter
from keywords import keywords
from datetime import datetime, timedelta

def generate_date_ranges(start, end, days=30):
    """
    Yield (since_date, until_date) strings, stepping by 'days' each time.
    """
    current = start
    while current < end:
        next_day = current + timedelta(days=days)
        if next_day > end:
            next_day = end
        yield current.strftime("%Y-%m-%d"), next_day.strftime("%Y-%m-%d")
        current = next_day

def build_query(terms, since, until):
    """
    Build a snscrape query with OR’d terms, date range, and English filter.
    """
    # Wrap multi-word terms in quotes
    quoted = [f'"{t}"' if " " in t else t for t in terms]
    term_query = " OR ".join(quoted)
    return f"({term_query}) since:{since} until:{until} lang:en"

def scrape_chunk(query, max_per_chunk=50000):
    """
    Scrape up to max_per_chunk tweets for a single query.
    Returns a DataFrame.
    """
    rows = []
    scraper = sntwitter.TwitterSearchScraper(query)
    for i, tweet in enumerate(scraper.get_items()):
        if i >= max_per_chunk:
            break
        rows.append({
            "id": tweet.id,
            "date": tweet.date,
            "user": tweet.user.username,
            "text": tweet.content,
            "lang": tweet.lang,
            "replyCount": tweet.replyCount,
            "retweetCount": tweet.retweetCount,
            "likeCount": tweet.likeCount,
            "quoteCount": tweet.quoteCount
        })
    return pd.DataFrame(rows)

def main():
    # Flatten all keyword terms into a single list
    flat_terms = [term for terms in keywords.values() for term in terms]

    # Define overall date span
    start_date = datetime(2019, 1, 1)
    end_date   = datetime(2024, 5, 31)

    # Container for per-chunk DataFrames
    all_dfs = []

    for since, until in generate_date_ranges(start_date, end_date, days=30):
        query = build_query(flat_terms, since, until)
        print(f"Scraping tweets from {since} to {until}…")

        try:
            df_chunk = scrape_chunk(query, max_per_chunk=50000)
            print(f" → Retrieved {len(df_chunk)} tweets")
            all_dfs.append(df_chunk)
        except Exception as e:
            print(f" ** Skipping window {since} → {until} due to error: {e}")

    # Concatenate all chunks
    if all_dfs:
        full_df = pd.concat(all_dfs, ignore_index=True)
    else:
        full_df = pd.DataFrame()

    # Save results
    os.makedirs("data/raw", exist_ok=True)
    out_path = "data/raw/twitter_scraped.csv"
    full_df.to_csv(out_path, index=False)
    print(f"\nFinished! Total tweets collected: {len(full_df)}")
    print(f"Saved to {out_path}")

if __name__ == "__main__":
    main()
