# scripts/plot_sentiment_by_topic.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Read the data
df = pd.read_csv('output/figures/sentiment_by_topic_platform.csv')

# Melt for plotting
df_melted = df.melt(id_vars=["Platform", "Topic", "Theme"],
                    value_vars=["Positive", "Neutral", "Negative"],
                    var_name="Sentiment", value_name="Percent")

# Sort by Platform/Topic
df_melted['TopicLabel'] = df_melted['Platform'] + " T" + df_melted['Topic'].astype(str)

# Set style for publication
sns.set(style="whitegrid", font_scale=1.2)
plt.figure(figsize=(10, 6))

# Make grouped barplot
ax = sns.barplot(
    data=df_melted,
    x="TopicLabel",
    y="Percent",
    hue="Sentiment",
    palette=["#4CAF50", "#FFC107", "#F44336"]
)

# Annotate bars
for c in ax.containers:
    ax.bar_label(c, fmt='%.1f', label_type="edge", padding=2)

plt.ylabel("Percentage (%)")
plt.xlabel("Platform & Topic")
plt.title("Sentiment Distribution by Topic and Platform")
plt.legend(title="Sentiment", loc='upper right')
plt.tight_layout()
plt.savefig("output/figures/sentiment_by_topic_platform.png", dpi=300)
plt.show()
