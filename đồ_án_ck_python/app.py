import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd
import numpy as np
import joblib

from database import get_connection

# =====================================
# LOAD DATA
# =====================================

conn = get_connection()

df = pd.read_sql(
    "SELECT * FROM wine_data",
    conn
)

conn.close()

model = joblib.load("random_forest.pkl")

# =====================================
# FUNCTIONS
# =====================================

def load_history():

    for item in history_tree.get_children():
        history_tree.delete(item)

    conn = get_connection()

    query = """
    SELECT *
    FROM prediction_history
    ORDER BY prediction_id DESC
    """

    history_df = pd.read_sql(query, conn)

    conn.close()

    for _, row in history_df.iterrows():

        history_tree.insert(
            "",
            "end",
            values=list(row)
        )


def predict_wine():

    try:

        values = []

        for entry in entries:

            values.append(
                float(entry.get())
            )

        data = np.array([values])

        prediction = model.predict(data)[0]

        probability = max(
            model.predict_proba(data)[0]
        ) * 100

        result_label.config(
            text=
            f"Loại rượu: Class {prediction}\n"
            f"Độ tin cậy: {probability:.2f}%"
        )

        # Lưu MySQL

        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        INSERT INTO prediction_history(
        alcohol,
        malic_acid,
        ash,
        alcalinity_of_ash,
        magnesium,
        total_phenols,
        flavanoids,
        nonflavanoid_phenols,
        proanthocyanins,
        color_intensity,
        hue,
        od280_od315,
        proline,
        predicted_class,
        confidence_score
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (
                values[0],
                values[1],
                values[2],
                values[3],
                values[4],
                values[5],
                values[6],
                values[7],
                values[8],
                values[9],
                values[10],
                values[11],
                values[12],
                int(prediction),
                float(probability)
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        load_history()

    except Exception as e:

        messagebox.showerror(
            "Lỗi",
            str(e)
        )


# =====================================
# WINDOW
# =====================================

root = tk.Tk()

root.title(
    "Hệ thống phân tích chất lượng rượu vang"
)

root.geometry("1300x750")

# =====================================
# TITLE
# =====================================

title = tk.Label(
    root,
    text="HỆ THỐNG PHÂN TÍCH CHẤT LƯỢNG RƯỢU VANG",
    font=("Arial",18,"bold")
)

title.pack(pady=10)

# =====================================
# NOTEBOOK
# =====================================

notebook = ttk.Notebook(root)

notebook.pack(
    fill="both",
    expand=True
)

tab_dashboard = ttk.Frame(notebook)
tab_data = ttk.Frame(notebook)
tab_predict = ttk.Frame(notebook)
tab_history = ttk.Frame(notebook)

notebook.add(tab_dashboard,text="Dashboard")
notebook.add(tab_data,text="Dữ liệu")
notebook.add(tab_predict,text="Dự đoán")
notebook.add(tab_history,text="Lịch sử")

# =====================================
# DASHBOARD
# =====================================

tk.Label(
    tab_dashboard,
    text="TỔNG QUAN HỆ THỐNG",
    font=("Arial",16,"bold")
).pack(pady=20)

tk.Label(
    tab_dashboard,
    text=f"Tổng số mẫu: {len(df)}",
    font=("Arial",14)
).pack()

avg_alcohol = round(
    df["alcohol"].mean(),
    2
)

tk.Label(
    tab_dashboard,
    text=f"Alcohol trung bình: {avg_alcohol}",
    font=("Arial",12)
).pack(pady=5)

class_count = df["class_label"].value_counts()

for cls,count in class_count.items():

    tk.Label(
        tab_dashboard,
        text=f"Class {cls}: {count} mẫu",
        font=("Arial",12)
    ).pack()

# =====================================
# DATA TAB
# =====================================

data_frame = tk.Frame(tab_data)

data_frame.pack(
    fill="both",
    expand=True
)

columns = list(df.columns)

tree = ttk.Treeview(
    data_frame,
    columns=columns,
    show="headings"
)

for col in columns:

    tree.heading(
        col,
        text=col
    )

    tree.column(
        col,
        width=100
    )

for _, row in df.iterrows():

    tree.insert(
        "",
        "end",
        values=list(row)
    )

scroll_y = ttk.Scrollbar(
    data_frame,
    orient="vertical",
    command=tree.yview
)

tree.configure(
    yscrollcommand=scroll_y.set
)

tree.pack(
    side="left",
    fill="both",
    expand=True
)

scroll_y.pack(
    side="right",
    fill="y"
)

# =====================================
# PREDICT TAB
# =====================================

fields = [
    "Alcohol",
    "Malic Acid",
    "Ash",
    "Alcalinity of Ash",
    "Magnesium",
    "Total Phenols",
    "Flavanoids",
    "Nonflavanoid Phenols",
    "Proanthocyanins",
    "Color Intensity",
    "Hue",
    "OD280/OD315",
    "Proline"
]

entries = []

for field in fields:

    frame = tk.Frame(tab_predict)

    frame.pack(
        pady=3
    )

    tk.Label(
        frame,
        text=field,
        width=25,
        anchor="w"
    ).pack(side="left")

    entry = tk.Entry(
        frame,
        width=20
    )

    entry.pack(side="left")

    entries.append(entry)

btn_predict = tk.Button(
    tab_predict,
    text="DỰ ĐOÁN",
    command=predict_wine,
    bg="lightgreen",
    font=("Arial",12,"bold")
)

btn_predict.pack(
    pady=10
)

result_label = tk.Label(
    tab_predict,
    text="",
    font=("Arial",14,"bold")
)

result_label.pack(
    pady=15
)

# =====================================
# HISTORY TAB
# =====================================

history_columns = (
    "prediction_id",
    "predicted_class",
    "confidence_score",
    "prediction_time"
)

history_tree = ttk.Treeview(
    tab_history,
    columns=history_columns,
    show="headings"
)

for col in history_columns:

    history_tree.heading(
        col,
        text=col
    )

    history_tree.column(
        col,
        width=200
    )

history_tree.pack(
    fill="both",
    expand=True
)

load_history()

# =====================================

root.mainloop()