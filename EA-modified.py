import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Load and clean data
df = pd.read_csv('plot-data-biofilm.csv')
df.columns = df.columns.str.strip()
df = df.dropna(subset=['Glycerol %'])

# Define glycerol order
glycerol_order = [0.5, 1, 2, 5]

# Grouped summary stats
summary_stats = df.groupby(['Glycerol %'], observed=False)['Ratio'].agg(['mean', 'std']).reset_index()

# Define color for the single condition
color = '#EF8E2D'

# Map Glycerol % to fixed x positions
x_positions = {val: i for i, val in enumerate(glycerol_order)}

# Plot setup
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_box_aspect(1)
fig.patch.set_alpha(0)

# Plot mean ± SD in gray (behind points)
x_vals = [x_positions[val] for val in summary_stats['Glycerol %']]
ax.errorbar(x_vals, summary_stats['mean'], yerr=summary_stats['std'],
            fmt='_', color='gray', markersize=8,
            capsize=4, capthick=1, elinewidth=1,
            zorder=1)

# Plot jittered points
jittered_x = [x_positions[val] + np.random.uniform(-0.1, 0.1) for val in df['Glycerol %']]
ax.scatter(jittered_x, df['Ratio'],
           color=color, alpha=1,
           s=80, edgecolor='black', linewidth=1.2, zorder=2)

# Axis labels and ticks
ax.set_xticks(list(x_positions.values()))
ax.set_xticklabels([f"{val}%" for val in glycerol_order],
                   fontsize=16, fontname='Arial', style='italic')
ax.set_ylabel('C:N ratio', fontsize=16, fontname='Arial', style='italic')
ax.tick_params(labelsize=12)

# Limits and grid
ax.set_ylim(0, 12)
ax.grid(True, alpha=0.2)

# Set y-axis font
for label in ax.get_yticklabels():
    label.set_fontsize(14)
    label.set_fontname('Arial')

# Legend
legend_handles = [
    Patch(color=color, label='Unmineralized B. subtilis biofilm')
]
ax.legend(handles=legend_handles, loc='lower right', frameon=True,
          prop={'family': 'Arial', 'style': 'italic', 'size': 12})

plt.savefig("CN_ratio-biofilm.png", dpi=300, transparent=True)
plt.show()
