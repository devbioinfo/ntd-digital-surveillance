# scripts/generate_attention_table.py

import pandas as pd

# 1. Load your cleaned data
df_yt   = pd.read_csv('data/clean/youtube_comments_clean.csv')
df_news = pd.read_csv('data/clean/google_news_clean.csv')

# 2. Define the disease keywords
diseases = ['dengue', 'chikungunya', 'kala-azar', 'filariasis']

# 3. Count mentions per platform
rows = []
for d in diseases:
    rows.append({
        'Disease': d.replace('-', ' ').title(),
        'YouTube Mentions':   int(df_yt['clean_text'].str.contains(d, case=False, na=False).sum()),
        'Google News Mentions': int(df_news['clean_title'].str.contains(d, case=False, na=False).sum())
    })

df_attention = pd.DataFrame(rows)

# 4. Save and print
df_attention.to_csv('data/clean/ntd_attention_table.csv', index=False)
print(df_attention)
