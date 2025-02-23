"""
Helper module providing utility functions, including a popup that explains
the DBSCAN algorithm, parameter estimation, PCA projection, and interpretation of results.
The explanation can be displayed in English or German with two selectable levels of detail.
"""

import tkinter as tk
from tkinter import ttk

def show_explanation_popup(parent: tk.Tk) -> None:
    """
    Display a popup window with an explanation of the DBSCAN algorithm and PCA projection.
    The explanation text is available in English and German (selectable via dropdown)
    and can be adjusted in detail level using a slider with values 1 (simple) and 2 (academic).

    Args:
        parent: The parent Tkinter window.
    """
    explanations = {
        "English": {
            1: (
                "Imagine you have a map with scattered points representing Wi-Fi signal strength in a city. "
                "Some areas have many points close together (high signal zones), while others have fewer points "
                "(low signal or no coverage). DBSCAN groups dense areas into clusters and marks sparse areas as noise. "
                "If we have more than two factors (e.g., signal strength, number of users, distance from the router), "
                "PCA helps reduce them to two dimensions for easier visualization."
            ),
            2: (
                "DBSCAN (Density-Based Spatial Clustering of Applications with Noise) is a density-driven clustering algorithm "
                "that groups data points based on their local neighborhood. Unlike k-means, it does not require specifying "
                "the number of clusters in advance and can identify arbitrarily shaped clusters. DBSCAN relies on two parameters: "
                "epsilon (ε), which defines the radius of a neighborhood, and minPts, the minimum number of points required "
                "to form a dense region. Points are classified as core, border, or noise.\n\n"
                "When working with high-dimensional data, PCA (Principal Component Analysis) is used to project the data into "
                "a two-dimensional space while preserving variance. PCA finds the directions of greatest variation (principal components) "
                "and constructs new axes where the first component captures the highest variance, followed by the second. "
                "This transformation allows DBSCAN results to be visualized even when the original data has more than two dimensions."
            )
        },
        "Deutsch": {
            1: (
                "Stell dir vor, du hast eine Karte mit Punkten, die WLAN-Signalstärke in einer Stadt anzeigen. "
                "In manchen Bereichen gibt es viele Punkte nah beieinander (starke Signalzonen), in anderen weniger "
                "(schwaches Signal oder kein Empfang). DBSCAN gruppiert dichte Bereiche in Cluster und markiert dünn besetzte "
                "Bereiche als Rauschen. Wenn wir mehr als zwei Faktoren haben (z. B. Signalstärke, Anzahl der Nutzer, Entfernung "
                "vom Router), hilft PCA dabei, sie für die Visualisierung auf zwei Dimensionen zu reduzieren."
            ),
            2: (
                "DBSCAN (Density-Based Spatial Clustering of Applications with Noise) ist ein dichtebasierter Clustering-Algorithmus, "
                "der Datenpunkte anhand ihrer lokalen Umgebung gruppiert. Im Gegensatz zu k-Means erfordert DBSCAN keine vorherige "
                "Festlegung der Cluster-Anzahl und erkennt Cluster beliebiger Form. DBSCAN verwendet zwei Parameter: Epsilon (ε), "
                "das den Radius einer Nachbarschaft bestimmt, und minPts, die Mindestanzahl an Punkten für eine dichte Region. "
                "Punkte werden als Kernpunkte, Randpunkte oder Rauschen klassifiziert.\n\n"
                "Für hochdimensionale Daten wird PCA (Hauptkomponentenanalyse) eingesetzt, um die Daten in eine zweidimensionale "
                "Darstellung zu projizieren, während die Datenvarianz möglichst erhalten bleibt. PCA bestimmt die Hauptrichtungen "
                "der Variation (Hauptkomponenten) und konstruiert neue Achsen, wobei die erste Hauptkomponente die größte Varianz "
                "erfasst, gefolgt von der zweiten. Diese Transformation ermöglicht die Visualisierung der DBSCAN-Ergebnisse auch dann, "
                "wenn die ursprünglichen Daten mehr als zwei Dimensionen haben."
            )
        }
    }

    current_language = tk.StringVar(value="English")
    current_level = tk.IntVar(value=1)

    def update_explanation_text(*args) -> None:
        """
        Update the explanation text based on the selected language and explanation level.
        """
        lang = current_language.get()
        level = current_level.get()
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", explanations[lang][level])
        text_widget.config(state="disabled")

    popup = tk.Toplevel(parent)
    popup.title("Explanation / Erklärung")
    popup.geometry("600x500")
    popup.resizable(False, False)

    control_frame = ttk.Frame(popup, padding="10")
    control_frame.pack(fill="x", expand=False)

    lang_label = ttk.Label(control_frame, text="Select Language / Sprache wählen:")
    lang_label.pack(side="left", padx=(0, 5))
    lang_menu = ttk.OptionMenu(control_frame, current_language, current_language.get(), "English", "Deutsch", command=lambda _: update_explanation_text())
    lang_menu.pack(side="left", padx=(0, 20))

    level_label = ttk.Label(control_frame, text="Explanation Level / Erklärungsniveau:")
    level_label.pack(side="left", padx=(0, 5))
    level_slider = tk.Scale(
        control_frame,
        from_=1,
        to=2,
        orient="horizontal",
        resolution=1,
        variable=current_level,
        command=lambda val: update_explanation_text()
    )
    level_slider.pack(side="left", padx=(0, 5))

    text_frame = ttk.Frame(popup, padding="10")
    text_frame.pack(fill="both", expand=True)

    text_widget = tk.Text(text_frame, wrap="word")
    text_widget.pack(fill="both", expand=True)
    update_explanation_text()

    close_button = ttk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)