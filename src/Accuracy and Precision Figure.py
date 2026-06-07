"""
UWB Accuracy and Precision Analysis

This script evaluates the accuracy of UWB ranging measurements
by comparing measured distances against reference distances.

Outputs:
- Accuracy plot with error bars
- PNG figure saved to results/

Author: Cristian Benavides
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# Configuration
# ============================================================

START_DISTANCE = 10
END_DISTANCE = 910
STEP = 10

DATA_DIR = Path(
   r"C:\Users\crist\OneDrive\Desktop\Data Analysis Python\data\processed\PASILLO" 
   )

OUTPUT_DIR = Path(r"C:\Users\crist\OneDrive\Desktop\Data Analysis Python\results")
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# Helper Functions
# ============================================================

def build_file_paths():
    """
    Generate CSV file paths for all measurement distances.
    """
    return [
        DATA_DIR / f"{distance}CM.csv"
        for distance in range(
            START_DISTANCE,
            END_DISTANCE,
            STEP
        )
    ]


def load_measurements(file_paths):
    """
    Load CSV files and convert distances to centimeters.
    """
    dataframes = []

    for path in file_paths:

        df = pd.read_csv(path)

        # Convert meters to centimeters
        df["Distance"] *= 100

        dataframes.append(df)

    return dataframes


def calculate_statistics(dataframes):
    """
    Compute mean distance and standard deviation
    for each measurement set.
    """

    means = [
        df["Distance"].mean()
        for df in dataframes
    ]

    stds = [
        df["Distance"].std()
        for df in dataframes
    ]

    return means, stds


# ============================================================
# Main Analysis
# ============================================================

csv_files = build_file_paths()

dfs = load_measurements(csv_files)

reference_distances = np.arange(
    START_DISTANCE,
    END_DISTANCE,
    STEP
)

mean_distances, std_distances = calculate_statistics(dfs)

# ============================================================
# Compute Performance Metrics
# ============================================================

errors = np.array(mean_distances) - reference_distances

mae = np.mean(np.abs(errors))
rmse = np.sqrt(np.mean(errors**2))
max_error = np.max(np.abs(errors))

print("\nUWB Performance Metrics")
print("-------------------------")
print(f"Mean Absolute Error (MAE): {mae:.2f} cm")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f} cm")
print(f"Maximum Error: {max_error:.2f} cm")

# ============================================================
# Accuracy Plot
# ============================================================

plt.figure(figsize=(12, 7))

plt.errorbar(
    reference_distances,
    mean_distances,
    yerr=std_distances,
    fmt="-o",
    capsize=4,
    label="Measured Distance"
)

# Ideal reference line

plt.plot(
    reference_distances,
    reference_distances,
    linestyle="--",
    linewidth=2,
    label="Ideal Measurement"
)

plt.title(
    "UWB Ranging Accuracy Analysis",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Reference Distance (cm)")
plt.ylabel("Measured Distance (cm)")

plt.grid(alpha=0.3)

plt.legend()

plt.tight_layout()

figure_file = OUTPUT_DIR / "uwb_accuracy_analysis.png"

plt.savefig(
    figure_file,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print(f"\nFigure saved: {figure_file}")
