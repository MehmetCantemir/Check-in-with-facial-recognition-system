import sqlite3

conn = sqlite3.connect("login_logs.db")  # İstersen "users.db" ile aynı dosyaya da ekleyebilirsin
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS giris_kayitlari (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        surname TEXT,
        login_time TEXT
    )
''')
conn.commit()
conn.close()



