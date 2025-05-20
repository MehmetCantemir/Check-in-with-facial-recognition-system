import sqlite3

def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            midterm TEXT NOT NULL,
            final TEXT NOT NULL,
            student_number TEXT NOT NULL,
            folder_path TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    
    
create_database()