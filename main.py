"""
main.py — Punto de entrada.

Correr:
    python main.py
"""

from tkinter import ttk
from app import App

if __name__ == "__main__":
    app = App()

    style = ttk.Style(app)
    style.theme_use("clam")
    style.configure("TCombobox",
                     fieldbackground="#21262d",
                     background="#161b22",
                     foreground="#e6edf3",
                     selectbackground="#1f6feb",
                     selectforeground="#e6edf3",
                     arrowcolor="#8b949e")

    app.mainloop()
