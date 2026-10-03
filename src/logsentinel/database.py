import sqlite3
from datetime import datetime

DB_PATH = "logsentinel.db"


def connect(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            rule TEXT NOT NULL,
            ip TEXT,
            username TEXT,
            count INTEGER,
            failures INTEGER
        )"""
    )
    return conn


def save_alerts(alerts, path=DB_PATH):
    conn = connect(path)
    now = datetime.now().isoformat(timespec="seconds")
    for a in alerts:
        conn.execute(
            "INSERT INTO alerts (created_at, rule, ip, username, count, failures) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (now, a["rule"], a.get("ip"), a.get("user"), a.get("count"), a.get("failures")),
        )
    conn.commit()
    conn.close()


def get_alerts(limit=100, path=DB_PATH):
    conn = connect(path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM alerts ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]