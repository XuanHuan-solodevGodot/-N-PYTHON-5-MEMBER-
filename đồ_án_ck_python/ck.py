import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",  # sửa theo máy bạn
    database="wine_quality_db"
)

query = "SELECT * FROM wine_data"

df = pd.read_sql(query, conn)

print(df.head())