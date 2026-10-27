"""A small local web dashboard. Standard library only, so it fits inside the exe.

The page itself (HTML / CSS / JavaScript) lives in dashboard_page.py.
"""
import json
import secrets
import threading
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from logsentinel.dashboard_page import PAGE
from logsentinel.database import get_alerts
from logsentinel.exports import REPORTS
from logsentinel.incidents import build_incidents


class LocalServer(HTTPServer):
    # On Windows, "reuse address" lets two programs share one port.
    # Turn it off so a busy port is skipped and the next one is used.
    allow_reuse_address = False


def new_state(scan=None, info=None, demo=False):
    return {
        "scan": scan,            # function that scans again and returns a summary dict
        "info": info or {},      # summary of the last scan
        "demo": demo,
        "status": "idle",        # idle / running / done / error
        "message": "",
        "lock": threading.Lock(),
    }


def get_data(state=None):
    state = state or new_state()
    rows = get_alerts(1000)
    return {
        "alerts": [dict(row) for row in rows],
        "incidents": build_incidents(rows),
        "info": state["info"],
        "demo": state["demo"],
        "scan": {
            "can_rescan": bool(state["scan"]),
            "status": state["status"],
            "message": state["message"],
        },
    }


def start_scan(state, hours=None):
    """Run the scan in the background. Returns False if one is already running."""
    with state["lock"]:
        if state["status"] == "running":
            return False
        state["status"] = "running"
        state["message"] = ""

    def work():
        try:
            result = state["scan"](hours) if hours is not None else state["scan"]()
            state["info"] = result or {}
            state["status"] = "done"
        except SystemExit:
            state["status"] = "error"
            state["message"] = "Could not read the log. See the LogSentinel window for details."
        except Exception as error:
            state["status"] = "error"
            state["message"] = str(error)[:200]

    threading.Thread(target=work, daemon=True).start()
    return True


def make_handler(token, port, state=None):
    state = state or new_state()
    allowed_hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # keep the console quiet

        def _send(self, code, body, content_type, extra=None):
            data = body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'none'; style-src 'unsafe-inline'; "
                "script-src 'unsafe-inline'; connect-src 'self'",
            )
            for name, value in (extra or {}).items():
                self.send_header(name, value)
            self.end_headers()
            self.wfile.write(data)

        def _check(self):
            """Host and token checks. Returns the parsed URL, or None (and answers 403)."""
            if self.headers.get("Host", "") not in allowed_hosts:
                self._send(403, "Forbidden", "text/plain")
                return None
            url = urlparse(self.path)
            given = parse_qs(url.query).get("token", [""])[0]
            if not secrets.compare_digest(given.encode(), token.encode()):
                self._send(
                    403,
                    "Missing or wrong token. Use the link shown in the LogSentinel window.",
                    "text/plain",
                )
                return None
            return url

        def do_GET(self):
            url = self._check()
            if url is None:
                return

            if url.path == "/":
                return self._send(200, PAGE, "text/html; charset=utf-8")
            if url.path == "/api/data":
                return self._send(200, json.dumps(get_data(state), default=str), "application/json")
            if url.path.startswith("/download/"):
                kind = url.path[len("/download/"):]
                if kind not in REPORTS:
                    return self._send(404, "Not found", "text/plain")
                build, content_type = REPORTS[kind]
                stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                return self._send(
                    200,
                    build(get_data(state)["alerts"]),
                    content_type,
                    {"Content-Disposition": f'attachment; filename="logsentinel-report-{stamp}.{kind}"'},
                )
            return self._send(404, "Not found", "text/plain")

        def do_POST(self):
            url = self._check()
            if url is None:
                return

            if url.path == "/api/rescan":
                if not state["scan"]:
                    return self._send(400, json.dumps({"error": "Rescan is not available here."}), "application/json")
                hours = None
                raw = parse_qs(url.query).get("hours", [""])[0]
                if raw:
                    try:
                        hours = int(raw)
                    except ValueError:
                        hours = 0
                    if not 0 < hours <= 720:
                        return self._send(400, json.dumps({"error": "Unsupported time range."}), "application/json")
                started = start_scan(state, hours)
                return self._send(202, json.dumps({"started": started}), "application/json")
            return self._send(404, "Not found", "text/plain")

    return Handler


def create_server(port=8765, scan=None, info=None, demo=False):
    """Make the server on 127.0.0.1 (this PC only). Returns (server, token, port)."""
    token = secrets.token_urlsafe(16)
    state = new_state(scan, info, demo)
    for p in range(port, port + 10):
        try:
            server = LocalServer(("127.0.0.1", p), make_handler(token, p, state))
            return server, token, p
        except OSError:
            continue  # port busy, try the next one
    raise OSError("No free port found for the dashboard.")


def serve(port=8765, open_browser=True, scan=None, info=None, demo=False):
    server, token, port = create_server(port, scan, info, demo)
    url = f"http://127.0.0.1:{port}/?token={token}"
    print()
    print(f"Dashboard: {url}", flush=True)
    print("Only this PC can open it. Press Ctrl+C to stop.", flush=True)
    if open_browser:
        threading.Timer(0.5, webbrowser.open, [url]).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    finally:
        server.server_close()
