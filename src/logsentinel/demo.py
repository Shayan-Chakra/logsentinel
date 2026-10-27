"""Made-up sample data, so a new user can see the dashboard working straight away."""
import csv
from datetime import datetime, timedelta

FIELDS = ["Time", "EventId", "User", "Ip", "LogonType"]


def make_sample_rows(now=None):
    now = (now or datetime.now()).replace(microsecond=0)
    start = now - timedelta(minutes=5)
    rows = []

    def add(seconds, event_id, user, ip, logon_type="3"):
        when = start + timedelta(seconds=seconds)
        rows.append({
            "Time": when.strftime("%Y-%m-%d %H:%M:%S"),
            "EventId": event_id,
            "User": user,
            "Ip": ip,
            "LogonType": logon_type,
        })

    # 1) brute force, then a successful login (a possible break-in)
    for n in range(8):
        add(n * 3, 4625, "admin", "203.0.113.50")
    add(30, 4624, "admin", "203.0.113.50")

    # 2) one IP trying many different usernames
    for n, user in enumerate(["root", "guest", "test", "oracle", "backup", "support"]):
        add(60 + n * 3, 4625, user, "198.51.100.7")

    # 3) many IPs all attacking one user (password spray)
    for n in range(6):
        add(120 + n * 3, 4625, "administrator", f"192.0.2.{10 + n}")

    return rows


def make_sample_csv(path):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(make_sample_rows())