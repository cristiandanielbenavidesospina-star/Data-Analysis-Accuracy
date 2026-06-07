"""
UWB Error Distribution Analysis

This script compares ranging error distributions across
multiple LOS, NLOS, and LOS/NLOS scenarios.

Outputs:
- Excel summary
- Boxplot visualization
- Violin plot visualization
- Summary table image

Author: Cristian Benavides
"""

from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# Configuration
# ============================================================

START_DISTANCE = 80
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
    "Exterior": "EXTERIOR/csv",
    "Hallway": "PASILLO",
    "Wood LOS": "MADERALOS",
    "Wood NLOS": "MADERANLOS",
    "Wood LOS-NLOS": "MADERALOSNLOS",
    "Metal LOS": "METALLOS",
    "Metal NLOS": "METALNLOS",
    "Metal LOS-NLOS": "METALLOSNLOS",
    "Glass LOS": "VIDRIOLOS",
    "Glass NLOS": "VIDRIONLOS",
    "Glass LOS-NLOS": "VIDRIOLOSNLOS",
    "Wall LOS": "PAREDLOS",
    "Wall NLOS": "PAREDNLOS"
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


def calculate_metrics(file_paths):
    """
    Calculate error metrics for one experiment.
    """

    reference_distances = list(
        range(
            START_DISTANCE,
            END_DISTANCE,
            STEP
        )
    )

    mean_errors = []
    all_errors = []

    for reference_distance, file_path in zip(
        reference_distances,
        file_paths
    ):

        try:

            df = pd.read_csv(file_path)

            df["Distance"] *= 100

            absolute_error = np.abs(
                df["Distance"] -
                reference_distance
            )

            mean_errors.append(
                absolute_error.mean()
            )

            all_errors.extend(
                absolute_error.tolist()
            )

        except Exception as error:

            print(
                f"Error loading {file_path}: {error}"
            )

    if len(all_errors) == 0:

        return {
            "Mean Error (cm)": np.nan,
            "Max Error (cm)": np.nan,
            "Min Error (cm)": np.nan,
            "RMSE (cm)": np.nan,
            "Error Distribution": []
        }

    all_errors = np.array(all_errors)

    return {
        "Mean Error (cm)": np.mean(all_errors),
        "Max Error (cm)": np.max(all_errors),
        "Min Error (cm)": np.min(all_errors),
        "RMSE (cm)": np.sqrt(
            np.mean(all_errors ** 2)
        ),
        "Error Distribution": mean_errors
    }


# ============================================================
# Process Experiments
# ============================================================

metrics_by_experiment = {}

error_distributions = {}

for experiment_name, folder_name in EXPERIMENTS.items():

    print(f"Processing {experiment_name}...")

    paths = build_file_paths(folder_name)

    results = calculate_metrics(paths)

    metrics_by_experiment[experiment_name] = results

    error_distributions[experiment_name] = (
        results["Error Distribution"]
    )

# ============================================================
# Create Summary DataFrame
# ============================================================

summary_df = pd.DataFrame(
    {
        key: value
        for key, value
        in metrics_by_experiment.items()
    }
).T

# Remove distribution column from summary table
summary_df_export = summary_df.drop(
    columns=["Error Distribution"]
)

summary_df_export = summary_df_export.round(2)

print("\nSummary Metrics")
print(summary_df_export)

# ============================================================
# Export Excel
# ============================================================

excel_file = (
    OUTPUT_DIR /
    "uwb_error_metrics.xlsx"
)

summary_df_export.to_excel(excel_file)

print(f"\nExcel saved: {excel_file}")

# ============================================================
# Prepare Data for Plots
# ============================================================

boxplot_df = pd.DataFrame(
    {
        key: pd.Series(value)
        for key, value
        in error_distributions.items()
    }
)

# ============================================================
# Boxplot
# ============================================================

plt.figure(figsize=(16, 8))

sns.boxplot(
    data=boxplot_df
)

plt.title(
    "Distribution of Mean Ranging Errors",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Scenario")
plt.ylabel("Mean Error (cm)")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.5
)

plt.tight_layout()

boxplot_file = (
    OUTPUT_DIR /
    "uwb_error_boxplot.png"
)

plt.savefig(
    boxplot_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"Boxplot saved: {boxplot_file}")

# ============================================================
# Violin Plot
# ============================================================

plt.figure(figsize=(16, 8))

sns.violinplot(
    data=boxplot_df,
    inner="box"
)

plt.title(
    "Error Distribution Across Scenarios",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Scenario")
plt.ylabel("Mean Error (cm)")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.5
)

plt.tight_layout()

violin_file = (
    OUTPUT_DIR /
    "uwb_error_violinplot.png"
)

plt.savefig(
    violin_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"Violin plot saved: {violin_file}")

# ============================================================
# Summary Table Figure
# ============================================================

fig, ax = plt.subplots(
    figsize=(12, 5)
)

ax.axis("off")

table = ax.table(
    cellText=summary_df_export.values,
    colLabels=summary_df_export.columns,
    rowLabels=summary_df_export.index,
    loc="center",
    cellLoc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.5)

plt.title(
    "UWB Error Metrics Summary",
    fontsize=16,
    fontweight="bold",
    pad=20
)

table_file = (
    OUTPUT_DIR /
    "uwb_error_summary_table.png"
)

plt.savefig(
    table_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"Summary table saved: {table_file}")

# ============================================================
# Ranking by RMSE
# ============================================================

ranking_df = summary_df_export.sort_values(
    by="RMSE (cm)"
)

ranking_file = (
    OUTPUT_DIR /
    "uwb_rmse_ranking.csv"
)

ranking_df.to_csv(ranking_file)

print(f"Ranking saved: {ranking_file}")

print("\nTop Performing Scenarios")
print("--------------------------------")
print(ranking_df)

print("\nAnalysis completed successfully.")