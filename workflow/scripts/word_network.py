import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations

# Manual shortlist of domain terms
manual_terms = [
    'dengue', 'fever', 'filariasis', 'lymphatic', 'lymphoedema', 'patients',
    'treatment', 'integrative', 'condition', 'limb', 'swelling', 'hospital', 'medicine'
]

df = pd.read_csv("data/clean/youtube_comments_clean.csv")
texts = [t.split() for t in df['clean_text'].dropna()]

edges = Counter()
for text in texts:
    words_in_text = [w for w in set(text) if w in manual_terms]
    for pair in combinations(words_in_text, 2):
        edges[tuple(sorted(pair))] += 1

# Only keep edges with at least 2 co-occurrences
edges = {k: v for k, v in edges.items() if v >= 2}

# Build graph
G = nx.Graph()
for (w1, w2), count in edges.items():
    G.add_edge(w1, w2, weight=count)

# Remove isolated nodes
G.remove_nodes_from(list(nx.isolates(G)))

if len(G.nodes) == 0:
    print("No strong co-occurrences between your hand-picked terms. Try lowering the cutoff or revising the manual_terms list.")
else:
    # Community coloring (greedy modularity, always works)
    from networkx.algorithms import community as nx_comm
    comms = nx_comm.greedy_modularity_communities(G)
    node_color_map = {}
    for i, com in enumerate(comms):
        for node in com:
            node_color_map[node] = i
    node_colors = [node_color_map.get(node, 0) for node in G.nodes()]

    # ... [all your code above remains the same] ...

plt.figure(figsize=(9, 9))
pos = nx.spring_layout(G, k=1.2, seed=21)
cmap = plt.cm.Set1

# Nodes
nx.draw_networkx_nodes(
    G, pos, node_size=2800, cmap=cmap, node_color=node_colors,
    linewidths=2.8, edgecolors="black", alpha=0.92
)
# Edges: now always thick enough to see!
max_weight = max([G[u][v]['weight'] for u, v in G.edges()])
min_width = 3  # try 3-5 for publication
nx.draw_networkx_edges(
    G, pos,
    width=[max(min_width, 5 * G[u][v]['weight'] / max_weight) for u, v in G.edges()],
    alpha=0.92, edge_color="black"
)
# Labels
nx.draw_networkx_labels(G, pos, font_size=20, font_weight='bold')

edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges() if G[u][v]['weight'] >= 6}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=14, font_color="brown")

plt.title("Key Medical Term Co-occurrence Network (YouTube NTD Comments)", fontsize=17, pad=18)
plt.axis('off')
plt.tight_layout()
plt.savefig("output/figures/yt_word_network_pub.png", dpi=400)
plt.show()
