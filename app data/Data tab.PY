import tkinter as tk
from tkinter import ttk

from config import (
    COLOR_BG, COLOR_TEXT, COLOR_CARD, COLOR_MUTED, COLOR_ROW_ALT,
    FONT_SECTION, FONT_LABEL, FEATURE_COLUMNS,
)
from ui_widgets import make_card


def build_data_tab(parent, df):
    tk.Label(
        parent, text="DỮ LIỆU RƯỢU VANG", font=FONT_SECTION,
        bg=COLOR_BG, fg=COLOR_TEXT,
    ).pack(anchor="w", pady=(15, 10), padx=5)

    data_card = make_card(parent)
    data_card.pack(fill="both", expand=True, padx=5, pady=(0, 10))

    data_frame = tk.Frame(data_card, bg=COLOR_CARD)
    data_frame.pack(fill="both", expand=True, padx=2, pady=2)

    columns = list(df.columns) if len(df.columns) else ["id", "class_label"] + FEATURE_COLUMNS

    tree = ttk.Treeview(data_frame, columns=columns, show="headings", style="Custom.Treeview")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110, anchor="center")

    for i, (_, row) in enumerate(df.iterrows()):
        tag = "odd" if i % 2 else "even"
        tree.insert("", "end", values=list(row), tags=(tag,))

    tree.tag_configure("even", background=COLOR_CARD)
    tree.tag_configure("odd", background=COLOR_ROW_ALT)

    scroll_y = ttk.Scrollbar(data_frame, orient="vertical", command=tree.yview)
    scroll_x = ttk.Scrollbar(data_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    data_frame.grid_rowconfigure(0, weight=1)
    data_frame.grid_columnconfigure(0, weight=1)

    if len(df) == 0:
        tk.Label(
            data_card,
            text="Chưa có dữ liệu. Hãy import wine_data_import.sql vào MySQL rồi khởi động lại ứng dụng.",
            font=FONT_LABEL, bg=COLOR_CARD, fg=COLOR_MUTED,
        ).pack(pady=20)

    return tree