# DBSCAN-Cluster-Analyzer

A Tkinter-based application for DBSCAN clustering analysis of GPS or multi-dimensional data. This tool was developed as a showcase application for the course "Algorithms and Data Structures" at DHBW Stuttgart. It helps students understand and interpret clustering algorithms like DBSCAN through interactive visualization and parameter estimation.

## Features

- **Load CSV datasets** with two or more columns.
- **Interactive column selection** (via checkboxes) for multi-dimensional datasets.
- **Automatic parameter estimation for DBSCAN** (epsilon and minPts) to assist in finding meaningful clusters.
- **Visualization of clustering results** with matplotlib.
- **Real-time validation** to prevent non-numeric data from being used for clustering, with explanations on data preprocessing and suitable scaling methods.
- **Flexible PCA-based projection** for high-dimensional data.
- **Comprehensive help pop-up**, explaining DBSCAN and PCA in varying levels of details:
   - **Basic level**: A simple, real-world example for intuitive understanding
   - **Advanced level**: A deep academic explanation covering density-based clustering, parameter impact, and interpretation.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/effzumdeh/DBSCAN-Cluster-Analyzer.git

2. Navigate to the project directory:
    cd DBSCAN-Cluster-Analyzer

3. Install the required dependencies:
    pip install -r requirements.txt


## Usage
1. Launch the application with python main.py
2. Load a CSV dataset with at least two numerical columns.
3. Select relevant columns, if the dataset has more than two columns
4. Clsuter the data - the application estimates optimal DBSCAN parameters or allows manual adjustment.
5. Visualizie results.
6. Refine selection.

## Educational Purpose

This tool was specifically designed as a **teaching aid** for my "Algorithms and Data Structures" course at **DHBW Stuttgart**. It enables students to explore the practical application of DBSCAN clustering, understand parameter tuning, and interpret results effectively. The interactive nature of the tool supports hands-on learning and experimentation with real-world datasets.
