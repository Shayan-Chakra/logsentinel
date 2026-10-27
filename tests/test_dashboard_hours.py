import json, threading, time, urllib.request, urllib.error
from logsentinel.dashboard import create_server

def post(port, token, extra=""):
    req = urllib.request.Request(f"http://127.0.0.1:{port}/api/rescan?token={token}{extra}", method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

def test_hours(monkeypatch=None):
    seen = []
    def scan(hours=None):
        seen.append(hours)
        return {"hours": hours}
    server, token, port = create_server(8900, scan=scan)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        assert post(port, token, "&hours=6")[0] == 202
        time.sleep(0.3)
        assert seen == [6]
        for bad in ("0", "-1", "99999", "abc"):
            assert post(port, token, "&hours=" + bad)[0] == 400, bad
        assert seen == [6]
    finally:
        server.shutdown(); server.server_close()