import sqlite3

def create_records_table():
    conn = sqlite3.connect('records.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_record(name, score):
    conn = sqlite3.connect('records.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO records (name, score) VALUES (?, ?)
    ''', (name, score))
    conn.commit()
    conn.close()

def get_records():
    conn = sqlite3.connect('records.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM records ORDER BY score DESC LIMIT 10')
    records = cursor.fetchall()
    conn.close()
    return records

def initialize_database():
    create_records_table()

# Инициализация базы данных
initialize_database()
