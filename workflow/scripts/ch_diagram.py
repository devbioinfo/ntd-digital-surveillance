import pandas as pd
import plotly.graph_objects as go

# Define your keywords and platforms
keywords = ['dengue', 'filariasis', 'chikungunya', 'kala-azar']
platforms = ['YouTube', 'Google News']

# Load cleaned data
yt = pd.read_csv('data/clean/youtube_comments_clean.csv')
news = pd.read_csv('data/clean/google_news_clean.csv')

# Count keyword occurrences
yt_counts = [yt['clean_text'].str.contains(k, case=False).sum() for k in keywords]
news_counts = [news['clean_title'].str.contains(k, case=False).sum() for k in keywords]

# Create nodes and flows
labels = platforms + keywords
# Index: 0=YouTube, 1=News, 2-5=keywords
source = [0]*len(keywords) + [1]*len(keywords)
target = [2,3,4,5]*2
value  = yt_counts + news_counts

# Build Sankey
fig = go.Figure(go.Sankey(
    node = dict(
        pad=15, thickness=25,
        line=dict(color="black", width=0.5),
        label=labels,
        color=["#636EFA","#EF553B","#00CC96","#AB63FA","#FFA15A","#19D3F3"]
    ),
    link = dict(
        source=source,
        target=target,
        value=value,
        color=["rgba(99,110,250,0.5)"]*len(yt_counts) + ["rgba(239,85,59,0.5)"]*len(news_counts)
    )
))

fig.update_layout(
    title_text="NTD Keyword Attention Across Platforms (YouTube vs. Google News)",
    font_size=15
)
fig.write_image("output/figures/ntd_sankey_crossplatform.png", scale=2, width=900, height=600)
fig.show()
