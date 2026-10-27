import http.client
import json
import threading

from logsentinel.dashboard import create_server


def fetch(port, path, host=None):
    conn = http.client.HTTPConnection("127.0.0.1", port)
    conn.request("GET", path, headers={"Host": host or f"127.0.0.1:{port}"})
    response = conn.getresponse()
    body = response.read().decode()
    conn.close()
    return response.status, body


def test_dashboard_is_locked_down(tmp_path, monkeypatch):
    monkeypatch.setenv("LOGSENTINEL_HOME", str(tmp_path))
    server, token, port = create_server(18765)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        assert fetch(port, "/")[0] == 403                                # no token
        assert fetch(port, "/?token=wrong")[0] == 403                    # wrong token
        assert fetch(port, f"/?token={token}", host="evil.com")[0] == 403  # wrong Host
        assert fetch(port, f"/?token={token}")[0] == 200                 # correct
        status, body = fetch(port, f"/api/data?token={token}")
        assert status == 200
        assert "alerts" in json.loads(body)
        assert fetch(port, f"/download/csv?token={token}")[0] == 200
        assert fetch(port, f"/download/json?token={token}")[0] == 200
        assert fetch(port, f"/download/html?token={token}")[0] == 200
        assert fetch(port, f"/download/exe?token={token}")[0] == 404
        assert fetch(port, "/download/csv")[0] == 403
    finally:
        server.shutdown()
        server.server_close()

def test_second_server_gets_a_different_port(tmp_path, monkeypatch):
    monkeypatch.setenv("LOGSENTINEL_HOME", str(tmp_path))
    first, _, port1 = create_server(18800)
    second, _, port2 = create_server(18800)
    try:
        assert port1 != port2
    finally:
        first.server_close()
        second.server_close()