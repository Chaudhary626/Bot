import sqlite3
from config import DB_FILE

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        # Users
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            status TEXT DEFAULT 'idle',
            warnings INTEGER DEFAULT 0,
            blocked INTEGER DEFAULT 0,
            is_admin INTEGER DEFAULT 0,
            video_link TEXT,
            video_title TEXT,
            video_thumb TEXT,
            paired_with INTEGER,
            task_start DATETIME,
            last_action DATETIME
        )""")
        # Proofs
        c.execute("""
        CREATE TABLE IF NOT EXISTS proofs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user INTEGER,
            to_user INTEGER,
            proof_file TEXT,
            proof_type TEXT,
            submitted_at DATETIME,
            verified INTEGER DEFAULT 0,
            rejected INTEGER DEFAULT 0
        )""")
        # Admin logs
        c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER,
            action TEXT,
            target_user INTEGER,
            at DATETIME
        )""")
        conn.commit()

def db_query(q, args=(), one=False, commit=False):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(q, args)
        res = None
        if commit:
            conn.commit()
        else:
            res = c.fetchone() if one else c.fetchall()
        return res