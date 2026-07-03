import tkinter as tk

from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT, COLOR_ACCENT, COLOR_HEADER, COLOR_MUTED,
    FONT_SECTION, FONT_LABEL, FONT_LABEL_BOLD, FONT_BUTTON, FONT_RESULT, FIELDS,
)
from ui_widgets import make_card, make_scrollable


def build_predict_tab(parent, on_predict, on_clear):
    """
    Builds the "Dự đoán" tab.

    The whole tab content lives inside a scrollable area (see ui_widgets.make_scrollable)
    so that on smaller windows the "DỰ ĐOÁN" button and result box are always reachable
    instead of being cut off below the visible area.

    Returns a dict with the widgets app.py needs to read/update:
    entries, result_var, result_frame, result_label.
    """
    scroll_area = make_scrollable(parent)

    tk.Label(
        scroll_area, text="DỰ ĐOÁN CHẤT LƯỢNG RƯỢU VANG", font=FONT_SECTION,
        bg=COLOR_BG, fg=COLOR_TEXT,
    ).pack(anchor="w", pady=(0, 15), padx=5)

    form_card = make_card(scroll_area)
    form_card.pack(fill="x", padx=5)

    form_inner = tk.Frame(form_card, bg=COLOR_CARD)
    form_inner.pack(fill="both", padx=25, pady=20)

    entries = []
    n_cols = 2

    for idx, (label_text, _placeholder) in enumerate(FIELDS):
        r, c = divmod(idx, n_cols)
        cell = tk.Frame(form_inner, bg=COLOR_CARD)
        cell.grid(row=r, column=c, sticky="w", padx=(0, 40), pady=8)

        tk.Label(
            cell, text=label_text, font=FONT_LABEL_BOLD, bg=COLOR_CARD, fg=COLOR_TEXT,
            width=20, anchor="w",
        ).pack(anchor="w")

        entry = tk.Entry(
            cell, width=22, font=FONT_LABEL, relief="solid", bd=1,
            highlightthickness=1, highlightbackground="#D8C8B8", highlightcolor=COLOR_ACCENT,
        )
        entry.pack(anchor="w", pady=(3, 0), ipady=3)
        entries.append(entry)

    btn_row = tk.Frame(scroll_area, bg=COLOR_BG)
    btn_row.pack(fill="x", pady=15, padx=5)

    tk.Button(
        btn_row, text="🔍  DỰ ĐOÁN", command=on_predict,
        bg=COLOR_ACCENT, fg="white", font=FONT_BUTTON,
        activebackground=COLOR_HEADER, activeforeground="white",
        relief="flat", padx=25, pady=10, cursor="hand2",
    ).pack(side="left")

    tk.Button(
        btn_row, text="Xóa form", command=on_clear,
        bg=COLOR_BG, fg=COLOR_MUTED, font=FONT_LABEL_BOLD,
        activebackground="#F1E6DC", relief="flat", padx=20, pady=10, cursor="hand2",
        highlightbackground="#D8C8B8", highlightthickness=1,
    ).pack(side="left", padx=10)

    result_var = tk.StringVar(value="")
    result_frame = make_card(scroll_area)
    result_frame.pack(fill="x", pady=(5, 20), padx=5)
    result_frame.config(highlightbackground=COLOR_ACCENT, highlightthickness=2)

    result_label = tk.Label(
        result_frame, textvariable=result_var, font=FONT_RESULT,
        bg=COLOR_CARD, fg=COLOR_ACCENT, justify="left", anchor="w",
    )
    result_label.pack(fill="x", padx=20, pady=18)

    return {
        "entries": entries,
        "result_var": result_var,
        "result_frame": result_frame,
        "result_label": result_label,
    }