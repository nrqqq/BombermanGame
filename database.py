import sqlite3

def create_table():
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            name TEXT PRIMARY KEY,
            score INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_score(name, score):
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()

    cursor.execute("SELECT score FROM scores WHERE name = ?", (name,))
    result = cursor.fetchone()

    if result:
        current_score = result[0]
        if score > current_score:
            cursor.execute("UPDATE scores SET score = ? WHERE name = ?", (score, name))
    else:
        cursor.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))

    conn.commit()
    conn.close()

def get_top_scores(limit=10):
    conn = sqlite3.connect("scores.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT ?", (limit,))
    top_scores = cursor.fetchall()
    conn.close()
    return top_scores
