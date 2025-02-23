"""
Main entry point for the DBSCAN Cluster Analyzer application.
"""

import tkinter as tk
from gui import DBSCANApp


def main() -> None:
    """Initialize and run the Tkinter application."""
    root = tk.Tk()
    app = DBSCANApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()