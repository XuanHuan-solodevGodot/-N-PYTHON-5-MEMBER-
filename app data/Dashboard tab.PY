import tkinter as tk

from config import COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_GOLD, FONT_SECTION, FONT_LABEL, CLASS_COLORS
from ui_widgets import stat_card


def build_dashboard_tab(parent, df, db_error):
    tk.Label(
        parent, text="TỔNG QUAN HỆ THỐNG", font=FONT_SECTION,
        bg=COLOR_BG, fg=COLOR_TEXT,
    ).pack(anchor="w", pady=(15, 5), padx=5)

    if db_error:
        _warning(
            parent,
            "⚠ Không kết nối được MySQL. Kiểm tra lại database.py "
            f"(host / user / password / database).\nChi tiết lỗi: {db_error}"
        )
    elif len(df) == 0:
        _warning(
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
            stat_card(
                cards_frame, f"Class {cls}", str(count),
                CLASS_COLORS.get(int(cls), COLOR_ACCENT), 2 + idx
            )


def _warning(parent, text):
    warn = tk.Frame(parent, bg="#FBE7C6", highlightbackground="#E0A800", highlightthickness=1)
    warn.pack(fill="x", padx=5, pady=10)
    tk.Label(
        warn, text=text, font=FONT_LABEL, bg="#FBE7C6", fg="#7A4B00",
        justify="left", wraplength=1150,
    ).pack(padx=15, pady=10, anchor="w")