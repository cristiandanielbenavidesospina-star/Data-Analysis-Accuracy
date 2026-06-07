"""
UWB Error Distribution Analysis

This script analyzes the distribution of ranging errors
for LOS and NLOS measurement scenarios.

Outputs:
- Histogram comparison
- Error statistics CSV
- PNG visualization

Author: Cristian Benavides
"""

from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Configuration
# ============================================================

START_DISTANCE = 80
END_DISTANCE = 330
STEP = 10

# Update these paths according to your dataset structure
LOS_DIR = Path(
    r"C:\Users\crist\OneDrive\Desktop\Data Analysis Python\data\processed\METALLOS"
)

NLOS_DIR = Path(
    r"C:\Users\crist\OneDrive\Desktop\Data Analysis Python\data\processed\METALNLOS"
)




OUTPUT_DIR = Path(r"C:\Users\crist\OneDrive\Desktop\Data Analysis Python\results")
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# Helper Functions
# ============================================================

def build_file_paths(directory):
    """
    Generate CSV file paths for an experiment.
    """
    return [
        directory / f"{distance}CM.csv"
        for distance in range(
            START_DISTANCE,
            END_DISTANCE + STEP,
            STEP
        )
    ]


def calculate_errors(file_paths, reference_distances):
    """
    Calculate absolute ranging errors.

    Parameters
    ----------
    file_paths : list
        List of CSV files.

    reference_distances : list
        Ground truth distances in centimeters.

    Returns
    -------
    list
        All absolute errors.
    """

    all_errors = []

    for reference_distance, file_path in zip(
        reference_distances,
        file_paths
    ):

        if not file_path.exists():

            print(
                f"Warning: File not found -> {file_path}"
            )
            continue

        df = pd.read_csv(file_path)

        measured_distances = df["Distance"] * 100

        absolute_errors = np.abs(
            measured_distances - reference_distance
        )

        all_errors.extend(absolute_errors)

    return all_errors


def calculate_statistics(errors):
    """
    Compute descriptive statistics.
    """

    return {
        "Mean Error (cm)": np.mean(errors),
        "Median Error (cm)": np.median(errors),
        "Std Dev (cm)": np.std(errors),
        "Max Error (cm)": np.max(errors),
        "Min Error (cm)": np.min(errors),
        "RMSE (cm)": np.sqrt(np.mean(np.square(errors)))
    }


# ============================================================
# Load Data
# ============================================================

reference_distances = list(
    range(
        START_DISTANCE,
        END_DISTANCE + STEP,
        STEP
    )
)

los_files = build_file_paths(LOS_DIR)

nlos_files = build_file_paths(NLOS_DIR)

# ============================================================
# Error Calculation
# ============================================================

los_errors = calculate_errors(
    los_files,
    reference_distances
)

nlos_errors = calculate_errors(
    nlos_files,
    reference_distances
)

# ============================================================
# Statistics
# ============================================================

los_stats = calculate_statistics(los_errors)

nlos_stats = calculate_statistics(nlos_errors)

statistics_df = pd.DataFrame(
    {
        "LOS": los_stats,
        "NLOS": nlos_stats
    }
)

statistics_file = (
    OUTPUT_DIR /
    "error_distribution_statistics.csv"
)

statistics_df.to_csv(statistics_file)

print("\nError Statistics")
print("---------------------------")
print(statistics_df)

# ============================================================
# Histogram Comparison
# ============================================================

fig, axes = plt.subplots(
    1,
    2,
    figsize=(14, 6)
)

# LOS Histogram

axes[0].hist(
    los_errors,
    bins=30,
    alpha=0.8,
    edgecolor="black"
)

axes[0].set_title(
    "LOS Error Distribution",
    fontsize=14,
    fontweight="bold"
)

axes[0].set_xlabel(
    "Absolute Error (cm)"
)

axes[0].set_ylabel(
    "Frequency"
)

axes[0].grid(alpha=0.3)

# NLOS Histogram

axes[1].hist(
    nlos_errors,
    bins=30,
    alpha=0.8,
    edgecolor="black"
)

axes[1].set_title(
    "NLOS Error Distribution",
    fontsize=14,
    fontweight="bold"
)

axes[1].set_xlabel(
    "Absolute Error (cm)"
)

axes[1].set_ylabel(
    "Frequency"
)

axes[1].grid(alpha=0.3)

plt.suptitle(
    "UWB Error Distribution Analysis",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()

histogram_file = (
    OUTPUT_DIR /
    "error_distribution_comparison.png"
)

plt.savefig(
    histogram_file,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print(
    f"\nStatistics saved: {statistics_file}"
)

print(
    f"Figure saved: {histogram_file}"
)
