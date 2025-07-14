import pandas as pd

# Define your keywords and platforms
keywords = ['dengue', 'filariasis', 'chikungunya', 'kala-azar']
platforms = ['YouTube', 'Google News']

# Load data
yt = pd.read_csv('data/clean/youtube_comments_clean.csv')
news = pd.read_csv('data/clean/google_news_clean.csv')

# Count occurrences for each keyword/platform
yt_counts = [yt['clean_text'].str.contains(k, case=False, na=False).sum() for k in keywords]
news_counts = [news['clean_title'].str.contains(k, case=False, na=False).sum() for k in keywords]

# Combine results
rows = []
for platform, counts in zip(platforms, [yt_counts, news_counts]):
    for k, c in zip(keywords, counts):
        rows.append({"Source": platform, "Target": k, "Value": c})

df_chord = pd.DataFrame(rows)
df_chord.to_csv("output/figures/ntd_platform_keywords.csv", index=False)
print(df_chord)
