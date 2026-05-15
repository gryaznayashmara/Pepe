import sqlite3
from config import DB_PATH

class MusicDB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.init()

    def init(self):
        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS music (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            artist TEXT DEFAULT '',
            file_id TEXT UNIQUE,
            plays INTEGER DEFAULT 0
        )
        """)

        self.conn.commit()

    def search(self, query):
        cur = self.conn.cursor()

        q = f"%{query}%"

        cur.execute("""
            SELECT id, title, artist, file_id, plays
            FROM music
            WHERE title LIKE ? OR artist LIKE ?
            ORDER BY plays DESC
            LIMIT 10
        """, (q, q))

        return cur.fetchall()

    def get(self, music_id):
        cur = self.conn.cursor()

        cur.execute("""
            SELECT id, title, artist, file_id, plays
            FROM music WHERE id = ?
        """, (music_id,))

        return cur.fetchone()

    def add_play(self, music_id):
        cur = self.conn.cursor()

        cur.execute("""
            UPDATE music
            SET plays = plays + 1
            WHERE id = ?
        """, (music_id,))

        self.conn.commit()