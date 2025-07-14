import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter
from scipy import stats

# Load data
df = pd.read_csv('data/clean/ntd_burden_attention_final.csv')

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

# Scatter each point individually
for _, row in df.iterrows():
    ax.scatter(
        row['Mean Burden'],
        row['Total Attention'],
        s=180,
        color=colors[row['Disease']],
        marker=markers[row['Disease']],
        edgecolor='black',
        alpha=0.9,
        label=row['Disease']
    )
    # Arrow annotation
    ax.annotate(
        row['Disease'],
        xy=(row['Mean Burden'], row['Total Attention']),
        xytext=(row['Mean Burden']*1.2, row['Total Attention']*1.4),
        fontsize=12,
        weight='bold',
        arrowprops=dict(arrowstyle="->", color=colors[row['Disease']])
    )

# Log-log regression with confidence interval
x = df['Mean Burden']
y = df['Total Attention']
mask = (x > 0) & (y > 0)

log_x = np.log10(x[mask])
log_y = np.log10(y[mask])

slope, intercept, r_value, p_value, std_err = stats.linregress(log_x, log_y)
x_fit = np.linspace(log_x.min(), log_x.max(), 100)
y_fit = slope * x_fit + intercept

# 95% confidence interval
ci = 1.96 * std_err
y_upper = y_fit + ci
y_lower = y_fit - ci

ax.plot(10**x_fit, 10**y_fit, color='gray', linestyle='--', label='Log-log trend')
ax.fill_between(
    10**x_fit,
    10**y_lower,
    10**y_upper,
    color='gray',
    alpha=0.2,
    label='95% CI'
)

# Log scales
ax.set_xscale('log')
ax.set_yscale('log')

# Labels and title
ax.set_xlabel("Mean Annual Burden (2019–2023)", fontsize=14)
ax.set_ylabel("Total Online Attention (Mentions)", fontsize=14)
ax.set_title("Attention vs. Mean Burden for NTDs in India", fontsize=16, weight='bold')

# Ticks
ax.xaxis.set_major_formatter(ScalarFormatter())
ax.yaxis.set_major_formatter(ScalarFormatter())

# Grid
ax.grid(True, which="both", linestyle="--", alpha=0.4)

# Legend
ax.legend(frameon=True, fontsize=11)

# Tight layout
plt.tight_layout()

# Save PNG
plt.savefig("output/figures/attention_vs_burden_plos_final.png", dpi=300)

# Save vector PDF
plt.savefig("output/figures/attention_vs_burden_plos_final.pdf")

# Save high-res TIFF
plt.savefig("output/figures/attention_vs_burden_plos_final.tiff", dpi=600)

# Show
plt.show()
