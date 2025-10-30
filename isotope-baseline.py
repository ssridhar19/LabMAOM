import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_excel("isotope-data.xlsx", sheet_name='plot-data')

# Define custom color palette for scatter points only
palette = {
    "Unmineralized B. subtilis biofilm": "#EF8E2D",
    "LabMAOM": "#A8604A",
}

# Prepare square figure
fig, ax = plt.subplots()
fig.set_size_inches(6, 6)

# Plot settings
categories = df.columns
x_pos = np.arange(len(categories))

for i, col in enumerate(categories):
    y = df[col].dropna().values
    x = np.full_like(y, x_pos[i], dtype=float)

    color = palette.get(col, 'gray')

    # Mean and std
    mean = np.mean(y)
    std = np.std(y)

    # Vertical error bar (mean ± std)
    ax.vlines(x_pos[i], mean - std, mean + std, color='gray', linewidth=1, zorder=1)

    # Whiskers (horizontal caps)
    cap_width = 0.2  # controls whisker width
    ax.hlines(mean + std, x_pos[i] - cap_width, x_pos[i] + cap_width, color='gray', linewidth=1, zorder=1)
    ax.hlines(mean - std, x_pos[i] - cap_width, x_pos[i] + cap_width, color='gray', linewidth=1, zorder=1)

    # Optional: horizontal tick at the mean
    ax.hlines(mean, x_pos[i] - cap_width, x_pos[i] + cap_width, color='gray', linewidth=1, zorder=1)

    # Scatter points
    ax.scatter(x, y, s=64, edgecolor='black', facecolor=color, linewidth=1, zorder=2)

# Horizontal reference lines
ax.axhline(-19.9, color='gray', linestyle='--', linewidth=1.5, zorder=0)
ax.axhline(-30.5, color='gray', linestyle='--', linewidth=1.5, zorder=0)

# Add labels for those lines
ax.text(len(categories) - 1.3, -19.9 + 0.2, 'LB = -19.9 ‰', color='gray',
        fontsize=14, fontname='Arial', verticalalignment='bottom')

ax.text(len(categories) - 1.3, -30.5 + 0.2, 'MSgg = -30.5 ‰', color='gray',
        fontsize=14, fontname='Arial', verticalalignment='bottom')

# --- Notes ---
# len(categories) - 1.3 positions the label inside the plot
# + 0.2 lifts the label slightly above the line
# verticalalignment='bottom' ensures the label sits on top of the line

# Axis labels and formatting
ax.set_xticks(x_pos)
ax.set_xticklabels(
    categories,
    rotation=15,
    fontsize=14,
    fontname='Arial',
    style='italic'
)
ax.set_yticks(ax.get_yticks())  # Just to apply font settings
ax.set_yticklabels([f"{tick:.1f}" for tick in ax.get_yticks()], fontsize=14, fontname='Arial')

ax.set_ylabel("δ¹³C (‰ vs std)", fontsize=14, fontname='Arial')
ax.set_xlim(-0.5, len(categories) - 0.5)
ax.set_frame_on(True)

# Layout
plt.tight_layout()
plt.savefig("isotope-baseline.png", dpi=300, transparent=True)

