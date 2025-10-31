import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Read the CSV file
df = pd.read_csv('combined-peak-area-distribution.csv')

# Clean columns
df.columns = df.columns.str.strip()

# Define colors for each condition
colors = {
    'Unmineralized biofilm': '#EF8E2D',
    'LabMAOM': '#A8604A'
}

# Define glycerol order
glycerol_order = [0.5, 1, 2, 5]

# Map Glycerol % to fixed x positions
x_positions = {val: i for i, val in enumerate(glycerol_order)}

# Plot setup
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_box_aspect(1)
fig.patch.set_alpha(0)

# Plot points for each condition
for condition in df['Condition'].unique():
    condition_data = df[df['Condition'] == condition]
    x_vals = [x_positions[val] for val in condition_data['Glycerol %']]
    ax.scatter(x_vals, condition_data['O-alkyl/Carbonyl'],
               color=colors[condition], alpha=1,
               s=80, edgecolor='black', linewidth=1.2, zorder=2)

# Axis labels and ticks
ax.set_xticks(list(x_positions.values()))
ax.set_xticklabels([f"{val}%" for val in glycerol_order],
                   fontsize=16, fontname='Arial', style='italic')
ax.set_xlabel('Glycerol %', fontsize=16, fontname='Arial', style='italic')
ax.set_ylabel('O-alkyl/Carbonyl', fontsize=16, fontname='Arial', style='italic')
ax.tick_params(labelsize=12)

# Grid
ax.grid(True, alpha=0.2)

# Set y-axis font
for label in ax.get_yticklabels():
    label.set_fontsize(14)
    label.set_fontname('Arial')

# Legend
legend_handles = [
    Patch(color=colors['Unmineralized biofilm'], label='Unmineralized biofilm'),
    Patch(color=colors['LabMAOM'], label='LabMAOM')
]
ax.legend(handles=legend_handles, loc='best', frameon=True,
          prop={'family': 'Arial', 'style': 'italic', 'size': 12})

plt.savefig("O-alkyl-Carbonyl_ratio.png", dpi=300, transparent=True)
plt.show()