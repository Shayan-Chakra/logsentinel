import argparse
import json
from pathlib import Path

import yaml

from logsentinel.parser import parse_line
from logsentinel.detect import (
    find_brute_force,
    find_username_enumeration,
    find_success_after_failure,
    find_password_spray,
)
from logsentinel.reports import save_csv, save_html
from logsentinel.monitor import monitor
from logsentinel.database import save_alerts, get_alerts
from logsentinel.scoring import risk_by_ip, severity
from logsentinel.incidents import build_incidents


def analyze(args):
    log_path = Path(args.logfile)
    if not log_path.exists():
        print(f"[ERROR] Log file not found: {log_path}")
        raise SystemExit(1)

    with open(args.rules) as file:
        rules = yaml.safe_load(file)

    allowed_ips = set(rules.get("allowlist", {}).get("ips", []))
    events = []

    with open(log_path) as file:
        for line in file:
            event = parse_line(line)
            if event and event["ip"] not in allowed_ips:
                events.append(event)

    failures = [e for e in events if e["type"] == "FAILURE"]
    successes = [e for e in events if e["type"] == "SUCCESS"]

    print(f"Failed logins found: {len(failures)}")
    print(f"Successful logins found: {len(successes)}")

    brute, enum, breakins, spray = {}, {}, [], {}

    cfg = rules["brute_force"]
    if cfg["enabled"]:
        brute = find_brute_force(
            failures,
            threshold=cfg["failed_attempts"],
            window_seconds=cfg["window_seconds"],
        )

    cfg = rules["username_enumeration"]
    if cfg["enabled"]:
        enum = find_username_enumeration(
            failures,
            unique_users=cfg["unique_users"],
            window_seconds=cfg["window_seconds"],
        )

    cfg = rules["success_after_failure"]
    if cfg["enabled"]:
        breakins = find_success_after_failure(
            events,
            failed_attempts=cfg["failed_attempts"],
            window_seconds=cfg["window_seconds"],
        )

    cfg = rules.get("password_spray", {})
    if cfg.get("enabled"):
        spray = find_password_spray(
            failures,
            unique_ips=cfg["unique_ips"],
            window_seconds=cfg["window_seconds"],
        )

    alerts = []

    for ip, count in brute.items():
        print(f"[ALERT] {ip} failed {count} times - possible brute force!")
        alerts.append({"rule": "BRUTE_FORCE", "ip": ip, "count": count})

    for ip, count in enum.items():
        print(f"[ALERT] {ip} tried {count} different usernames - possible username enumeration!")
        alerts.append({"rule": "USERNAME_ENUMERATION", "ip": ip, "count": count})

    for item in breakins:
        print(
            f"[CRITICAL] {item['ip']} logged in as '{item['user']}' "
            f"after {item['failures']} failures - possible break-in!"
        )
        alerts.append({"rule": "SUCCESS_AFTER_FAILURE", **item})

    for user, count in spray.items():
        print(f"[ALERT] {count} different IPs targeted user '{user}' - possible password spraying!")
        alerts.append({"rule": "PASSWORD_SPRAY", "user": user, "count": count})

    if not alerts:
        print("No suspicious activity.")

    for ip, score in sorted(risk_by_ip(alerts).items(), key=lambda item: -item[1]):
        print(f"RISK: {ip} score {score}/100 -> {severity(score)}")

    with open(args.json, "w") as report:
        json.dump(alerts, report, indent=4)

    print(f"Report saved: {args.json} ({len(alerts)} alerts)")

    if args.csv:
        save_csv(alerts, args.csv)
        print(f"CSV report saved: {args.csv}")

    if args.html:
        save_html(alerts, args.html)
        print(f"HTML report saved: {args.html}")

    new, repeated = save_alerts(alerts)
    print(f"Database: {new} new alerts, {repeated} repeated (already known)")


def history(args):
    rows = get_alerts(args.limit)
    if not rows:
        print("No alerts stored yet.")
        return
    for row in rows:
        print(
            f"{row['last_seen']}  {row['rule']:<22} "
            f"{row['ip'] or row['username'] or '-':<16} x{row['occurrences']}"
        )

def show_incidents(args):
    incidents = build_incidents(get_alerts(1000))
    if not incidents:
        print("No incidents yet. Run 'logsentry analyze' first.")
        return
    for inc in incidents:
        print(f"[{inc['severity']}] {inc['ip']}  score {inc['risk_score']}/100  {inc['status']}")
        print(f"    first seen: {inc['first_seen']}")
        print(f"    last seen:  {inc['last_seen']}")
        print(f"    rules:      {', '.join(inc['rules'])}")
        print()


def main():
    parser = argparse.ArgumentParser(
        prog="logsentry",
        description="Security log analysis tool",
    )
    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze a log file")
    analyze_parser.add_argument("logfile", help="Path to the log file")
    analyze_parser.add_argument("--rules", default="rules.yaml", help="Path to rules file")
    analyze_parser.add_argument("--json", default="report.json", help="Where to save the JSON report")
    analyze_parser.add_argument("--csv", help="Where to save the CSV report")
    analyze_parser.add_argument("--html", help="Where to save the HTML report")

    monitor_parser = subparsers.add_parser("monitor", help="Watch a log file live")
    monitor_parser.add_argument("logfile", help="Path to the log file")
    monitor_parser.add_argument("--rules", default="rules.yaml", help="Path to rules file")

    history_parser = subparsers.add_parser("history", help="Show stored alerts")
    history_parser.add_argument("--limit", type=int, default=20, help="How many alerts to show")
    subparsers.add_parser("incidents", help="Show one case per attacker IP")

    args = parser.parse_args()

    if args.command == "analyze":
        analyze(args)
    elif args.command == "monitor":
        monitor(args.logfile, args.rules)
    elif args.command == "history":
        history(args)
    elif args.command == "incidents":
        show_incidents(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()