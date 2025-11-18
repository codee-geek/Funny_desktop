import sqlite3
from datetime import datetime
import os
import threading

DB_PATH = os.path.join(os.path.dirname(__file__), "roaster.db")
MAX_MESSAGES = 200
_db_lock = threading.Lock()  # Thread-safe database access


def init_db():
    """Initialize the database with chat_history table."""
    with _db_lock:
        try:
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)

            # Create index for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON chat_history(timestamp DESC)
            """)

            conn.commit()
            conn.close()
            print("[DB] Database initialized:", DB_PATH)
        except Exception as e:
            print(f"[DB] Error initializing database: {e}")


def insert_message(role, message):
    """Insert a message and prune older ones. Thread-safe."""
    if not message or not message.strip():
        return
    
    with _db_lock:
        try:
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO chat_history (role, message, timestamp)
                VALUES (?, ?, ?)
            """, (role, message.strip(), datetime.now().isoformat()))

            # Prune older rows, keep only the newest MAX_MESSAGES
            cursor.execute("""
                DELETE FROM chat_history
                WHERE id NOT IN (
                    SELECT id FROM chat_history
                    ORDER BY id DESC
                    LIMIT ?
                )
            """, (MAX_MESSAGES,))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[DB] Error inserting message: {e}")


def get_recent_messages(limit=50):
    """Get recent messages from database. Thread-safe."""
    with _db_lock:
        try:
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
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
        except Exception as e:
            print(f"[DB] Error getting messages: {e}")
            return []
