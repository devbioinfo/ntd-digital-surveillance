# scripts/run_all_pipeline.py

import os
import re
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

os.makedirs("data/clean", exist_ok=True)
os.makedirs("data/sentiment", exist_ok=True)
os.makedirs("output/figures", exist_ok=True)

######################
# 1. CLEANING
######################
def clean_text(text):
    text = str(text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = text.strip().lower()
    return text

# --- YouTube ---
df_yt = pd.read_csv('data/raw/youtube_comments.csv')
df_yt = df_yt.drop_duplicates(subset=["text"])
df_yt['clean_text'] = df_yt['text'].apply(clean_text)
df_yt.to_csv('data/clean/youtube_comments_clean.csv', index=False)

# --- Google News ---
df_news = pd.read_csv('data/raw/google_news.csv')
df_news = df_news.drop_duplicates(subset=["title", "snippet"])
df_news['clean_title'] = df_news['title'].apply(clean_text)
df_news['clean_snippet'] = df_news['snippet'].apply(clean_text)
df_news.to_csv('data/clean/google_news_clean.csv', index=False)

print("Step 1/4: Data cleaned and saved.")

######################
# 2. SENTIMENT ANALYSIS
######################
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = analyzer.polarity_scores(str(text))
    if score['compound'] >= 0.05:
        return 'positive'
    elif score['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

# --- YouTube ---
df_yt['sentiment'] = df_yt['clean_text'].apply(get_sentiment)
df_yt.to_csv('data/sentiment/youtube_sentiment.csv', index=False)

# --- News (headline & snippet) ---
df_news['title_sentiment'] = df_news['clean_title'].apply(get_sentiment)
df_news['snippet_sentiment'] = df_news['clean_snippet'].apply(get_sentiment)
df_news.to_csv('data/sentiment/news_sentiment.csv', index=False)

print("Step 2/4: Sentiment analysis complete.")

######################
# 3. WORDCLOUDS
######################
# --- YouTube ---
yt_text = " ".join(df_yt['clean_text'].astype(str).tolist())
yt_wc = WordCloud(width=800, height=400, background_color='white').generate(yt_text)
plt.figure(figsize=(12,6))
plt.imshow(yt_wc, interpolation='bilinear')
plt.axis('off')
plt.tight_layout()
plt.savefig("output/figures/youtube_wordcloud.png")
plt.close()

# --- News ---
news_text = " ".join(df_news['clean_title'].astype(str).tolist())
news_wc = WordCloud(width=800, height=400, background_color='white').generate(news_text)
plt.figure(figsize=(12,6))
plt.imshow(news_wc, interpolation='bilinear')
plt.axis('off')
plt.tight_layout()
plt.savefig("output/figures/news_wordcloud.png")
plt.close()

print("Step 3/4: Wordclouds generated.")

######################
# 4. SENTIMENT PIE CHARTS
######################
# --- YouTube ---
yt_counts = df_yt['sentiment'].value_counts()
plt.figure(figsize=(6,6))
yt_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#99ff99','#ff9999'])
plt.ylabel('')
plt.title('YouTube Comments Sentiment Distribution')
plt.savefig("output/figures/youtube_sentiment_pie.png")
plt.close()

# --- News (headline sentiment) ---
news_counts = df_news['title_sentiment'].value_counts()
plt.figure(figsize=(6,6))
news_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#99ff99','#ff9999'])
plt.ylabel('')
plt.title('Google News Headline Sentiment Distribution')
plt.savefig("output/figures/news_sentiment_pie.png")
plt.close()

print("Step 4/4: Sentiment pie charts created.")

######################
print("\nPipeline complete! Check these folders:")
print("  Cleaned data:      data/clean/")
print("  Sentiment CSVs:    data/sentiment/")
print("  All figures:       output/figures/")
