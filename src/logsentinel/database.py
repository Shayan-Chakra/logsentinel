import sqlite3
from datetime import datetime

DB_PATH = "logsentinel.db"


def connect(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            last_seen TEXT NOT NULL,
            occurrences INTEGER NOT NULL DEFAULT 1,
            rule TEXT NOT NULL,
            ip TEXT,
            username TEXT,
            count INTEGER,
            failures INTEGER
        )"""
    )
    return conn


def save_alerts(alerts, path=DB_PATH):
    """Save alerts. Returns (new_count, repeated_count)."""
    conn = connect(path)
    now = datetime.now().isoformat(timespec="seconds")
    new, repeated = 0, 0

    for a in alerts:
        ip = a.get("ip")
        user = a.get("user")

        # "IS ?" also works when the value is empty (None)
        row = conn.execute(
            "SELECT id FROM alerts WHERE rule = ? AND ip IS ? AND username IS ?",
            (a["rule"], ip, user),
        ).fetchone()

        if row:
            conn.execute(
                "UPDATE alerts SET occurrences = occurrences + 1, last_seen = ? WHERE id = ?",
                (now, row[0]),
            )
            repeated += 1
        else:
            conn.execute(
                "INSERT INTO alerts (created_at, last_seen, rule, ip, username, count, failures) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (now, now, a["rule"], ip, user, a.get("count"), a.get("failures")),
            )
            new += 1

    conn.commit()
    conn.close()
    return new, repeated


def get_alerts(limit=100, path=DB_PATH):
    conn = connect(path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM alerts ORDER BY last_seen DESC, id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]