import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

# Load data
df = pd.read_csv('data/clean/ntd_burden_attention_final.csv')

# Prepare figure
fig, ax = plt.subplots(figsize=(8,6))

# Colorblind-friendly palette
colors = {
    'Dengue': '#0072B2',
    'Chikungunya': '#E69F00',
    'Filariasis': '#009E73',
    'Kala-azar': '#D55E00'
}

# Scatter points
for _, row in df.iterrows():
    ax.scatter(
        row['Mean Burden'],
        row['Total Attention'],
        s=150,
        color=colors[row['Disease']],
        edgecolor='black',
        alpha=0.9,
        label=row['Disease']
    )
    ax.text(
        row['Mean Burden']*1.1,  # slightly offset x
        row['Total Attention']*1.1,  # slightly offset y
        row['Disease'],
        fontsize=11,
        weight='bold'
    )

# Optional: regression line (log-log)
x = df['Mean Burden']
y = df['Total Attention']
mask = (x > 0) & (y > 0)  # exclude zeros
log_x = np.log10(x[mask])
log_y = np.log10(y[mask])
slope, intercept = np.polyfit(log_x, log_y, 1)
x_fit = np.linspace(x.min(), x.max(), 100)
y_fit = 10 ** (intercept + slope * np.log10(x_fit))
ax.plot(x_fit, y_fit, color='gray', linestyle='--', label='Log-log trend')

# Log scales
ax.set_xscale('log')
ax.set_yscale('log')

# Axis labels and title
ax.set_xlabel("Mean Annual Burden (2019–2023)", fontsize=14)
ax.set_ylabel("Total Online Attention (Mentions)", fontsize=14)
ax.set_title("Attention vs. Mean Burden for NTDs in India", fontsize=16, weight='bold')

# Ticks formatting
ax.xaxis.set_major_formatter(ScalarFormatter())
ax.yaxis.set_major_formatter(ScalarFormatter())

# Grid
ax.grid(True, which="both", linestyle="--", alpha=0.4)

# Legend
ax.legend(frameon=True)

# Tight layout
plt.tight_layout()

# Save high-resolution PNG
plt.savefig("output/figures/attention_vs_burden_plos.png", dpi=300)

# Save vector PDF
plt.savefig("output/figures/attention_vs_burden_plos.pdf")

# Show
plt.show()
