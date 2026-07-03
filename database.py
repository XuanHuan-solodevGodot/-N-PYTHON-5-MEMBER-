import mysql.connector

def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Koyboy2605#",   # sửa lại
        database="wine_quality_db"
    )