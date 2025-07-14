# scripts/plot_bubble_map_attention_burden.py

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load India shapefile you downloaded (adjust path if needed)
shapefile_path = "data/india/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
world = gpd.read_file(shapefile_path)

# Filter for India
india = world[world["ADMIN"] == "India"]

# Your data
df = pd.DataFrame({
    "Disease": ["Dengue", "Chikungunya", "Filariasis", "Kala-azar"],
    "Mean Burden": [163679, 13875, 3060, 1359],
    "Total Attention": [173, 46, 106, 0],
    "Latitude": [23.5, 13, 19, 25],
    "Longitude": [78, 80, 85, 85]
})

# Plot
fig, ax = plt.subplots(1, 1, figsize=(9, 10))
india.boundary.plot(ax=ax, color="black", linewidth=0.8)

# Bubble size scaling (increase this value to enlarge circles)
size_scale = 0.01

# Bubble colors by attention
# Bubble colors by attention
scatter = ax.scatter(
    df["Longitude"],
    df["Latitude"],
    s=df["Mean Burden"] * size_scale,
    c=df["Total Attention"],
    cmap="viridis",   # <-- or whichever colormap you prefer
    edgecolors="black",
    alpha=0.85
)


# Annotate each point
for i, row in df.iterrows():
    ax.annotate(
        row["Disease"],
        xy=(row["Longitude"], row["Latitude"]),
        xytext=(3, 3),
        textcoords="offset points",
        fontsize=11,
        fontweight="bold"
    )

# Title mentioning all four NTDs
plt.title(
    "Burden and Online Attention of Four NTDs in India:\n"
    "Dengue, Chikungunya, Filariasis, and Kala-azar",
    fontsize=14,
    fontweight="bold",
    pad=20
)

# Colorbar for attention
cbar = plt.colorbar(scatter, ax=ax, shrink=0.7)
cbar.set_label("Total Online Attention (Mentions)")

ax.axis("off")
plt.tight_layout()
plt.savefig("output/figures/ntd_bubble_map_polished.png", dpi=300)
plt.show()
