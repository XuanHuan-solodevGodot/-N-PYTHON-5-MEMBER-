from database import get_connection

conn = get_connection()

print("Connected!")

conn.close()