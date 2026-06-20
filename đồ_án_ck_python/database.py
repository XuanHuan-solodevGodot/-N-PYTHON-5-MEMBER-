import mysql.connector

def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",   # sửa lại
        database="wine_quality_db"
    )