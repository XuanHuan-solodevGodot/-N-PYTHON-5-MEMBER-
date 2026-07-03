import tkinter as tk
from tkinter import ttk

from config import COLOR_BG, COLOR_TEXT, COLOR_CARD, COLOR_MUTED, COLOR_ROW_ALT, FONT_SECTION, FONT_LABEL
from ui_widgets import make_card

HISTORY_COLUMNS = ("prediction_id", "predicted_class", "confidence_score", "prediction_time")

COL_LABELS = {
    "prediction_id": "ID",
    "predicted_class": "Loại rượu",
    "confidence_score": "Độ tin cậy (%)",
    "prediction_time": "Thời gian",
}


def build_history_tab(parent, db_error):
    tk.Label(
        parent, text="LỊCH SỬ DỰ ĐOÁN", font=FONT_SECTION,
        bg=COLOR_BG, fg=COLOR_TEXT,
    ).pack(anchor="w", pady=(15, 10), padx=5)

    history_card = make_card(parent)
    history_card.pack(fill="both", expand=True, padx=5, pady=(0, 10))

    history_frame = tk.Frame(history_card, bg=COLOR_CARD)
    history_frame.pack(fill="both", expand=True, padx=2, pady=2)

    tree = ttk.Treeview(
        history_frame, columns=HISTORY_COLUMNS, show="headings", style="Custom.Treeview"
    )

    for col in HISTORY_COLUMNS:
        tree.heading(col, text=COL_LABELS[col])
        tree.column(col, width=250, anchor="center")

    tree.tag_configure("even", background=COLOR_CARD)
    tree.tag_configure("odd", background=COLOR_ROW_ALT)

    scroll_y = ttk.Scrollbar(history_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)

    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")

    history_frame.grid_rowconfigure(0, weight=1)
    history_frame.grid_columnconfigure(0, weight=1)

    if db_error:
        tk.Label(
            history_card, text="Không thể tải lịch sử do lỗi kết nối cơ sở dữ liệu.",
            font=FONT_LABEL, bg=COLOR_CARD, fg=COLOR_MUTED,
        ).pack(pady=20)

    return tree