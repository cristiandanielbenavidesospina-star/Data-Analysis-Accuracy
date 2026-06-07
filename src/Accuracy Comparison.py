"""
UWB Accuracy Comparison Across Propagation Conditions

This script compares the average measured distance
against the ground-truth distance for multiple
propagation scenarios.

Outputs:
- Accuracy comparison plot
- CSV file with mean distances

Author: Cristian Benavides
"""

from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Configuration
# ============================================================

START_DISTANCE = 60
END_DISTANCE = 340
STEP = 10

DATA_DIR = Path(
    r"C:\Users\crist\OneDrive\Desktop\Data Analysis Python\data\processed"
)

OUTPUT_DIR = Path(r"C:\Users\crist\OneDrive\Desktop\Data Analysis Python\results")
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# Experiment Definitions
# ============================================================

EXPERIMENTS = {
    "Metal NLOS": "METALNLOS",
    "Metal LOS-NLOS": "METALLOSNLOS",
    "Metal LOS": "METALLOS",
    "Outdoor": "EXTERIOR"
}

# ============================================================
# Helper Functions
# ============================================================

def build_file_paths(folder_name):
    """
    Generate CSV paths for one experiment.
    """

    return [
        DATA_DIR / folder_name / f"{distance}CM.csv"
        for distance in range(
            START_DISTANCE,
            END_DISTANCE,
            STEP
        )
    ]


def load_mean_distances(file_paths):
    """
    Calculate mean measured distance for each file.
    """

    mean_values = []

    for file_path in file_paths:

        try:

            df = pd.read_csv(file_path)

            # Convert meters to centimeters
            df["Distance"] *= 100

            mean_values.append(
                df["Distance"].mean()
            )

        except Exception as error:

            print(
                f"Error loading {file_path}: {error}"
            )

            mean_values.append(np.nan)

    return mean_values


# ============================================================
# Reference Distances
# ============================================================

reference_distances = np.arange(
    START_DISTANCE,
    END_DISTANCE,
    STEP
)

# ============================================================
# Load Experiments
# ============================================================

results = {}

for experiment_name, folder_name in EXPERIMENTS.items():

    print(f"Processing {experiment_name}...")

    file_paths = build_file_paths(folder_name)

    results[experiment_name] = load_mean_distances(
        file_paths
    )

# ============================================================
# Export Mean Distances
# ============================================================

mean_distances_df = pd.DataFrame(
    results,
    index=reference_distances
)

mean_distances_df.index.name = (
    "Reference Distance (cm)"
)

csv_file = (
    OUTPUT_DIR /
    "uwb_mean_distance_comparison.csv"
)

mean_distances_df.to_csv(csv_file)

print(f"\nCSV saved: {csv_file}")

# ============================================================
# Accuracy Comparison Plot
# ============================================================

plt.figure(figsize=(12, 8))

for experiment_name in results:

    plt.plot(
        reference_distances,
        results[experiment_name],
        marker="o",
        linewidth=2,
        label=experiment_name
    )

# Ideal measurement line

plt.plot(
    reference_distances,
    reference_distances,
    linestyle="--",
    linewidth=2,
    label="Ideal Measurement"
)

plt.title(
    "UWB Accuracy Comparison Across Propagation Conditions",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel(
    "Reference Distance (cm)"
)

plt.ylabel(
    "Measured Distance (cm)"
)

plt.grid(
    alpha=0.3
)

plt.legend()

plt.tight_layout()

figure_file = (
    OUTPUT_DIR /
    "uwb_accuracy_comparison.png"
)

plt.savefig(
    figure_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"Figure saved: {figure_file}")

# ============================================================
# Calculate Global Metrics
# ============================================================

print("\nScenario Performance Summary")
print("-----------------------------------")

for experiment_name, measurements in results.items():

    measurements = np.array(measurements)

    valid_mask = ~np.isnan(measurements)

    errors = (
        measurements[valid_mask]
        - reference_distances[valid_mask]
    )

    mae = np.mean(np.abs(errors))

    rmse = np.sqrt(
        np.mean(errors**2)
    )

    print(
        f"{experiment_name}"
        f" | MAE = {mae:.2f} cm"
        f" | RMSE = {rmse:.2f} cm"
    )

print("\nAnalysis completed successfully.")