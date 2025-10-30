import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm

# Load data
file_path = "all-data.xlsx"
xls = pd.ExcelFile(file_path)
mm_data = xls.parse(xls.sheet_names[1]) # change for other sheets

conditions = mm_data.columns.tolist()
n_conditions = len(conditions)

palette = {
    "P. putida only": "gray",
    "P. putida + unmineralized B. subtilis biofilm": "#EF8E2D",
    "P. putida + LabMAOM": "#A8604A",
}

# Prepare jittered data points for scatter
scatter_x = []
scatter_y = []
scatter_colors = []
for i, col in enumerate(conditions):
    vals = mm_data[col].dropna().values
    jitter = np.random.normal(i, 0.1, size=len(vals))
    scatter_x.extend(jitter)
    scatter_y.extend(vals)
    scatter_colors.extend([palette[col]] * len(vals))

# Create square figure
fig, ax = plt.subplots(figsize=(6, 6))

elinewidth = 1  # thickness for error bars and mean line

# Plot mean ± SD first (behind points)
for i, col in enumerate(conditions):
    y = mm_data[col].dropna()
    mean = y.mean()
    std = y.std()

    # SD error bars
    ax.errorbar(
        i,
        mean,
        yerr=std,
        fmt='none',
        ecolor='gray',
        elinewidth=elinewidth,
        capsize=5,
        capthick=elinewidth,
        zorder=2  # behind points
    )
    # Shorter horizontal mean line
    ax.hlines(mean, i - 0.2, i + 0.2, colors='gray', linewidth=elinewidth, zorder=2)

# Plot scatter points last (on top)
ax.scatter(
    scatter_x,
    scatter_y,
    s=100,
    facecolors=scatter_colors,
    edgecolors='black',
    linewidth=1.5,
    zorder=3,
)

# Set axis limits tighter
ax.set_ylim(-25, -19)
ax.set_xlim(-0.6, n_conditions - 0.4)  # add extra spacing to avoid label collisions

# Clean wrapped x-axis labels for spacing
wrapped_labels = [
    "P. putida\nonly",
    "P. putida\n+ unmineralized\n B. subtilis biofilm",
    "P. putida\n+ LabMAOM"
]

# Italic Arial font, size 16
arial_italic = fm.FontProperties(family='Arial', style='italic', size=16)
ax.set_xticks(range(n_conditions))
ax.set_xticklabels(wrapped_labels, fontproperties=arial_italic)

# Set y tick labels font to Arial size 14
for label in ax.get_yticklabels():
    label.set_fontfamily('Arial')
    label.set_fontsize(14)

# Bigger y-axis label and title
ax.set_ylabel('', fontsize=16, fontname='Arial')
ax.set_title('MM Medium', fontsize=16, fontname='Arial')

# Disable ticks on top and right
ax.tick_params(top=False, right=False, labelsize=14)

# Optional: keep spines visible
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)

plt.tight_layout(pad=0.6)
plt.savefig("MM_medium.png", dpi=300, transparent=True)
plt.close()
