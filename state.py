import sqlite3
from datetime import datetime, timezone
from config import config

class State:
    def __init__(self):
        self.conn = sqlite3.connect(str(config.db_path))
        self._init_db()

    def _init_db(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS niches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                last_used_at TEXT,
                rotation_order INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                niche TEXT NOT NULL,
                prompts_count INTEGER DEFAULT 0,
                gumroad_product_id TEXT,
                gumroad_url TEXT,
                pinterest_pin_id TEXT,
                status TEXT DEFAULT 'draft',
                created_at TEXT DEFAULT (datetime('now'))
            );
        """)
        self.conn.commit()
        self._seed_niches()

    def _seed_niches(self):
        niches = ["copywriting", "coding", "marketing", "business", "writing", "data-analysis", "learning"]
        for i, n in enumerate(niches):
            self.conn.execute("INSERT OR IGNORE INTO niches (name, rotation_order) VALUES (?, ?)", (n, i))
        self.conn.commit()

    def get_next_niche(self):
        row = self.conn.execute("""
            SELECT name FROM niches
            ORDER BY last_used_at ASC NULLS FIRST, rotation_order ASC
            LIMIT 1
        """).fetchone()
        return row[0] if row else "copywriting"

    def mark_niche_used(self, niche: str):
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute("UPDATE niches SET last_used_at = ? WHERE name = ?", (now, niche))
        self.conn.commit()

    def record_template(self, title: str, niche: str, prompts_count: int,
                        gumroad_id: str = None, gumroad_url: str = None,
                        pinterest_pin_id: str = None, status: str = "published"):
        self.conn.execute("""
            INSERT INTO templates (title, niche, prompts_count, gumroad_product_id,
                                   gumroad_url, pinterest_pin_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, niche, prompts_count, gumroad_id, gumroad_url, pinterest_pin_id, status))
        self.conn.commit()

    def get_recent_templates(self, limit: int = 5):
        return self.conn.execute(
            "SELECT title, niche, created_at FROM templates ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ).fetchall()

state = State()
