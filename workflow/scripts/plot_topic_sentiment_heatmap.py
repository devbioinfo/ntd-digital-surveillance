# scripts/plot_topic_sentiment_heatmap.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Example data (use your actual numbers)
data = {
    ("YouTube", "1"): {"Positive": 45, "Neutral": 35, "Negative": 20},
    ("YouTube", "2"): {"Positive": 50, "Neutral": 50, "Negative": 0},
    ("Google News", "1"): {"Positive": 22.4, "Neutral": 54.9, "Negative": 22.8},
    ("Google News", "2"): {"Positive": 22.2, "Neutral": 50.0, "Negative": 27.8},
    ("Google News", "3"): {"Positive": 0, "Neutral": 100, "Negative": 0},
}

# Flatten for DataFrame
records = []
for (platform, topic), sent_dict in data.items():
    for sentiment, value in sent_dict.items():
        records.append({"Platform": platform, "Topic": topic, "Sentiment": sentiment, "Percent": value})

df = pd.DataFrame(records)
heatmap_df = df.pivot_table(index=["Platform", "Topic"], columns="Sentiment", values="Percent")

plt.figure(figsize=(8, 4))
sns.heatmap(
    heatmap_df,
    annot=True, fmt=".1f", cmap="YlGnBu",
    cbar_kws={'label': 'Percent (%)'}
)
plt.title("Sentiment Distribution Across Topics and Platforms")
plt.ylabel("Platform & Topic")
plt.tight_layout()
plt.savefig("output/figures/topic_sentiment_heatmap.png", dpi=300)
plt.show()
