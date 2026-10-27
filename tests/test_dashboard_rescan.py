import http.client
import json
import threading
import time

from logsentinel.dashboard import create_server


def call(port, method, path):
    conn = http.client.HTTPConnection("127.0.0.1", port)
    conn.request(method, path, headers={"Host": f"127.0.0.1:{port}"})
    response = conn.getresponse()
    body = response.read().decode()
    conn.close()
    return response.status, body


def run(server):
    threading.Thread(target=server.serve_forever, daemon=True).start()


def test_rescan_runs_in_background(tmp_path, monkeypatch):
    monkeypatch.setenv("LOGSENTINEL_HOME", str(tmp_path))

    def fake_scan():
        return {"failures": 4, "successes": 1, "alerts": 0, "live": True, "admin": True, "hours": 24}

    server, token, port = create_server(18780, scan=fake_scan, info={"failures": 0})
    run(server)
    try:
        assert call(port, "POST", "/api/rescan")[0] == 403           # no token
        assert call(port, "POST", f"/api/rescan?token={token}")[0] == 202
        data = {}
        for _ in range(50):
            data = json.loads(call(port, "GET", f"/api/data?token={token}")[1])
            if data["scan"]["status"] == "done":
                break
            time.sleep(0.1)
        assert data["scan"]["status"] == "done"
        assert data["info"]["failures"] == 4
    finally:
        server.shutdown()
        server.server_close()


def test_rescan_not_available_without_scan_function(tmp_path, monkeypatch):
    monkeypatch.setenv("LOGSENTINEL_HOME", str(tmp_path))
    server, token, port = create_server(18790)
    run(server)
    try:
        assert call(port, "POST", f"/api/rescan?token={token}")[0] == 400
    finally:
        server.shutdown()
        server.server_close()