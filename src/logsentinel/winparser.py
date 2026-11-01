import csv
from datetime import datetime
from pathlib import Path

from logsentinel.textsafe import clean_text

IGNORED_IPS = {"", "-", "::1", "127.0.0.1", "0.0.0.0"}

# Logon types that count as a login from another computer:
# 3 = network, 8 = network with the password sent in clear text, 10 = Remote Desktop.
SUCCESS_TYPES = ("3", "8", "10")

# The built-in Administrators group has the same SID on every Windows PC and language.
ADMINS_SID = "S-1-5-32-544"


def _name(value, default="-"):
    """Clean a name from the log. Windows account names are not case sensitive."""
    text = clean_text(str(value or "").strip()).lower()
    return text or default


def rows_to_events(rows):
    """Turn Windows event rows into the same events the SSH parser produces.

    Each row needs: Time, EventId, User, Ip, LogonType.
    Optional columns: Subject (who did it), Target, TargetSid.

    4625 = failed logon.  4624 = successful logon (types 3, 8 and 10 from another computer).
    1102 = the Security log was cleared.  4720 = a user account was created.
    4732 = someone was added to the Administrators group.
    """
    events = []

    for row in rows:
        ip = clean_text(str(row.get("Ip") or "").strip())
        if ip.lower().startswith("::ffff:"):  # IPv4 written in IPv6 style
            ip = ip[7:]
        if ip in IGNORED_IPS:
            ip = "LOCAL"   # attempt made on this PC itself, not from the network

        event_id = str(row.get("EventId") or "").strip()
        logon_type = str(row.get("LogonType") or "").strip()
        user = _name(row.get("User"))

        if event_id == "4625":
            kind = "FAILURE"
        elif event_id == "4624" and logon_type in SUCCESS_TYPES and ip != "LOCAL":
            kind = "SUCCESS"
        elif event_id == "1102":
            kind, user, ip = "LOG_CLEARED", _name(row.get("Subject") or row.get("User")), "LOCAL"
        elif event_id == "4720":
            kind, ip = "ACCOUNT_CREATED", "LOCAL"          # user = the NEW account
        elif event_id == "4732" and (
            str(row.get("TargetSid") or "").strip() == ADMINS_SID
            or str(row.get("Target") or row.get("User") or "").strip().lower() == "administrators"
        ):
            kind, user, ip = "ADMIN_ADDED", _name(row.get("Subject") or row.get("User")), "LOCAL"
        else:
            continue

        try:
            time = datetime.strptime(str(row["Time"]).strip(), "%Y-%m-%d %H:%M:%S")
        except (KeyError, ValueError):
            continue

        events.append({"time": time, "user": user, "ip": ip, "type": kind})

    return sorted(events, key=lambda e: e["time"])


def parse_windows_file(path):
    """Read a Windows event CSV (columns: Time,EventId,User,Ip,LogonType[,Subject,Target,TargetSid])."""
    with Path(path).open(encoding="utf-8-sig", errors="replace", newline="") as file:
        return rows_to_events(csv.DictReader(file))
