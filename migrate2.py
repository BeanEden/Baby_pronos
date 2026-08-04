import sqlite3
import os

db_path = os.path.join('instance', 'baby_shower.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()
try:
    c.execute("""
    CREATE TABLE form_config (
        id INTEGER PRIMARY KEY,
        show_dob BOOLEAN NOT NULL,
        show_sex BOOLEAN NOT NULL,
        show_first_name BOOLEAN NOT NULL,
        show_height BOOLEAN NOT NULL,
        show_weight BOOLEAN NOT NULL,
        show_skin_color BOOLEAN NOT NULL,
        show_eye_color BOOLEAN NOT NULL,
        show_hair_color BOOLEAN NOT NULL,
        show_hints BOOLEAN NOT NULL
    )
    """)
    # Insert default config
    c.execute("""
    INSERT INTO form_config (id, show_dob, show_sex, show_first_name, show_height, show_weight, show_skin_color, show_eye_color, show_hair_color, show_hints)
    VALUES (1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    """)
    conn.commit()
    print("Table form_config created successfully.")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")
finally:
    conn.close()
