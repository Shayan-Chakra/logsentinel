import argparse
import json
import os
import sys
import time
from pathlib import Path
from types import SimpleNamespace

from logsentinel.config import load_rules
from logsentinel.database import get_alerts, save_alerts
from logsentinel.detect import (
    find_anomalies,
    find_brute_force,
    find_password_spray,
    find_success_after_failure,
    find_username_enumeration,
)
from logsentinel.elevate import relaunch_as_admin
from logsentinel.incidents import build_incidents
from logsentinel.monitor import monitor
from logsentinel.parser import parse_line
from logsentinel.paths import data_dir
from logsentinel.reports import save_csv, save_html
from logsentinel.scoring import risk_by_ip, severity
from logsentinel.threatintel import load_blocklist, lookup
from logsentinel.winlogs import WindowsLogError, is_admin, read_windows_events
from logsentinel.winparser import parse_windows_file


def pick_format(path, requested):
    """auto = .csv and .evtx files are Windows logs, everything else is an SSH log."""
    if requested and requested != "auto":
        return requested
    return "windows" if path.suffix.lower() in (".csv", ".evtx") else "ssh"


def load_events(args):
    """Read the log the user asked for and return normalized events."""
    hours = getattr(args, "hours", None)

    if getattr(args, "live_windows", False):
        hours = hours or 24
        print(f"Reading this PC's Windows Security log (last {hours:g} hours)...")
        events = read_windows_events(hours=hours)
        if not events and not is_admin():
            print("[NOTE] No events found, and this window is NOT running as Administrator. "
                  "Windows may be hiding the Security log from you. "
                  "Open PowerShell as Administrator and try again.")
        return events

    if not args.logfile:
        print("[ERROR] Give a log file, or use --live-windows to read this PC's Windows Security log.")
        raise SystemExit(1)

    log_path = Path(args.logfile)
    if not log_path.exists():
        print(f"[ERROR] Log file not found: {log_path}")
        raise SystemExit(1)
    if log_path.is_dir():
        print(f"[ERROR] That is a folder, not a file: {log_path}")
        raise SystemExit(1)

    if pick_format(log_path, getattr(args, "format", "auto")) == "windows":
        if log_path.suffix.lower() == ".evtx":
            print(f"Reading Windows event log file: {log_path}")
            return read_windows_events(path=str(log_path), hours=hours)
        events = parse_windows_file(log_path)
        if not events:
            print("[NOTE] No usable logon events found. A Windows CSV needs the columns: "
                  "Time,EventId,User,Ip,LogonType")
        return events

    events = []
    with open(log_path, encoding="utf-8", errors="replace") as file:
        for line in file:
            event = parse_line(line)
            if event:
                events.append(event)
    return events


def analyze(args):
    try:
        parsed = load_events(args)
    except WindowsLogError as error:
        print(f"[ERROR] {error}")
        raise SystemExit(1)

    rules = load_rules(args.rules)
    allowed_ips = set(rules.get("allowlist", {}).get("ips", []))
    events = [e for e in parsed if e["ip"] not in allowed_ips]

    failures = [e for e in events if e["type"] == "FAILURE"]
    successes = [e for e in events if e["type"] == "SUCCESS"]

    print(f"Failed logins found: {len(failures)}")
    print(f"Successful logins found: {len(successes)}")

    brute, enum, breakins, spray, anomalies = {}, {}, [], {}, []

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

    cfg = rules.get("anomaly", {})
    if cfg.get("enabled"):
        anomalies = find_anomalies(
            failures,
            factor=cfg["factor"],
            min_failures=cfg["min_failures"],
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

    for item in anomalies:
        print(
            f"[ALERT] {item['count']} failures during {item['bucket']} "
            f"(normal is about {item['baseline']}) - unusual spike!"
        )
        alerts.append({"rule": "ANOMALY", "count": item["count"]})

    if not alerts:
        print("No suspicious activity.")

    for ip, score in sorted(risk_by_ip(alerts).items(), key=lambda item: -item[1]):
        print(f"RISK: {ip} score {score}/100 -> {severity(score)}")

    blocklist = load_blocklist()
    for ip in sorted(risk_by_ip(alerts)):
        for note in lookup(ip, blocklist):
            print(f"THREAT INTEL: {ip} {note}")

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
    return {"failures": len(failures), "successes": len(successes), "alerts": len(alerts)}

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


def ask_yes_no(question):
    """Ask a yes/no question. Pressing Enter means yes."""
    try:
        answer = input(question).strip().lower()
    except EOFError:
        return False
    return answer in ("", "y", "yes")


def start(args):
    """One command: ask for admin rights, read the Windows Security log, analyze, show dashboard."""
    folder = data_dir()
    print("LogSentinel - scan of this PC's Windows Security log")
    print(f"Data folder: {folder}")
    print()

    if sys.platform == "win32" and not is_admin() and not args.no_admin:
        print("To read the Windows Security log, LogSentinel needs Administrator permission.")
        print("Windows will show a confirmation window. Nothing on your PC is changed.")
        if ask_yes_no("Continue? [Y/n] "):
            extra = ["start", "--hours", f"{args.hours:g}", "--elevated"]
            if args.rules:
                extra += ["--rules", os.path.abspath(args.rules)]
            if relaunch_as_admin(extra):
                print("A new window with administrator rights is opening. You can close this one.")
                time.sleep(2)
                return
            print("[NOTE] Administrator permission was not granted. Trying without it...")
        else:
            print("[NOTE] Skipping administrator permission. Some events may be hidden.")
        print()

    def scan_once(hours=None):
        h = hours or args.hours
        result = analyze(SimpleNamespace(
            logfile=None,
            live_windows=True,
            hours=h,
            rules=args.rules,
            json=str(folder / "last_report.json"),
            csv=None,
            html=None,
            format="auto",
        ))
        return {**result, "live": True, "admin": is_admin(), "hours": h}

    try:
        info = scan_once()
        print()
        print(f"Results saved in: {folder}")
        if not getattr(args, "no_dashboard", False):
            from logsentinel.dashboard import serve
            serve(scan=scan_once, info=info)
    finally:
        if args.elevated or args.guided:
            try:
                input("\nPress Enter to close this window...")
            except EOFError:
                pass

def demo(args):
    """Show the dashboard with made-up data. Uses a throwaway folder, never your real data."""
    import tempfile
    from logsentinel.dashboard import serve
    from logsentinel.demo import make_sample_csv

    folder = Path(tempfile.mkdtemp(prefix="logsentinel-demo-"))
    os.environ["LOGSENTINEL_HOME"] = str(folder)  # fake alerts go into a separate database
    sample = folder / "demo_windows.csv"
    make_sample_csv(sample)

    print("LogSentinel DEMO - made-up data, nothing is read from your PC.")
    result = analyze(SimpleNamespace(
        logfile=str(sample),
        live_windows=False,
        hours=None,
        rules=None,
        json=str(folder / "demo_report.json"),
        csv=None,
        html=None,
        format="windows",
    ))
    serve(info={**result, "live": False}, demo=True)

def main():
    parser = argparse.ArgumentParser(
        prog="logsentry",
        description="Security log analysis tool",
    )
    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze a log file")
    analyze_parser.add_argument("logfile", nargs="?", help="Path to the log file (.log, .csv or .evtx)")
    analyze_parser.add_argument("--rules", default=None, help="Path to rules file")
    analyze_parser.add_argument("--json", default="report.json", help="Where to save the JSON report")
    analyze_parser.add_argument("--csv", help="Where to save the CSV report")
    analyze_parser.add_argument("--html", help="Where to save the HTML report")
    analyze_parser.add_argument(
        "--format", choices=["auto", "ssh", "windows"], default="auto",
        help="Log type. auto (default): .csv and .evtx are Windows logs, anything else is SSH",
    )
    analyze_parser.add_argument(
        "--live-windows", action="store_true",
        help="Read this PC's Windows Security log directly (run as Administrator)",
    )
    analyze_parser.add_argument(
        "--hours", type=float,
        help="Only look at the last N hours (live Windows default: 24)",
    )

    monitor_parser = subparsers.add_parser("monitor", help="Watch a log file live")
    monitor_parser.add_argument("logfile", help="Path to the log file")
    monitor_parser.add_argument("--rules", default=None, help="Path to rules file")

    history_parser = subparsers.add_parser("history", help="Show stored alerts")
    history_parser.add_argument("--limit", type=int, default=20, help="How many alerts to show")

    subparsers.add_parser("incidents", help="Show one case per attacker IP")
    subparsers.add_parser("console", help="Start the interactive console")

    start_parser = subparsers.add_parser("start", help="Scan this PC's Windows Security log")
    start_parser.add_argument("--hours", type=float, default=24, help="How many hours back to scan (default 24)")
    start_parser.add_argument("--rules", default=None, help="Path to rules file")
    start_parser.add_argument("--no-admin", action="store_true", help="Do not ask for Administrator permission")
    start_parser.add_argument("--elevated", action="store_true", help=argparse.SUPPRESS)
    start_parser.add_argument("--no-dashboard", action="store_true", help="Do not open the dashboard")

    dashboard_parser = subparsers.add_parser("dashboard", help="Open the dashboard in your browser")
    dashboard_parser.add_argument("--port", type=int, default=8765, help="Port to use (default 8765)")
    dashboard_parser.add_argument("--no-browser", action="store_true", help="Do not open the browser automatically")
    subparsers.add_parser("demo", help="Show the dashboard with made-up sample data")
    
    args = parser.parse_args()

    if args.command == "analyze":
        analyze(args)
    elif args.command == "monitor":
        monitor(args.logfile, args.rules)
    elif args.command == "history":
        history(args)
    elif args.command == "incidents":
        show_incidents(args)
    elif args.command == "start":
        args.guided = False
        start(args)
    elif args.command == "dashboard":
        from logsentinel.dashboard import serve
        serve(args.port, open_browser=not args.no_browser)
    elif args.command == "demo":
        demo(args)
    elif args.command == "console":
        from logsentinel.console import start_console
        start_console()
    else:
        # double-clicked the exe / typed just "logsentry" -> guided scan
        start(SimpleNamespace(hours=24, rules=None, elevated=False, no_admin=False, guided=True))


if __name__ == "__main__":
    main()