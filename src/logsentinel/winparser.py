import csv
from datetime import datetime
from pathlib import Path

IGNORED_IPS = {"", "-", "::1", "127.0.0.1", "0.0.0.0"}


def rows_to_events(rows):
    """Turn Windows logon rows into the same events the SSH parser produces.

    Each row needs: Time, EventId, User, Ip, LogonType.
    4625 = failed logon. 4624 = successful logon (only network/remote types 3 and 10).
    """
    events = []

    for row in rows:
        ip = str(row.get("Ip") or "").strip()
        if ip.lower().startswith("::ffff:"):  # IPv4 written in IPv6 style
            ip = ip[7:]
        if ip in IGNORED_IPS:
            ip = "LOCAL"   # attempt made on this PC itself, not from the network

        event_id = str(row.get("EventId") or "").strip()
        logon_type = str(row.get("LogonType") or "").strip()

        if event_id == "4625":
            kind = "FAILURE"
        elif event_id == "4624" and logon_type in ("3", "10") and ip != "LOCAL":
            kind = "SUCCESS"
        else:
            continue

        try:
            time = datetime.strptime(str(row["Time"]).strip(), "%Y-%m-%d %H:%M:%S")
        except (KeyError, ValueError):
            continue

        events.append({
            "time": time,
            "user": str(row.get("User") or "-").strip(),
            "ip": ip,
            "type": kind,
        })

    return sorted(events, key=lambda e: e["time"])


def parse_windows_file(path):
    """Read a Windows logon CSV (columns: Time,EventId,User,Ip,LogonType)."""
    with Path(path).open(encoding="utf-8-sig", errors="replace", newline="") as file:
        return rows_to_events(csv.DictReader(file))