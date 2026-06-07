# UWB Distance Measurement Analysis

## Overview

This repository contains the Python scripts and datasets developed during my undergraduate research project focused on evaluating the accuracy of Ultra-Wideband (UWB) distance measurements under different propagation conditions.

The objective of the study was to analyze how different environmental obstacles and propagation scenarios affect ranging accuracy, precision, and measurement error.

The experiments were conducted using UWB devices in both Line-of-Sight (LOS) and Non-Line-of-Sight (NLOS) conditions.

---

## Research Objectives

The project investigates the impact of different materials and environments on UWB ranging performance, including:

* Metal obstacles
* Wooden obstacles
* Glass obstacles
* Concrete walls
* Indoor hallway scenarios
* Outdoor environments
* LOS conditions
* NLOS conditions
* Mixed LOS/NLOS conditions

The analysis focuses on evaluating measurement accuracy and comparing the performance of each scenario.

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* OpenPyXL
* Git
* GitHub

---

## Dataset Structure

The dataset contains experimental ranging measurements collected at reference distances between 10 cm and 340 cm (and up to 910 cm in some scenarios).

```text
data/
│
├── raw/
│   ├── metal_los/
│   ├── metal_nlos/
│   ├── metal_los_nlos/
│   ├── wood_los/
│   ├── wood_nlos/
│   ├── wood_los_nlos/
│   ├── glass_los/
│   ├── glass_nlos/
│   ├── glass_los_nlos/
│   ├── wall_los/
│   ├── wall_nlos/
│   ├── hallway/
│   └── outdoor/
```

Each CSV file contains multiple UWB distance measurements recorded at a specific reference distance.

---

## Analysis Performed

### Accuracy Analysis

Comparison between:

* Reference distance
* Measured distance

Metrics:

* Mean Error
* Absolute Error
* Standard Deviation
* Root Mean Square Error (RMSE)

---

### Statistical Analysis

The project includes:

* Error distributions
* Histograms
* Boxplots
* Violin plots
* Heatmaps
* Scenario rankings

---

### Automated Reporting

Python scripts automatically generate:

* Excel reports
* CSV summaries
* Statistical tables
* Publication-ready figures

---

## Project Structure

```text
UWB-Distance-Measurement-Analysis/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── accuracy_analysis.py
│   ├── error_distribution_analysis.py
│   ├── metrics_summary.py
│   └── report_generation.py
│
├── results/
│   ├── figures/
│   └── reports/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/UWB-Distance-Measurement-Analysis.git
```

Navigate to the project folder:

```bash
cd UWB-Distance-Measurement-Analysis
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Example Outputs

The repository generates visualizations such as:

* Accuracy comparison plots
* Error distribution histograms
* Boxplots
* Violin plots
* Heatmaps
* Performance rankings

These outputs help evaluate the behavior of UWB ranging systems under different propagation conditions.

---

## Skills Demonstrated

This project demonstrates practical experience in:

### Software Development

* Python programming
* Data processing pipelines
* Code organization and refactoring
* Version control with Git

### Data Analysis

* Data cleaning
* Statistical analysis
* Error modeling
* Data visualization

### Engineering Applications

* Ultra-Wideband (UWB) systems
* Indoor positioning systems
* Wireless communications
* Experimental performance evaluation

---

## Author

Cristian Benavides

Electronic Engineer

Areas of Interest:

* Software Engineering
* Data Analysis
* Artificial Intelligence
* FinTech
* Embedded Systems
* Wireless Communications
