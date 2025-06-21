import sqlite3
import logging
from typing import List, Union, Dict, Any
from api.models import History
import json

log = logging.getLogger(__name__)

DATABASE_URL = "history.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def create_history_table():
    conn = get_db_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT NOT NULL,
                model TEXT NOT NULL,
                output TEXT,
                structured_output JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                videos TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()

def add_history_entry(prompt: str, model: str, output: str | None, structured_output: Dict[str, Any] | None, videos: List[str]):
    conn = get_db_connection()
    try:
        structured_output = json.dumps(structured_output) if structured_output else None
        videos_str = json.dumps(videos)
        
        conn.execute(
            "INSERT INTO history (prompt, model, output, structured_output, videos) VALUES (?, ?, ?, ?, ?)",
            (prompt, model, output, structured_output, videos_str)
        )
        conn.commit()
    finally:
        conn.close()

def get_history() -> List[History]:
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT * FROM history")
        rows = cursor.fetchall()

        histories = []
        for row in rows:
            row_dict = dict(row)
            row_dict['videos'] = json.loads(row_dict['videos'])
            if row_dict['structured_output']:
                row_dict['structured_output'] = json.loads(row_dict['structured_output'])
            else:
                row_dict['structured_output'] = None
            histories.append(History(**row_dict))
        return histories
    finally:
        conn.close()
    

# Create the table when the module is loaded
create_history_table()
