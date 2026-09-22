import sqlite3
import os

DB_PATH = os.path.join('instance', 'baby_shower.db')

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Add time_of_birth to baby_info
        cursor.execute("ALTER TABLE baby_info ADD COLUMN time_of_birth TIME")
        print("Added time_of_birth to baby_info")
    except sqlite3.OperationalError as e:
        print(f"Notice: {e}")

    try:
        # Add time_of_birth to guess
        cursor.execute("ALTER TABLE guess ADD COLUMN time_of_birth TIME")
        print("Added time_of_birth to guess")
    except sqlite3.OperationalError as e:
        print(f"Notice: {e}")

    try:
        # Add show_time to form_config
        cursor.execute("ALTER TABLE form_config ADD COLUMN show_time BOOLEAN DEFAULT 1")
        print("Added show_time to form_config")
    except sqlite3.OperationalError as e:
        print(f"Notice: {e}")

    try:
        # Add table_show_time to form_config
        cursor.execute("ALTER TABLE form_config ADD COLUMN table_show_time BOOLEAN DEFAULT 1")
        print("Added table_show_time to form_config")
    except sqlite3.OperationalError as e:
        print(f"Notice: {e}")

    conn.commit()
    conn.close()
    print("Migration completed.")

if __name__ == '__main__':
    migrate()
