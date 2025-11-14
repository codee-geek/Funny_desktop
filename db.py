import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "roaster.db")
MAX_MESSAGES = 200


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("[DB] Database initialized:", DB_PATH)


def insert_message(role, message):
    """Insert a message and prune older ones."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_history (role, message, timestamp)
        VALUES (?, ?, ?)
    """, (role, message, datetime.now().isoformat()))

    # prune older rows, keep only the newest MAX_MESSAGES
    cursor.execute(f"""
        DELETE FROM chat_history
        WHERE id NOT IN (
            SELECT id FROM chat_history
            ORDER BY id DESC
            LIMIT {MAX_MESSAGES}
        )
    """)

    conn.commit()
    conn.close()


def get_recent_messages(limit=50):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, message, timestamp
        FROM chat_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return list(reversed(rows))
