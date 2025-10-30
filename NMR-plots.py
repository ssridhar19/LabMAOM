import pandas as pd
import matplotlib.pyplot as plt

# Load clean data
xlsx_path = "combined-spectra-all.xlsx"
df_plot = pd.read_excel(xlsx_path, sheet_name='plot-data')

# Extract x data (measurements were conducted at different times, so x axis
# is different for some samples)
x_left = df_plot['δ [ppm]']
x_right = df_plot['δ [ppm].1']

# Define y columns
biofilm_cols = ['5 % biofilm', '2 % biofilm', '1 % biofilm', '0.5 %  biofilm']
mineral_cols = ['5 % mineral', '2 % mineral', '1 % mineral', '0.5 % mineral']

# Assign colors
biofilm_colors = ['#8c6515', '#b07c1e', '#c48a27', '#d8a03d']
mineral_colors = ['#000000', '#1f1400', '#3c2a00', '#5a3b00']

# Calculate a dynamic offset to fully separate spectra
max_signal = max(df_plot[mineral_cols + biofilm_cols].max())
offset_step = 0.8 * max_signal

# Finalize figure size
figsize = (6, 5)

# === Plot 1: Mineral Spectra ===
fig, ax = plt.subplots(figsize=figsize)

for idx, col in enumerate(mineral_cols):
    y = df_plot[col] + idx * offset_step
    ax.plot(x_right, y, color=mineral_colors[idx], linewidth=1.5)

ax.invert_xaxis()
ax.set_xlabel('δ [ppm]', fontname='Arial', fontsize=12, fontstyle='italic')

ax.set_yticks([])  # remove y-axis
# ax.set_title('Mineral Spectra')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(direction='out', left=False)

for label in ax.get_xticklabels():
    label.set_fontname('Arial')
    label.set_fontsize(10)
    label.set_fontstyle('italic') 

plt.tight_layout()
plt.savefig("mineral_spectra_stacked.pdf", dpi=600, transparent=True)
plt.savefig("mineral_spectra_stacked.eps", format='eps', transparent=True)
plt.show()

# === Plot 2: Biofilm Spectra ===
fig, ax = plt.subplots(figsize=figsize)

for idx, col in enumerate(biofilm_cols):
    y = df_plot[col] + idx * offset_step
    ax.plot(x_left, y, color=biofilm_colors[idx], linewidth=1.5)

ax.invert_xaxis()
ax.set_xlabel('δ [ppm]', fontname='Arial', fontsize=12, fontstyle='italic')

ax.set_yticks([])  # remove y-axis
# ax.set_title('Biofilm Spectra')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(direction='out', left=False)

for label in ax.get_xticklabels():
    label.set_fontname('Arial')
    label.set_fontsize(10)
    label.set_fontstyle('italic') 

plt.tight_layout()
plt.savefig("biofilm_spectra_stacked.pdf", dpi=600, transparent=True)
plt.savefig("biofilm_spectra_stacked.eps", format='eps', transparent=True)
plt.show()
