# scripts/facebook_mobile_scraper.py

import os, time, requests
from bs4 import BeautifulSoup
import pandas as pd

# Public page handles (mobile site)
pages = ["MoHFWIndia", "WHOIndia"]
# NTD terms to filter in the posts
terms = ["dengue", "chikungunya", "kala-azar", "filariasis"]

# A desktop‐style User-Agent often works best
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

records = []

for page in pages:
    print(f"\nScraping Facebook (mobile) page: {page}")
    url = f"https://m.facebook.com/{page}/"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f" → Failed to load {url} (status {resp.status_code})")
        continue

    soup = BeautifulSoup(resp.text, "html.parser")
    # On m.facebook.com, posts are in <div class="story_body_container">
    containers = soup.find_all("div", class_="story_body_container")
    print(f" → Found {len(containers)} posts on first screen")

    for div in containers:
        text = div.get_text(separator=" ", strip=True)
        lower = text.lower()
        for term in terms:
            if term in lower:
                # Attempt to find a timestamp (in a <abbr> tag just before)
                abbr = div.find_previous("abbr")
                ts = abbr.text if abbr else None
                records.append({
                    "page": page,
                    "time": ts,
                    "text": text,
                    "term": term
                })
    # Be polite
    time.sleep(2)

# Save results
df = pd.DataFrame(records)
os.makedirs("data/raw", exist_ok=True)
out_path = "data/raw/facebook_posts.csv"
df.to_csv(out_path, index=False)
print(f"\nSaved {len(df)} posts → {out_path}")
