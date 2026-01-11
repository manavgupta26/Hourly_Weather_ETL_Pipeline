import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "weather.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM weather_data").fetchall()

for row in rows:
    print(row)

conn.close()
