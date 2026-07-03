"""
Toàn bộ phần giao diện: các thành phần dùng chung (card, bảng, khung cuộn)
và 4 hàm build_..._tab() để dựng từng tab. app.py chỉ gọi các hàm này.
"""

import tkinter as tk
from tkinter import ttk

from config import (
    COLOR_BG, COLOR_HEADER, COLOR_ACCENT, COLOR_GOLD, COLOR_CARD,
    COLOR_TEXT, COLOR_MUTED, COLOR_ROW_ALT, CLASS_COLORS,
    FONT_LABEL, FONT_LABEL_BOLD, FONT_SECTION, FONT_BUTTON, FONT_RESULT,
    FONT_STAT_NUM, FONT_STAT_LABEL, FEATURE_COLUMNS, FIELDS,
)

# =====================================
# SHARED WIDGETS
# =====================================

def style_treeview(tree_name="Custom.Treeview", rowheight=28):
    style = ttk.Style()
    style.configure(
        tree_name, background=COLOR_CARD, fieldbackground=COLOR_CARD,
        foreground=COLOR_TEXT, rowheight=rowheight, font=FONT_LABEL, borderwidth=0,
    )
    style.configure(
        tree_name + ".Heading", background=COLOR_ACCENT, foreground="white",
        font=FONT_LABEL_BOLD, relief="flat",
    )
    style.map(tree_name + ".Heading", background=[("active", COLOR_HEADER)])
    style.map(
        tree_name,
        background=[("selected", COLOR_GOLD)],
        foreground=[("selected", COLOR_TEXT)],
    )


def make_card(parent, **kwargs):
    return tk.Frame(
        parent, bg=COLOR_CARD, highlightbackground="#E3D6C8",
        highlightthickness=1, **kwargs
    )


def stat_card(parent, title, value, color, col):
    card = make_card(parent, width=260, height=110)
    card.grid(row=0, column=col, padx=(0, 15), sticky="nsew")
    card.grid_propagate(False)
    tk.Frame(card, bg=color, width=6).pack(side="left", fill="y")
    inner = tk.Frame(card, bg=COLOR_CARD)
    inner.pack(side="left", fill="both", expand=True, padx=15, pady=10)
    tk.Label(inner, text=value, font=FONT_STAT_NUM, bg=COLOR_CARD, fg=color).pack(anchor="w")
    tk.Label(inner, text=title, font=FONT_STAT_LABEL, bg=COLOR_CARD, fg=COLOR_MUTED).pack(anchor="w")


def make_scrollable(parent, bg=COLOR_BG):
    """Khung cuộn dọc - dùng cho tab Dự đoán để nút bấm không bao giờ bị cắt mất."""
    canvas = tk.Canvas(parent, bg=bg, highlightthickness=0)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=bg)

    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

    def _wheel(e):
        canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _wheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return inner


def warning_box(parent, text):
    warn = tk.Frame(parent, bg="#FBE7C6", highlightbackground="#E0A800", highlightthickness=1)
    warn.pack(fill="x", padx=5, pady=10)
    tk.Label(
        warn, text=text, font=FONT_LABEL, bg="#FBE7C6", fg="#7A4B00",
        justify="left", wraplength=1150,
    ).pack(padx=15, pady=10, anchor="w")


# =====================================
# DASHBOARD TAB
# =====================================

def build_dashboard_tab(parent, df, db_error):
    tk.Label(
        parent, text="TỔNG QUAN HỆ THỐNG", font=FONT_SECTION, bg=COLOR_BG, fg=COLOR_TEXT,
    ).pack(anchor="w", pady=(15, 5), padx=5)

    if db_error:
        warning_box(
            parent,
            "⚠ Không kết nối được MySQL. Kiểm tra lại database.py "
            f"(host / user / password / database).\nChi tiết lỗi: {db_error}"
        )
    elif len(df) == 0:
        warning_box(
            parent,
            "⚠ Bảng 'wine_data' đang trống. Hãy chạy file wine_data_import.sql "
            "(vd: mysql -u root -p wine_quality_db < wine_data_import.sql) rồi mở lại ứng dụng."
        )

    cards_frame = tk.Frame(parent, bg=COLOR_BG)
    cards_frame.pack(fill="x", padx=5, pady=10)

    total_samples = len(df)
    avg_alcohol = round(df["alcohol"].mean(), 2) if total_samples and "alcohol" in df else "—"

    stat_card(cards_frame, "Tổng số mẫu", str(total_samples), COLOR_ACCENT, 0)
    stat_card(cards_frame, "Alcohol trung bình", str(avg_alcohol), COLOR_GOLD, 1)

    if total_samples and "class_label" in df:
        class_count = df["class_label"].value_counts().sort_index()
        for idx, (cls, count) in enumerate(class_count.items()):
            stat_card(cards_frame, f"Class {cls}", str(count), CLASS_COLORS.get(int(cls), COLOR_ACCENT), 2 + idx)


# =====================================
# DATA TAB
# =====================================

def build_data_tab(parent, df):
    tk.Label(
        parent, text="DỮ LIỆU RƯỢU VANG", font=FONT_SECTION, bg=COLOR_BG, fg=COLOR_TEXT,
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
        tree.insert("", "end", values=list(row), tags=("odd" if i % 2 else "even",))

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


# =====================================
# PREDICT TAB
# =====================================

def build_predict_tab(parent, on_predict, on_clear):
    """
    Trả về dict widget để app.py đọc/ghi: entries, result_var, result_frame, result_label.
    Bọc trong khung cuộn (make_scrollable) để nút DỰ ĐOÁN không bao giờ bị khuất
    kể cả khi cửa sổ nhỏ.
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

    for idx, label_text in enumerate(FIELDS):
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


# =====================================
# HISTORY TAB
# =====================================

HISTORY_COLUMNS = ("prediction_id", "predicted_class", "confidence_score", "prediction_time")
HISTORY_COL_LABELS = {
    "prediction_id": "ID",
    "predicted_class": "Loại rượu",
    "confidence_score": "Độ tin cậy (%)",
    "prediction_time": "Thời gian",
}


def build_history_tab(parent, db_error):
    tk.Label(
        parent, text="LỊCH SỬ DỰ ĐOÁN", font=FONT_SECTION, bg=COLOR_BG, fg=COLOR_TEXT,
    ).pack(anchor="w", pady=(15, 10), padx=5)

    history_card = make_card(parent)
    history_card.pack(fill="both", expand=True, padx=5, pady=(0, 10))
    history_frame = tk.Frame(history_card, bg=COLOR_CARD)
    history_frame.pack(fill="both", expand=True, padx=2, pady=2)

    tree = ttk.Treeview(history_frame, columns=HISTORY_COLUMNS, show="headings", style="Custom.Treeview")

    for col in HISTORY_COLUMNS:
        tree.heading(col, text=HISTORY_COL_LABELS[col])
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
