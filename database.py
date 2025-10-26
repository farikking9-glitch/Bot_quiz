import sqlite3

DB_FILE = "quiz.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER UNIQUE,
            username TEXT,
            score INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_user(tg_id, username):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (tg_id, username) VALUES (?, ?)", (tg_id, username))
    conn.commit()
    conn.close()

def add_score(tg_id, points):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("UPDATE users SET score = score + ? WHERE tg_id = ?", (points, tg_id))
    conn.commit()
    conn.close()

def get_user_score(tg_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT score FROM users WHERE tg_id = ?", (tg_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0

def get_rating():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT username, score FROM users ORDER BY score DESC LIMIT 10")
    data = cur.fetchall()
    conn.close()
    return data
