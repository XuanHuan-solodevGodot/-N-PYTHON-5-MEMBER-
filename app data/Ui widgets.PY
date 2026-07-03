import tkinter as tk
from tkinter import ttk

from config import (
    COLOR_BG, COLOR_HEADER, COLOR_ACCENT, COLOR_GOLD, COLOR_CARD,
    COLOR_TEXT, COLOR_MUTED, FONT_LABEL, FONT_LABEL_BOLD,
    FONT_STAT_NUM, FONT_STAT_LABEL,
)


def style_treeview(tree_name="Custom.Treeview", rowheight=28):
    """Applies the wine theme to a ttk Treeview style."""
    style = ttk.Style()
    style.configure(
        tree_name,
        background=COLOR_CARD,
        fieldbackground=COLOR_CARD,
        foreground=COLOR_TEXT,
        rowheight=rowheight,
        font=FONT_LABEL,
        borderwidth=0,
    )
    style.configure(
        tree_name + ".Heading",
        background=COLOR_ACCENT,
        foreground="white",
        font=FONT_LABEL_BOLD,
        relief="flat",
    )
    style.map(tree_name + ".Heading", background=[("active", COLOR_HEADER)])
    style.map(
        tree_name,
        background=[("selected", COLOR_GOLD)],
        foreground=[("selected", COLOR_TEXT)],
    )


def make_card(parent, **kwargs):
    """A plain white 'card' frame with a thin border, used everywhere."""
    return tk.Frame(
        parent, bg=COLOR_CARD, highlightbackground="#E3D6C8",
        highlightthickness=1, **kwargs
    )


def stat_card(parent, title, value, color, col):
    """A small dashboard stat card (colored strip + big number + label)."""
    card = make_card(parent, width=260, height=110)
    card.grid(row=0, column=col, padx=(0, 15), sticky="nsew")
    card.grid_propagate(False)

    tk.Frame(card, bg=color, width=6).pack(side="left", fill="y")

    inner = tk.Frame(card, bg=COLOR_CARD)
    inner.pack(side="left", fill="both", expand=True, padx=15, pady=10)

    tk.Label(inner, text=value, font=FONT_STAT_NUM, bg=COLOR_CARD, fg=color).pack(anchor="w")
    tk.Label(inner, text=title, font=FONT_STAT_LABEL, bg=COLOR_CARD, fg=COLOR_MUTED).pack(anchor="w")

    return card


def make_scrollable(parent, bg=COLOR_BG):
    """
    Creates a vertically-scrollable area inside `parent`.
    Returns the inner frame that content should be packed/gridded into,
    so tall tabs (like the predict form) are never cut off by a small window.
    """
    canvas = tk.Canvas(parent, bg=bg, highlightthickness=0)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=bg)

    inner.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )

    canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def _resize_inner(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", _resize_inner)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bind_wheel(_event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _unbind_wheel(_event):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>", _bind_wheel)
    canvas.bind("<Leave>", _unbind_wheel)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return inner