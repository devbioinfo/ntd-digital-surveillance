import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter
from scipy import stats

# Load data
df = pd.read_csv('data/clean/ntd_burden_attention_final.csv')

# Configure default font
plt.rcParams["font.family"] = "Arial"
plt.rcParams["axes.titlesize"] = 18
plt.rcParams["axes.labelsize"] = 16
plt.rcParams["legend.fontsize"] = 13
plt.rcParams["xtick.labelsize"] = 13
plt.rcParams["ytick.labelsize"] = 13

# Prepare figure
fig, ax = plt.subplots(figsize=(8,6))

# Colorblind-friendly colors
colors = {
    'Dengue': '#0072B2',
    'Chikungunya': '#E69F00',
    'Filariasis': '#009E73',
    'Kala-azar': '#D55E00'
}

# Unique markers
markers = {
    'Dengue': 'o',
    'Chikungunya': 's',
    'Filariasis': 'D',
    'Kala-azar': '^'
}

# Scatter points with transparency
for _, row in df.iterrows():
    ax.scatter(
        row['Mean Burden'],
        row['Total Attention'],
        s=200,
        color=colors[row['Disease']],
        marker=markers[row['Disease']],
        edgecolor='black',
        alpha=0.85,
        label=row['Disease']
    )
    ax.annotate(
        row['Disease'],
        xy=(row['Mean Burden'], row['Total Attention']),
        xytext=(row['Mean Burden']*1.25, row['Total Attention']*1.3),
        fontsize=13,
        weight='bold',
        arrowprops=dict(arrowstyle="->", color=colors[row['Disease']], lw=1.5)
    )

# Regression (log-log)
x = df['Mean Burden']
y = df['Total Attention']
mask = (x > 0) & (y > 0)

log_x = np.log10(x[mask])
log_y = np.log10(y[mask])

slope, intercept, r_value, p_value, std_err = stats.linregress(log_x, log_y)
x_fit = np.linspace(log_x.min(), log_x.max(), 100)
y_fit = slope * x_fit + intercept

ci = 1.96 * std_err
y_upper = y_fit + ci
y_lower = y_fit - ci

ax.plot(10**x_fit, 10**y_fit, color='gray', linestyle='--', lw=2, label='Log–log trend')
ax.fill_between(
    10**x_fit,
    10**y_lower,
    10**y_upper,
    color='gray',
    alpha=0.15,
    label='95% CI'
)

# Annotate R²
ax.text(
    0.05, 0.95,
    f"$R^2$ = {r_value**2:.2f}",
    transform=ax.transAxes,
    fontsize=14,
    verticalalignment='top',
    bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='gray')
)

# Log scales
ax.set_xscale('log')
ax.set_yscale('log')

# Labels and title
ax.set_xlabel("Mean Annual Burden (2019–2023)", fontsize=16)
ax.set_ylabel("Total Online Attention (Mentions)", fontsize=16)
ax.set_title("Attention vs. Mean Burden for NTDs in India", fontsize=18, weight='bold')

# Remove grid
ax.grid(False)

# Legend (outside)
ax.legend(
    frameon=False,
    bbox_to_anchor=(1.05, 1),
    loc='upper left'
)

# Ticks formatting
ax.xaxis.set_major_formatter(ScalarFormatter())
ax.yaxis.set_major_formatter(ScalarFormatter())

# Tight layout
plt.tight_layout()

# Save high-res files
plt.savefig("output/figures/attention_vs_burden_plos_final2.png", dpi=300)
plt.savefig("output/figures/attention_vs_burden_plos_final2.pdf")
plt.savefig("output/figures/attention_vs_burden_plos_final2.eps")  # EPS for journal submission

# Show
plt.show()
