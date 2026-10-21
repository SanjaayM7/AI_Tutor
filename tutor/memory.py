import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "tutor_data.db"

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY CHECK (id=1), data TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS turns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT NOT NULL, role TEXT NOT NULL, content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        c.execute("INSERT OR IGNORE INTO profile(id, data) VALUES(1, ?)", (json.dumps({
            "name": "", "topic": "Python fundamentals", "level": "Beginner",
            "goal": "Understand the fundamentals and solve practical problems"
        }),))

def get_profile():
    with connect() as c:
        row = c.execute("SELECT data FROM profile WHERE id=1").fetchone()
    return json.loads(row["data"]) if row else {}

def save_profile(profile):
    with connect() as c:
        c.execute("INSERT OR REPLACE INTO profile(id, data) VALUES(1, ?)", (json.dumps(profile),))

def add_turn(channel, role, content):
    with connect() as c:
        c.execute("INSERT INTO turns(channel, role, content) VALUES(?, ?, ?)", (channel, role, content))

def get_recent_history(channel, limit=12):
    with connect() as c:
        rows = c.execute("SELECT role, content FROM turns WHERE channel=? ORDER BY id DESC LIMIT ?", (channel, limit)).fetchall()
    return [dict(r) for r in reversed(rows)]
