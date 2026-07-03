import tkinter as tk
from tkinter import ttk, messagebox

from config import (
    COLOR_BG, COLOR_HEADER, COLOR_HEADER_TEXT, COLOR_CARD, COLOR_MUTED,
    FONT_TITLE, FONT_SUBTITLE, FONT_LABEL_BOLD, CLASS_COLORS, COLOR_ACCENT, FIELDS,
)
from services import load_wine_data, load_prediction_history, save_prediction, load_model, predict_wine_class
from ui import style_treeview, build_dashboard_tab, build_data_tab, build_predict_tab, build_history_tab

# =====================================
# LOAD DATA & MODEL
# =====================================

df, db_error = load_wine_data()
model, model_error = load_model("random_forest.pkl")

# =====================================
# WINDOW
# =====================================

root = tk.Tk()
root.title("Hệ thống phân tích chất lượng rượu vang")
root.geometry("1300x780")
root.minsize(1000, 650)
root.configure(bg=COLOR_BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
style.configure(
    "TNotebook.Tab", background=COLOR_BG, foreground=COLOR_MUTED,
    padding=[18, 10], font=FONT_LABEL_BOLD, borderwidth=0,
)
style.map(
    "TNotebook.Tab",
    background=[("selected", COLOR_CARD)],
    foreground=[("selected", COLOR_ACCENT)],
)
style_treeview()

# =====================================
# HEADER
# =====================================

header = tk.Frame(root, bg=COLOR_HEADER, height=90)
header.pack(fill="x", side="top")
header.pack_propagate(False)

tk.Label(
    header, text="🍷  HỆ THỐNG PHÂN TÍCH CHẤT LƯỢNG RƯỢU VANG",
    font=FONT_TITLE, bg=COLOR_HEADER, fg=COLOR_HEADER_TEXT,
).pack(side="left", padx=30, pady=(18, 0))

tk.Label(
    header, text="Wine Quality Classification  •  Random Forest",
    font=FONT_SUBTITLE, bg=COLOR_HEADER, fg="#D8B9A6",
).pack(side="left", padx=30, anchor="w")

if db_error:
    tk.Label(
        header, text="⚠ Không kết nối được cơ sở dữ liệu",
        font=FONT_LABEL_BOLD, bg=COLOR_HEADER, fg="#FFD27F",
    ).pack(side="right", padx=30)

# =====================================
# TABS
# =====================================

outer = tk.Frame(root, bg=COLOR_BG)
outer.pack(fill="both", expand=True, padx=20, pady=15)

notebook = ttk.Notebook(outer)
notebook.pack(fill="both", expand=True)

tab_dashboard = tk.Frame(notebook, bg=COLOR_BG)
tab_data = tk.Frame(notebook, bg=COLOR_BG)
tab_predict = tk.Frame(notebook, bg=COLOR_BG)
tab_history = tk.Frame(notebook, bg=COLOR_BG)

notebook.add(tab_dashboard, text="  Dashboard  ")
notebook.add(tab_data, text="  Dữ liệu  ")
notebook.add(tab_predict, text="  Dự đoán  ")
notebook.add(tab_history, text="  Lịch sử  ")

build_dashboard_tab(tab_dashboard, df, db_error)
build_data_tab(tab_data, df)
history_tree = build_history_tab(tab_history, db_error)


# =====================================
# PREDICT LOGIC
# =====================================

def refresh_history():
    for item in history_tree.get_children():
        history_tree.delete(item)

    history_df, err = load_prediction_history()
    if err:
        messagebox.showerror("Lỗi kết nối", f"Không thể tải lịch sử:\n{err}")
        return

    for i, (_, row) in enumerate(history_df.iterrows()):
        history_tree.insert("", "end", values=list(row), tags=("odd" if i % 2 else "even",))


def handle_predict():
    if model is None:
        messagebox.showerror("Lỗi mô hình", f"Không thể tải model random_forest.pkl:\n{model_error}")
        return

    try:
        values = []
        for i, entry in enumerate(predict_widgets["entries"]):
            raw = entry.get().strip()
            if raw == "":
                raise ValueError(f"Vui lòng nhập giá trị cho '{FIELDS[i]}'")
            values.append(float(raw))

        prediction, probability = predict_wine_class(model, values)

        predict_widgets["result_var"].set(
            f"Loại rượu dự đoán:  Class {prediction}\nĐộ tin cậy:  {probability:.2f}%"
        )
        color = CLASS_COLORS.get(int(prediction), COLOR_ACCENT)
        predict_widgets["result_frame"].config(highlightbackground=color)
        predict_widgets["result_label"].config(fg=color)

        save_prediction(values, prediction, probability)
        refresh_history()

    except ValueError as e:
        messagebox.showerror("Thiếu dữ liệu", str(e))
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


def handle_clear():
    for entry in predict_widgets["entries"]:
        entry.delete(0, tk.END)
    predict_widgets["result_var"].set("")


predict_widgets = build_predict_tab(tab_predict, handle_predict, handle_clear)

if not db_error:
    refresh_history()

# =====================================
root.mainloop()
