import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Load the calibration data
file_path = "EA-07-29-25-repeated.xlsx"
df_cal = pd.read_excel(file_path, sheet_name="calibration", header=None)

# Manually assign columns
df_cal.columns = ["Sample_ID", "N_Response", "N_Weight", "C_Response", "C_Weight"]
print(df_cal.head(10))  # See first 10 rows to check for unexpected strings
print(df_cal.dtypes)

# Check for any non-numeric or missing values in N_Response and N_Weight
print(df_cal["N_Response"].apply(type).value_counts())
print(df_cal["N_Weight"].apply(type).value_counts())

# Convert columns to numeric explicitly, forcing errors to NaN
df_cal["N_Response"] = pd.to_numeric(df_cal["N_Response"], errors='coerce')
df_cal["N_Weight"] = pd.to_numeric(df_cal["N_Weight"], errors='coerce')

# Drop any rows with NaN values after conversion
df_cal.dropna(subset=["N_Response", "N_Weight"], inplace=True)

# === Nitrogen Linear Calibration ===
X_N = df_cal["N_Response"].values.reshape(-1, 1)
y_N = df_cal["N_Weight"].values

lin_reg_N = LinearRegression().fit(X_N, y_N)
y_pred_N = lin_reg_N.predict(X_N)
r2_N = r2_score(y_N, y_pred_N)

plt.figure(figsize=(5, 5), dpi=300)
plt.scatter(
    X_N, y_N,
    color='olive',
    edgecolor='black',
    s=6**2,
    label="Data"
)
plt.plot(
    X_N, y_pred_N,
    color='gray',
    linestyle='--',
    label=f"Linear Fit\n$y={lin_reg_N.coef_[0]:.4f}x+{lin_reg_N.intercept_:.4f}$\n$R^2={r2_N:.4f}$"
)
plt.xlabel("Nitrogen Response (a.u.)", fontsize=12, style='italic', fontname='Arial')
plt.ylabel("Nitrogen Weight (mg)", fontsize=12, style='italic', fontname='Arial')
plt.xticks(fontsize=10, fontname='Arial', style='italic')
plt.yticks(fontsize=10, fontname='Arial', style='italic')
plt.grid(True, linestyle=':', alpha=0.5)
plt.gca().set_facecolor('none')
plt.legend(prop={'family': 'Arial', 'size': 8})
plt.savefig("Nitrogen_Calibration_Curve.png", dpi=300, transparent=True, bbox_inches='tight')
plt.show()

# === Carbon Linear and Quadratic Calibration ===
X_C = df_cal["C_Response"].values.reshape(-1, 1)
y_C = df_cal["C_Weight"].values

# Linear fit
lin_reg_C = LinearRegression().fit(X_C, y_C)
y_pred_C_lin = lin_reg_C.predict(X_C)
r2_C_lin = r2_score(y_C, y_pred_C_lin)

# Quadratic fit
X_C_quad = np.column_stack([X_C.flatten()**2, X_C.flatten()])
lin_reg_C_quad = LinearRegression().fit(X_C_quad, y_C)
y_pred_C_quad = lin_reg_C_quad.predict(X_C_quad)
r2_C_quad = r2_score(y_C, y_pred_C_quad)

plt.figure(figsize=(5, 5), dpi=300)
plt.scatter(
    X_C, y_C,
    color='maroon',
    edgecolor='black',
    s=6**2,
    label="Data"
)

sorted_idx = np.argsort(X_C.flatten())

# Linear fit dashed gray
plt.plot(
    X_C[sorted_idx], y_pred_C_lin[sorted_idx],
    color='gray',
    linestyle='--',
    label=f"Linear Fit\n$y={lin_reg_C.coef_[0]:.4f}x+{lin_reg_C.intercept_:.4f}$\n$R^2={r2_C_lin:.4f}$"
)

# Quadratic fit dashed black
plt.plot(
    X_C[sorted_idx], y_pred_C_quad[sorted_idx],
    color='black',
    linestyle='--',
    label=(f"Quadratic Fit\n$y={lin_reg_C_quad.coef_[0]:.4e}x^2"
           f"+{lin_reg_C_quad.coef_[1]:.4f}x+{lin_reg_C_quad.intercept_:.4f}$\n"
           f"$R^2={r2_C_quad:.4f}$")
)

plt.xlabel("Carbon Response (a.u.)", fontsize=12, style='italic', fontname='Arial')
plt.ylabel("Carbon Weight (mg)", fontsize=12, style='italic', fontname='Arial')
plt.xticks(fontsize=10, fontname='Arial', style='italic')
plt.yticks(fontsize=10, fontname='Arial', style='italic')
plt.grid(True, linestyle=':', alpha=0.5)
plt.gca().set_facecolor('none')
plt.legend(prop={'family': 'Arial', 'size': 8})
plt.savefig("Carbon_Calibration_Curve.png", dpi=300, transparent=True, bbox_inches='tight')
plt.show()