from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# CONFIGURATION
# =============================================================================

# Distance range used in the experiments (cm)
START_DISTANCE = 80
END_DISTANCE = 340
STEP = 10

# Base directory containing all measurement datasets
DATA_DIR = Path(
    r"C:\Users\crist\OneDrive\Desktop\Data Analysis Python\data\processed"
)

# Output directory
OUTPUT_DIR = Path(
    r"C:\Users\crist\OneDrive\Desktop\Data Analysis Python\results"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# EXPERIMENT FOLDERS
# =============================================================================

MATERIAL_FOLDERS = {
    "Exterior": "EXTERIOR",
    "Hallway": "PASILLO",
    "Wood": "MADERALOS",
    "Wood NLOS": "MADERANLOS",
    "Wood LOS-NLOS": "MADERALOSNLOS",
    "Metal": "METALLOS",
    "Metal NLOS": "METALNLOS",
    "Metal LOS-NLOS": "METALLOSNLOS",
    "Glass": "VIDRIOLOS",
    "Glass NLOS": "VIDRIONLOS",
    "Glass LOS-NLOS": "VIDRIOLOSNLOS",
    "Wall": "PAREDLOS",
    "Wall NLOS": "PAREDNLOS",
}

# =============================================================================
# FUNCTIONS
# =============================================================================

def build_file_paths(folder_name):
    """
    Generate a list of CSV file paths for a given experiment folder.

    Parameters
    ----------
    folder_name : str
        Folder containing the measurement CSV files.

    Returns
    -------
    list[Path]
        List of CSV file paths.
    """

    return [
        DATA_DIR / folder_name / f"{distance}CM.csv"
        for distance in range(START_DISTANCE, END_DISTANCE, STEP)
    ]


def calculate_metrics(file_paths):
    """
    Calculate accuracy and precision metrics for UWB ranging measurements.

    Metrics:
    - Mean Absolute Error (MAE)
    - Mean Standard Deviation
    - Root Mean Squared Error (RMSE)

    Parameters
    ----------
    file_paths : list[Path]
        List of CSV files containing distance measurements.

    Returns
    -------
    dict
        Dictionary containing calculated metrics.
    """

    dataframes = [pd.read_csv(path) for path in file_paths]

    reference_distances = np.array(
        list(range(START_DISTANCE, END_DISTANCE, STEP))
    )

    # Convert distances from meters to centimeters
    for df in dataframes:
        df["Distance"] *= 100

    # Mean measurement at each reference distance
    mean_measurements = np.array(
        [df["Distance"].mean() for df in dataframes]
    )

    # Standard deviation at each reference distance
    standard_deviations = np.array(
        [df["Distance"].std() for df in dataframes]
    )

    # Measurement error
    errors = mean_measurements - reference_distances

    # Mean Absolute Error
    mean_absolute_error = np.mean(np.abs(errors))

    # Root Mean Squared Error
    rmse = np.sqrt(np.mean(errors ** 2))

    # Average standard deviation
    mean_std = np.nanmean(standard_deviations)

    return {
        "Average Standard Deviation (cm)": round(mean_std, 4),
        "Mean Absolute Error (cm)": round(mean_absolute_error, 4),
        "RMSE (cm)": round(rmse, 4),
    }


# =============================================================================
# GENERATE FILE PATHS
# =============================================================================

experiment_paths = {
    label: build_file_paths(folder)
    for label, folder in MATERIAL_FOLDERS.items()
}

# =============================================================================
# CALCULATE METRICS
# =============================================================================

metrics_by_material = {
    material: calculate_metrics(paths)
    for material, paths in experiment_paths.items()
}

# Create summary DataFrame
metrics_df = pd.DataFrame(metrics_by_material).T

# =============================================================================
# SAVE EXCEL FILE
# =============================================================================

excel_output = OUTPUT_DIR / "uwb_metrics_summary.xlsx"

metrics_df.to_excel(excel_output)

# =============================================================================
# CREATE TABLE FIGURE
# =============================================================================

fig, ax = plt.subplots(figsize=(12, 6))

ax.axis("off")

table = ax.table(
    cellText=metrics_df.values,
    colLabels=metrics_df.columns,
    rowLabels=metrics_df.index,
    loc="center",
    cellLoc="center",
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

plt.title(
    "UWB Ranging Performance Metrics by Material and Scenario",
    fontsize=12,
)

plt.tight_layout()

# =============================================================================
# SAVE FIGURE
# =============================================================================

image_output = OUTPUT_DIR / "uwb_metrics_summary.png"

plt.savefig(
    image_output,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# =============================================================================
# CONFIRMATION
# =============================================================================

print("\nFiles saved successfully:")
print(f"Excel: {excel_output}")
print(f"Image: {image_output}")