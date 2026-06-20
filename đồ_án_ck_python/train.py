import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Kết nối MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",  # đổi theo máy bạn
    database="wine_quality_db"
)

# Đọc dữ liệu
df = pd.read_sql("SELECT * FROM wine_data", conn)

# Xóa cột không cần thiết
X = df.drop(
    columns=[
        'id',
        'class_label',
        'created_at'
    ]
)

y = df['class_label']

# Chia dữ liệu
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Huấn luyện
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Dự đoán
y_pred = model.predict(X_test)

print("Accuracy =", accuracy_score(y_test, y_pred))

print(classification_report(
    y_test,
    y_pred
))

# Lưu model
joblib.dump(
    model,
    "random_forest.pkl"
)

print("Model saved!")