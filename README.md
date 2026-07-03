# 🍷 Hệ Thống Phân Tích Chất Lượng Rượu Vang

Ứng dụng desktop (Tkinter) phân loại chất lượng rượu vang bằng mô hình
**Random Forest**, dữ liệu lưu trữ trên **MySQL**.

Dataset sử dụng: [Wine Dataset (UCI)](https://archive.ics.uci.edu/dataset/109/wine) — 178 mẫu, 13 đặc trưng hóa học, 3 class (loại rượu).

---

## 📁 Cấu trúc thư mục

```
wine-quality/
├── app.py                 # Chạy ứng dụng (giao diện chính)
├── config.py               # Màu sắc, font, danh sách 13 trường nhập liệu
├── services.py              # Đọc/ghi MySQL + load & chạy model
├── ui.py                    # Toàn bộ giao diện: 4 tab + component dùng chung
├── database.py              # Kết nối MySQL (host/user/password/database)
├── train.py                 # Huấn luyện model Random Forest
├── test.py                  # Kiểm tra kết nối MySQL nhanh
├── ck.py                    # Kiểm tra đọc dữ liệu wine_data nhanh
├── wine_quality.sql         # Tạo database + 3 bảng
├── wine_data_import.sql     # Nạp 178 mẫu dữ liệu Wine gốc
├── kt.sql                   # Đếm số dòng trong wine_data
└── random_forest.pkl        # Model đã huấn luyện (dùng cho app.py)
```

---

## ⚙️ Yêu cầu

- Python 3.9+
- MySQL Server đang chạy (XAMPP / MySQL Workbench / mysql thuần đều được)

Cài thư viện Python:

```bash
pip install pandas numpy scikit-learn joblib mysql-connector-python
```

> `tkinter` đi kèm sẵn với Python trên Windows; trên Linux nếu thiếu thì cài thêm `sudo apt install python3-tk`.

---

## 🗄️ 1. Thiết lập cơ sở dữ liệu

1. Mở `database.py`, sửa lại `host`, `user`, `password` cho đúng với MySQL trên máy bạn (mặc định là `root` / mật khẩu bạn tự đặt).
2. Tạo database + bảng:

```bash
mysql -u root -p < wine_quality.sql
```

3. Nạp dữ liệu mẫu vào bảng `wine_data`:

```bash
mysql -u root -p wine_quality_db < wine_data_import.sql
```

4. Kiểm tra nhanh đã có dữ liệu chưa:

```bash
mysql -u root -p wine_quality_db < kt.sql
```

Kết quả phải trả về `total_rows = 178`. Nếu bỏ qua bước import, tab **Dashboard**/**Dữ liệu** trong app sẽ hiện cảnh báo "chưa có dữ liệu".

---

## 🧠 2. Huấn luyện model (tùy chọn)

`random_forest.pkl` đã có sẵn trong repo, nhưng nếu muốn huấn luyện lại:

```bash
python train.py
```

Script sẽ đọc dữ liệu từ `wine_data`, huấn luyện `RandomForestClassifier`, in ra độ chính xác, và lưu model mới đè lên `random_forest.pkl`.

---

## ▶️ 3. Chạy ứng dụng

```bash
python app.py
```

Ứng dụng có 4 tab:

| Tab | Chức năng |
|---|---|
| **Dashboard** | Tổng quan: tổng số mẫu, alcohol trung bình, số mẫu theo từng class |
| **Dữ liệu** | Xem toàn bộ dữ liệu trong bảng `wine_data` |
| **Dự đoán** | Nhập 13 chỉ số hóa học → bấm "DỰ ĐOÁN" → xem class + độ tin cậy, tự lưu vào lịch sử |
| **Lịch sử** | Danh sách các lần dự đoán trước đó (lưu trong bảng `prediction_history`) |

---

## 🔧 Kiểm tra nhanh (troubleshooting)

- **Kiểm tra kết nối MySQL:** `python test.py` → in `Connected!` nếu ổn.
- **Kiểm tra đọc dữ liệu:** `python ck.py` → in 5 dòng đầu bảng `wine_data`.
- **App báo "Không kết nối được cơ sở dữ liệu":** kiểm tra lại `host/user/password/database` trong `database.py`, và MySQL server có đang chạy không.
- **App báo "Bảng wine_data đang trống":** chạy lại bước import ở mục 1.3.
- **Lỗi "Không thể tải model random_forest.pkl":** chạy `python train.py` để tạo lại file model, đảm bảo nó nằm cùng thư mục với `app.py`.

---

## 📊 Bảng dữ liệu (MySQL)

- **wine_data** — dữ liệu gốc dùng để huấn luyện/hiển thị (13 đặc trưng + `class_label`)
- **model_results** — kết quả so sánh các thuật toán đã thử (KNN, Decision Tree, Random Forest)
- **prediction_history** — lịch sử mọi lần dự đoán từ tab "Dự đoán" trong app