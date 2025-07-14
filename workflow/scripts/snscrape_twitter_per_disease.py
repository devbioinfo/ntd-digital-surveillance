import time
import random
# … (other imports)

def main():
    # … (setup code)

    for disease, keyword in disease_keywords.items():
        print(f"\n=== Scraping: {disease} ===")
        for since, until in generate_date_ranges(start_date, end_date, days=30):
            query = f"{keyword} since:{since} until:{until} lang:en"
            for attempt in (1,2):
                print(f"Window {since}→{until} (attempt {attempt}) …", end=" ", flush=True)
                try:
                    df = scrape_chunk(query, max_per_chunk=2000)
                    df["disease"] = disease
                    print(f"{len(df)} tweets")
                    all_dfs.append(df)
                    break
                except Exception as e:
                    msg = str(e)
                    if "429" in msg and attempt == 1:
                        wait = 300  # 5 min
                        print(f"Rate-limited, sleeping {wait//60} min…")
                        time.sleep(wait)
                    else:
                        print(f"Skipping window ({msg})")
                        break
            # polite pause before next window
            pause = 30 + random.random()*10
            time.sleep(pause)
