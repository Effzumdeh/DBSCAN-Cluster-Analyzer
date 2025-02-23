"""
Graphical User Interface (GUI) module for the DBSCAN Cluster Analyzer application.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from clustering import estimate_epsilon, run_dbscan, plot_clusters
from helpers import show_explanation_popup


class DBSCANApp:
    """
    Main application class that encapsulates the Tkinter GUI.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the DBSCAN clustering application GUI.

        Args:
            root: The root Tkinter window.
        """
        self.root = root
        self.root.title("DBSCAN Cluster Analyzer")
        self.data = None  # Loaded dataset will be stored here
        self.selected_columns = []  # Columns chosen for clustering

        # --- GUI Elements ---
        self.dataset_label = tk.Label(root, text="No dataset loaded")
        self.dataset_label.pack(pady=5)

        self.load_button = tk.Button(root, text="Load Dataset", command=self.load_file)
        self.load_button.pack(pady=5)

        # Button to change column selection after initial load (if applicable)
        self.change_columns_button = tk.Button(
            root, text="Change Column Selection", command=self.change_columns, state=tk.DISABLED
        )
        self.change_columns_button.pack(pady=5)

        # Entry field for minPts (minimum number of points in the eps-radius)
        self.minpts_label = tk.Label(root, text="Minimum number of points (minPts):")
        self.minpts_label.pack(pady=5)
        self.minpts_entry = tk.Entry(root)
        self.minpts_entry.pack(pady=5)
        self.minpts_entry.insert(0, "5")

        # Entry field for Epsilon (eps)
        self.eps_label = tk.Label(root, text="Epsilon (Distance parameter):")
        self.eps_label.pack(pady=5)
        self.eps_entry = tk.Entry(root)
        self.eps_entry.pack(pady=5)
        self.eps_entry.insert(0, "0.01")  # Default value; adjust according to data scale

        # Button to automatically estimate parameters
        self.auto_param_button = tk.Button(
            root, text="Automatically Estimate Parameters", command=self.auto_estimate_parameters
        )
        self.auto_param_button.pack(pady=5)

        # Button to perform clustering
        self.cluster_button = tk.Button(root, text="Run Clustering", command=self.run_clustering)
        self.cluster_button.pack(pady=10)

        # Information label explaining eps and minPts influence
        self.info_label = tk.Label(
            root,
            text=(
                "Adjust Epsilon and minPts to obtain different clustering results.\n"
                "Epsilon defines the maximum distance within which points are considered neighbors.\n"
                "minPts specifies the minimum number of points required to form a cluster."
            ),
            wraplength=400
        )
        self.info_label.pack(pady=10)

        # Help button that shows an explanation popup
        self.help_button = tk.Button(root, text="?", command=lambda: show_explanation_popup(root))
        self.help_button.pack(pady=5)

    def load_file(self) -> None:
        """
        Open a file dialog to load a CSV file containing data.
        For files with more than two columns, a popup allows the user to select the columns for clustering.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                if self.data.shape[1] > 2:
                    # Open column selection popup if more than two columns available.
                    self.open_column_selection_popup()
                    self.change_columns_button.config(state=tk.NORMAL)
                else:
                    # For two columns, select both automatically.
                    self.selected_columns = list(self.data.columns)
                    self.dataset_label.config(
                        text=f"Dataset loaded with columns: {', '.join(self.selected_columns)}"
                    )
                    self.change_columns_button.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Error", f"Error loading file:\n{e}")

    def open_column_selection_popup(self) -> None:
        """
        Open a popup window that allows the user to select the columns to be used for clustering.
        A minimum of two columns must be selected. Also, non-numeric columns are rejected with an error message.
        """
        popup = tk.Toplevel(self.root)
        popup.title("Select Columns for Clustering")
        popup.geometry("300x300")
        popup.resizable(False, False)

        instruction_label = tk.Label(popup, text="Select at least two columns for clustering:")
        instruction_label.pack(pady=5)

        columns = list(self.data.columns)
        check_vars = []
        # Frame to contain the checkboxes
        check_frame = tk.Frame(popup)
        check_frame.pack(fill="both", expand=True, padx=10, pady=10)

        for col in columns:
            var = tk.BooleanVar()
            check_vars.append(var)
            chk = tk.Checkbutton(check_frame, text=col, variable=var)
            chk.pack(anchor='w')

        def confirm_selection() -> None:
            selected = [col for col, var in zip(columns, check_vars) if var.get()]
            if len(selected) < 2:
                messagebox.showerror("Error", "Please select at least two columns for clustering.")
                return
            # Check if selected columns are numeric; if not, show error message.
            non_numeric = [col for col in selected if not pd.api.types.is_numeric_dtype(self.data[col])]
            if non_numeric:
                messagebox.showerror(
                    "Error",
                    f"The following column(s) contain non-numeric data: {', '.join(non_numeric)}.\n"
                    "DBSCAN requires numeric data. Please transform these columns into a numeric scale (e.g., using "
                    "label encoding, one-hot encoding, or embedding techniques) before clustering."
                )
                return
            self.selected_columns = selected
            self.dataset_label.config(
                text=f"Dataset loaded with columns: {', '.join(self.selected_columns)}"
            )
            popup.destroy()

        confirm_button = tk.Button(popup, text="Confirm Selection", command=confirm_selection)
        confirm_button.pack(pady=5)

    def change_columns(self) -> None:
        """
        Allows re-selection of columns without reloading the CSV.
        """
        if self.data is not None and self.data.shape[1] > 2:
            self.open_column_selection_popup()

    def auto_estimate_parameters(self) -> None:
        """
        Automatically determine ideal settings for DBSCAN and update the input fields.
        """
        if self.data is None:
            messagebox.showwarning("Warning", "Please load a dataset first!")
            return

        if self.data.shape[1] > 2:
            if not self.selected_columns or len(self.selected_columns) < 2:
                messagebox.showwarning("Warning", "Please select at least two columns for clustering!")
                return
            coords = self.data[self.selected_columns].values
        else:
            coords = self.data.values

        try:
            min_pts_val = int(self.minpts_entry.get())
            if min_pts_val < 2:
                raise ValueError
        except ValueError:
            min_pts_val = 5
            messagebox.showinfo("Info", "Invalid value for minPts. Using default value 5.")

        recommended_epsilon = estimate_epsilon(coords, min_pts_val)
        self.eps_entry.delete(0, tk.END)
        self.eps_entry.insert(0, f"{recommended_epsilon:.4f}")
        messagebox.showinfo(
            "Parameters Estimated",
            f"Recommended Epsilon: {recommended_epsilon:.4f}\nminPts: {min_pts_val}"
        )

    def run_clustering(self) -> None:
        """
        Run DBSCAN on the loaded data, visualize the results with a legend,
        and display warnings if parameters might lead to poor clustering.
        """
        if self.data is None:
            messagebox.showwarning("Warning", "Please load a dataset first!")
            return

        if self.data.shape[1] > 2:
            if not self.selected_columns or len(self.selected_columns) < 2:
                messagebox.showwarning("Warning", "Please select at least two columns for clustering!")
                return
            coords = self.data[self.selected_columns].values
        else:
            coords = self.data.values

        try:
            eps = float(self.eps_entry.get())
            min_pts = int(self.minpts_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid values for Epsilon and minPts.")
            return

        labels = run_dbscan(coords, eps, min_pts)

        # Check for potential issues in clustering result
        unique_labels = set(labels)
        clusters = [label for label in unique_labels if label != -1]

        if len(clusters) == 0:
            messagebox.showwarning(
                "Warning",
                "All points were marked as noise.\nHint: Increase Epsilon or decrease minPts to detect clusters."
            )
        elif len(clusters) == 1:
            messagebox.showwarning(
                "Warning",
                "All points were grouped into a single cluster.\nHint: Decrease Epsilon or increase minPts for finer clustering."
            )

        # Determine labels for plotting:
        if len(self.selected_columns) > 2:
            x_label = "PC1"
            y_label = "PC2"
            title = f"Detected Clusters ({', '.join(self.selected_columns)})"
        else:
            x_label = self.selected_columns[0]
            y_label = self.selected_columns[1]
            title = "Detected Clusters"

        plot_clusters(coords, labels, x_label, y_label, title)

        # Additional console output:
        n_clusters = len(clusters)
        n_noise = list(labels).count(-1)
        print(f"Number of clusters (excluding noise): {n_clusters}")
        print(f"Number of noise points: {n_noise}")
