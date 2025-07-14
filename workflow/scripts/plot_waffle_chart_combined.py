import pandas as pd
import matplotlib.pyplot as plt
from pywaffle import Waffle

# Data
data = {
    "Disease": ["Dengue", "Chikungunya", "Filariasis", "Kala-azar"],
    "Mean Burden": [163679, 13875, 3060, 1359],
    "Total Attention": [173, 46, 106, 0]
}
df = pd.DataFrame(data)

# Compute percentages
df["Burden %"] = df["Mean Burden"] / df["Mean Burden"].sum() * 100
df["Attention %"] = df["Total Attention"] / df["Total Attention"].sum() * 100

# Colors
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

# Create combined figure
fig = plt.figure(
    FigureClass=Waffle,
    plots={
        121: {   # subplot 1
            'values': df["Burden %"],
            'labels': [f"{d} ({p:.1f}%)" for d, p in zip(df["Disease"], df["Burden %"])],
            'legend': {'loc': 'upper left', 'bbox_to_anchor': (1.05, 1)},
            'title': {'label': 'Proportion of Total Disease Burden', 'loc': 'center'},
            'colors': colors
        },
        122: {   # subplot 2
            'values': df["Attention %"],
            'labels': [f"{d} ({p:.1f}%)" for d, p in zip(df["Disease"], df["Attention %"])],
            'title': {'label': 'Proportion of Total Online Attention', 'loc': 'center'},
            'colors': colors
        },
    },
    rows=10,
    figsize=(16, 6)
)

plt.tight_layout()
plt.savefig("output/figures/waffle_combined.png", dpi=300)
plt.show()
