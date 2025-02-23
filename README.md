# DBSCAN-Cluster-Analyzer

A Tkinter-based application for DBSCAN clustering analysis of GPS or multi-dimensional data. This tool allows users to load CSV datasets containing two or more columns, automatically estimate DBSCAN parameters, and visualize clustering results. If the dataset contains more than two columns, a pop-up allows the user to select which columns should be used for clustering.

## Features

- Load CSV datasets with two or more columns.
- Interactive column selection (via checkboxes) for multi-dimensional datasets.
- Automatic parameter estimation for DBSCAN (epsilon and minPts).
- Visualization of clustering results with matplotlib.
- A help pop-up that explains the DBSCAN algorithm, the parameter estimation process, and how to interpret the results.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/effzumdeh/DBSCAN-Cluster-Analyzer.git

2. Navigate to the project directory:
    cd DBSCAN-Cluster-Analyzer

3. Install the required dependencies:
    pip install -r requirements.txt