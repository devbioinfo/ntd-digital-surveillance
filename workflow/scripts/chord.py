import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import random

# Load comments
df = pd.read_csv('data/clean/youtube_comments_clean.csv')

# If you *don't* have a user column, mock some:
if 'user' not in df.columns:
    df['user'] = ['user' + str(random.randint(1,30)) for _ in range(len(df))]

topics = ['dengue', 'filariasis', 'chikungunya', 'kala-azar']

# Build bipartite edges: (user, topic) if comment mentions topic
edges = []
for idx, row in df.iterrows():
    for topic in topics:
        if topic in row['clean_text']:
            edges.append( (row['user'], topic) )

# Build bipartite graph
B = nx.Graph()
B.add_nodes_from(df['user'].unique(), bipartite=0)
B.add_nodes_from(topics, bipartite=1)
B.add_edges_from(edges)

# Draw (project onto topic layer for clarity)
topic_nodes = [n for n in B.nodes if n in topics]
user_nodes = [n for n in B.nodes if n not in topics]

plt.figure(figsize=(11,8))
pos = nx.spring_layout(B, k=0.9, seed=42)
nx.draw_networkx_nodes(B, pos, nodelist=topic_nodes, node_color='red', node_size=1600, label='Topics')
nx.draw_networkx_nodes(B, pos, nodelist=user_nodes, node_color='skyblue', node_size=500, label='Users')
nx.draw_networkx_edges(B, pos, alpha=0.6)
nx.draw_networkx_labels(B, pos, font_size=11, font_weight='bold')
plt.title("Bipartite Network: YouTube Users and NTD Topics")
plt.legend()
plt.axis('off')
plt.tight_layout()
plt.savefig("output/figures/yt_bipartite_users_topics.png", dpi=350)
plt.show()
