import sqlite3
import os

db_path = os.path.join('instance', 'baby_shower.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()
try:
    c.execute("ALTER TABLE form_config ADD COLUMN lock_sex BOOLEAN NOT NULL DEFAULT 0;")
    conn.commit()
    print("Column lock_sex added successfully.")
except sqlite3.OperationalError as e:
    print(f"Error (maybe column exists?): {e}")
finally:
    conn.close()
