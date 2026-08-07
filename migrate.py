import sqlite3
import os

db_path = os.path.join('instance', 'baby_shower.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()
try:
    c.execute("ALTER TABLE baby_info ADD COLUMN sex VARCHAR(50);")
    conn.commit()
    print("Column added successfully.")
except sqlite3.OperationalError as e:
    print(f"Error (maybe column exists?): {e}")
finally:
    conn.close()
