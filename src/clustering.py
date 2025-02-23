"""
Module providing DBSCAN clustering functionality and parameter estimation.
"""

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def estimate_epsilon(coords: np.ndarray, k: int) -> float:
    """
    Estimate the ideal epsilon using the k-distance graph.

    For each point, the distance to its k-th nearest neighbor is calculated.
    Then, the "knee" (inflection point) of the sorted distance vector is determined
    using a geometric approach (maximal distance to the line connecting the first and last point).

    Args:
        coords: A numpy array of coordinates.
        k: The number of neighbors (typically equals minPts).

    Returns:
        The recommended epsilon value.
    """
    nbrs = NearestNeighbors(n_neighbors=k).fit(coords)
    distances, _ = nbrs.kneighbors(coords)
    k_distances = distances[:, k - 1]  # k-th nearest neighbor distance
    sorted_k_distances = np.sort(k_distances)
    n_points = len(sorted_k_distances)
    x = np.arange(n_points)
    y = sorted_k_distances

    # Define a line from the first to the last point in the graph
    line_start = np.array([0, y[0]])
    line_end = np.array([n_points - 1, y[-1]])
    line_vec = line_end - line_start
    norm = np.linalg.norm(line_vec)

    # Vectorized calculation of distances from each point to the line
    points = np.column_stack((x, y))
    diff = points - line_start
    distances_to_line = np.abs(line_vec[0] * diff[:, 1] - line_vec[1] * diff[:, 0]) / norm

    knee_index = np.argmax(distances_to_line)
    recommended_epsilon = sorted_k_distances[knee_index]
    return recommended_epsilon


def run_dbscan(coords: np.ndarray, eps: float, min_samples: int) -> np.ndarray:
    """
    Run DBSCAN on the provided coordinates.

    Args:
        coords: A numpy array of coordinates.
        eps: The epsilon parameter (maximum distance between two samples to be considered as in the same neighborhood).
        min_samples: The minimum number of samples in a neighborhood to form a cluster.

    Returns:
        An array of labels assigned by DBSCAN.
    """
    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(coords)
    return labels


def plot_clusters(coords: np.ndarray, labels: np.ndarray, x_label: str, y_label: str, title: str) -> None:
    """
    Visualize clustering results using matplotlib with flexible axis labels and title.
    If the data has more than 2 dimensions, PCA is used to project the data onto 2 dimensions for visualization.

    Args:
        coords: A numpy array of coordinates.
        labels: The cluster labels for each coordinate.
        x_label: Label for the x-axis.
        y_label: Label for the y-axis.
        title: Title of the plot.
    """
    unique_labels = set(labels)
    plt.figure(figsize=(8, 6))
    ax = plt.gca()
    cmap = plt.get_cmap('tab20')

    # If more than 2 dimensions, apply PCA for visualization.
    if coords.shape[1] > 2:
        pca = PCA(n_components=2)
        plot_data = pca.fit_transform(coords)
        # Override axis labels to clearly indicate a PCA projection.
        x_label, y_label = "Projection Axis 1", "Projection Axis 2"
    else:
        plot_data = coords

    for label in unique_labels:
        class_member_mask = (labels == label)
        xy = plot_data[class_member_mask]
        if label == -1:
            marker = "x"
            color = "k"
            label_text = "Noise"
        else:
            marker = "o"
            color = cmap((label - 1) % 20)
            label_text = f"Cluster {label}"
        ax.scatter(xy[:, 0], xy[:, 1], c=[color], marker=marker, label=label_text, s=10)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend()
    plt.show()
