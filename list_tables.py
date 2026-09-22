import sqlite3

def list_tables():
    conn = sqlite3.connect('baby_shower.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())
    conn.close()

if __name__ == '__main__':
    list_tables()
