import sqlite3

def migrate():
    conn = sqlite3.connect('instance/baby_shower.db')
    cursor = conn.cursor()
    
    # Check FormConfig columns
    cursor.execute("PRAGMA table_info(form_config)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'max_names' not in columns:
        print("Adding max_names to form_config...")
        cursor.execute("ALTER TABLE form_config ADD COLUMN max_names INTEGER DEFAULT 3")
    
    # Check Guess columns
    cursor.execute("PRAGMA table_info(guess)")
    columns = [col[1] for col in cursor.fetchall()]
    
    for i in range(4, 11):
        col_name = f'first_name_{i}'
        if col_name not in columns:
            print(f"Adding {col_name} to guess...")
            cursor.execute(f"ALTER TABLE guess ADD COLUMN {col_name} VARCHAR(150)")
            
    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == '__main__':
    migrate()
