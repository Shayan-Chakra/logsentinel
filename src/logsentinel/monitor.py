import time

import yaml

from logsentinel.parser import parse_line
from logsentinel.detect import (
    find_brute_force,
    find_username_enumeration,
    find_success_after_failure,
)


def follow(path):
    """Yield new lines as they are added to the file."""
    with open(path, encoding="utf-8", errors="replace") as file:
        file.seek(0, 2)  # jump to the end, ignore old lines
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.5)  # nothing new, wait a bit
                continue
            yield line


def check(events, rules):
    """Run all enabled rules and return a list of (rule, ip, message)."""
    alerts = []
    failures = [e for e in events if e["type"] == "FAILURE"]

    cfg = rules["brute_force"]
    if cfg["enabled"]:
        found = find_brute_force(failures, cfg["failed_attempts"], cfg["window_seconds"])
        for ip, count in found.items():
            alerts.append(("BRUTE_FORCE", ip, f"{ip} failed {count} times - possible brute force!"))

    cfg = rules["username_enumeration"]
    if cfg["enabled"]:
        found = find_username_enumeration(failures, cfg["unique_users"], cfg["window_seconds"])
        for ip, count in found.items():
            alerts.append(("USERNAME_ENUMERATION", ip, f"{ip} tried {count} different usernames - possible enumeration!"))

    cfg = rules["success_after_failure"]
    if cfg["enabled"]:
        found = find_success_after_failure(events, cfg["failed_attempts"], cfg["window_seconds"])
        for item in found:
            alerts.append((
                "SUCCESS_AFTER_FAILURE",
                item["ip"],
                f"[CRITICAL] {item['ip']} logged in as '{item['user']}' after {item['failures']} failures - possible break-in!",
            ))

    return alerts


def monitor(logfile, rules_path):
    with open(rules_path) as file:
        rules = yaml.safe_load(file)

    allowed_ips = set(rules.get("allowlist", {}).get("ips", []))
    events = []
    already_alerted = set()

    print(f"Watching {logfile} ... press Ctrl+C to stop.")

    try:
        for line in follow(logfile):
            event = parse_line(line)
            if not event or event["ip"] in allowed_ips:
                continue

            events.append(event)

            # keep only the last 10 minutes of events (memory stays small)
            events = [
                e for e in events
                if (event["time"] - e["time"]).total_seconds() <= 600
            ]

            for rule, ip, message in check(events, rules):
                if (rule, ip) not in already_alerted:  # alert only once
                    already_alerted.add((rule, ip))
                    print(f"[ALERT] {message}")
    except KeyboardInterrupt:
        print("\nStopped.")