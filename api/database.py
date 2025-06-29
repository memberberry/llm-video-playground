import sqlite3
import logging
from typing import List, Union, Dict, Any
from api.models import History
import json, base64

log = logging.getLogger(__name__)

DATABASE_URL = "history.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    try:
        # Enable foreign key support
        conn.execute("PRAGMA foreign_keys = ON")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_name TEXT NOT NULL,
                video_uri TEXT,
                thumbnail BLOB,
                gemini_name TEXT,
                mime_type TEXT NOT NULL,
                size_bytes INTEGER NOT NULL,
                upload_status TEXT NOT NULL DEFAULT 'PROCESSING',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_deleted BOOLEAN DEFAULT FALSE,
                path TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                hash TEXT PRIMARY KEY,
                prompt TEXT NOT NULL,
                model TEXT NOT NULL,
                output TEXT,
                structured_output JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS history_videos (
                history_hash TEXT,
                video_id INTEGER,
                PRIMARY KEY (history_hash, video_id),
                FOREIGN KEY (history_hash) REFERENCES history(hash) ON DELETE CASCADE,
                FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE
            )
        """)
        conn.commit()
    finally:
        conn.close()

def add_video_entry(display_name: str, mime_type: str, size_bytes: int, path: str) -> int:
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO videos (display_name, mime_type, size_bytes, path) VALUES (?, ?, ?, ?)",
            (display_name, mime_type, size_bytes, path)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()



def update_video_upload_success(video_id: int, video_uri: str, thumbnail: bytes, gemini_name: str):
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE videos SET video_uri = ?, thumbnail = ?, gemini_name = ?, upload_status = 'ACTIVE' WHERE id = ?",
            (video_uri, thumbnail, gemini_name, video_id)
        )
        conn.commit()
    finally:
        conn.close()

def update_video_upload_failed(video_id: int):
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE videos SET upload_status = 'FAILED' WHERE id = ?",
            (video_id,)
        )
        conn.commit()
    finally:
        conn.close()


def add_history_entry(prompt: str, model: str, output: str | None, structured_output: Dict[str, Any] | None, video_ids: List[int]):
    import hashlib
    import time

    conn = get_db_connection()
    try:
        structured_output_str = json.dumps(structured_output) if structured_output else None
        
        # Generate a unique hash
        hash_str = hashlib.sha256(f"{prompt}{model}{time.time()}".encode()).hexdigest()

        conn.execute(
            "INSERT INTO history (hash, prompt, model, output, structured_output) VALUES (?, ?, ?, ?, ?)",
            (hash_str, prompt, model, output, structured_output_str)
        )

        if video_ids:
            for video_id in video_ids:
                conn.execute(
                    "INSERT INTO history_videos (history_hash, video_id) VALUES (?, ?)",
                    (hash_str, video_id)
                )
        conn.commit()
    finally:
        conn.close()

def get_history() -> List[History]:
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT h.hash, h.prompt, h.model, h.output, h.structured_output, h.created_at, GROUP_CONCAT(hv.video_id) as videos FROM history h LEFT JOIN history_videos hv ON h.hash = hv.history_hash GROUP BY h.hash ORDER BY h.created_at DESC")
        rows = cursor.fetchall()

        histories = []
        for row in rows:
            row_dict = dict(row)
            if row_dict['videos']:
                row_dict['videos'] = [int(i) for i in row_dict['videos'].split(',')]
            else:
                row_dict['videos'] = []

            if row_dict['structured_output']:
                row_dict['structured_output'] = json.loads(row_dict['structured_output'])
            else:
                row_dict['structured_output'] = None
            histories.append(History(**row_dict))
        return histories
    finally:
        conn.close()

def get_history_with_videos() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            SELECT
                h.*,
                v.id AS vid_id,
                v.display_name,
                v.video_uri,
                v.thumbnail,
                v.gemini_name,
                v.mime_type,
                v.size_bytes,
                v.upload_status,
                v.created_at AS vid_created_at,
                v.is_deleted,
                v.path
            FROM
                history h
            LEFT JOIN
                history_videos hv ON h.hash = hv.history_hash
            LEFT JOIN
                videos v ON hv.video_id = v.id
            ORDER BY
                h.created_at DESC
        """)
        rows = cursor.fetchall()

        results = []
        for row in rows:
            row_dict = dict(row)
            if row_dict['structured_output']:
                row_dict['structured_output'] = json.loads(row_dict['structured_output'])
            
            # Encode thumbnail to base64 if it exists
            if row_dict['thumbnail']:
                import base64
                row_dict['thumbnail'] = base64.b64encode(row_dict['thumbnail']).decode('utf-8')
            
            results.append(row_dict)
        return results
    finally:
        conn.close()

def get_event_from_history_with_videos_by_hash(hash: str) -> Dict[str, Any] | None:
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            SELECT
                h.hash,
                h.prompt,
                h.model,
                h.output,
                h.structured_output,
                h.created_at,
                v.id AS video_id,
                v.display_name,
                v.video_uri,
                v.thumbnail,
                v.gemini_name,
                v.mime_type,
                v.size_bytes,
                v.upload_status,
                v.created_at AS video_created_at,
                v.is_deleted,
                v.path
            FROM
                history h
            LEFT JOIN
                history_videos hv ON h.hash = hv.history_hash
            LEFT JOIN
                videos v ON hv.video_id = v.id
            WHERE
                h.hash = ?
        """, (hash,))
        rows = cursor.fetchall()

        if not rows:
            return None

        history_data = {}
        videos_list = []

        for row in rows:
            if not history_data: # Populate history data from the first row
                history_data = {
                    "hash": row['hash'],
                    "prompt": row['prompt'],
                    "model": row['model'],
                    "output": row['output'],
                    "structured_output": json.loads(row['structured_output']) if row['structured_output'] else None,
                    "created_at": row['created_at'],
                    "videos": [] # Initialize videos list
                }
            
            if row['video_id']: # If there's video data for this row
                video_dict = {
                    "id": row['video_id'],
                    "display_name": row['display_name'],
                    "video_uri": row['video_uri'],
                    "thumbnail": base64.b64encode(row['thumbnail']).decode('utf-8') if row['thumbnail'] else None,
                    "gemini_name": row['gemini_name'],
                    "mime_type": row['mime_type'],
                    "size_bytes": row['size_bytes'],
                    "upload_status": row['upload_status'],
                    "created_at": row['video_created_at'],
                    "is_deleted": bool(row['is_deleted']),
                    "path": row['path']
                }
                videos_list.append(video_dict)
        
        history_data['videos'] = videos_list
        return history_data
    finally:
        conn.close()

def get_videos() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT * FROM videos WHERE is_deleted = FALSE ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def get_video(video_id: int) -> Dict[str, Any] | None:
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT * FROM videos WHERE id = ?", (video_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def delete_video(video_id: int):
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM videos WHERE id = ?", (video_id,))
        conn.commit()
    finally:
        conn.close()

def soft_delete_video(video_id: int):
    conn = get_db_connection()
    try:
        conn.execute("UPDATE videos SET is_deleted = TRUE WHERE id = ?", (video_id,))
        conn.commit()
    finally:
        conn.close()

# Create the tables when the module is loaded
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    log.info("Creating database tables...")
    create_tables()
