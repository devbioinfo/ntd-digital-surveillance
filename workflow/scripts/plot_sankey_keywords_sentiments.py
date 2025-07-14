import pandas as pd
import plotly.graph_objects as go

# Load cleaned YouTube sentiment data
df = pd.read_csv("data/sentiment/youtube_sentiment.csv")

# List of keywords to check
keywords = ["dengue", "filariasis", "chikungunya", "kala"]

# Build counts of keyword -> sentiment
rows = []
for kw in keywords:
    for sentiment in ["positive", "neutral", "negative"]:
        count = df[
            df["clean_text"].str.contains(kw, case=False, na=False)
            & (df["sentiment"] == sentiment)
        ].shape[0]
        rows.append({"keyword": kw, "sentiment": sentiment, "count": count})

df_links = pd.DataFrame(rows)
df_links = df_links[df_links["count"] > 0]

# Nodes
all_keywords = df_links["keyword"].unique().tolist()
all_sentiments = df_links["sentiment"].unique().tolist()
nodes = all_keywords + all_sentiments
node_indices = {name: i for i, name in enumerate(nodes)}

# Sankey components
source = [node_indices[k] for k in df_links["keyword"]]
target = [node_indices[s] for s in df_links["sentiment"]]
value = df_links["count"]

# Custom node colors: richer, more distinct
node_colors = (
    ["#4c72b0", "#55a868", "#c44e52", "#8172b3"]  # 4 keyword colors
    + ["#117733", "#dd8452", "#cc6677"]           # 3 sentiment colors
)

# Custom link colors: solid, semi-transparent
sentiment_color_map = {
    "positive": "rgba(17,119,51,0.7)",   # deep green
    "neutral": "rgba(221,132,82,0.7)",   # warm brown-orange
    "negative": "rgba(204,102,119,0.7)"  # soft red
}
link_colors = [sentiment_color_map[s] for s in df_links["sentiment"]]

# Create figure
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,
        thickness=25,
        line=dict(color="black", width=0.7),
        label=nodes,
        color=node_colors,
        hovertemplate='%{label}<extra></extra>',
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=link_colors,
        hovertemplate='Count: %{value}<extra></extra>',
    )
)])

fig.update_layout(
    title_text="Keyword to Sentiment Sankey Diagram",
    title_font_size=20,
    font=dict(size=15),
    margin=dict(l=50, r=50, t=80, b=40),
    width=900,
    height=600
)

# Save interactive HTML
fig.write_html("output/figures/sankey_keywords_sentiment.html")
print("✅ HTML Sankey saved to output/figures/sankey_keywords_sentiment.html")

# Save high-res PNG
fig.write_image("output/figures/sankey_keywords_sentiment.png", scale=2)
print("✅ PNG Sankey saved to output/figures/sankey_keywords_sentiment.png")
