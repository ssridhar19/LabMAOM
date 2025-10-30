import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage import img_as_ubyte
from PIL import Image

# Load CSV matrices
mat_C = pd.read_csv("C.csv", header=0).to_numpy()
mat_Fe = pd.read_csv("Fe.csv", header=0).to_numpy()
mat_O = pd.read_csv("O.csv", header=0).to_numpy()

# Normalize
def normalize(mat):
    mat = mat - np.nanmin(mat)
    max_val = np.nanmax(mat)
    return mat / max_val if max_val > 0 else mat

C_norm = normalize(mat_C)
Fe_norm = normalize(mat_Fe)
O_norm = normalize(mat_O)

# RGB image
rgb = np.zeros((*C_norm.shape, 3), dtype=np.float32)
rgb[..., 0] = Fe_norm  # Red: Fe
rgb[..., 1] = C_norm   # Green: C
rgb[..., 2] = O_norm   # Blue: O

# Highlight Fe–C co-occurrence
threshold_Fe = 0.2
threshold_C = 0.2
cooccurrence_mask = (Fe_norm > threshold_Fe) & (C_norm > threshold_C)
rgb[cooccurrence_mask] = [1.0, 1.0, 0.0]  # Yellow

# Add alpha channel
alpha = np.where(np.sum(rgb, axis=-1) > 0, 1.0, 0.0)  # Fully transparent where all channels are 0
rgba = np.dstack((rgb, alpha))  # Shape: (H, W, 4)

# Convert to 8-bit
rgba_8bit = img_as_ubyte(rgba)

# Save transparent PNG
im = Image.fromarray(rgba_8bit)
im.save("RGB_composite_Fe_C_cooccurrence.png", "PNG")
