import json

from logsentinel.exports import to_csv, to_html, to_json

ALERTS = [{
    "rule": "BRUTE_FORCE", "ip": "=1+1", "username": None,
    "occurrences": 3, "last_seen": "2026-10-11 10:00:00",
}]


def test_csv_blocks_formulas():
    out = to_csv(ALERTS)
    assert "'=1+1" in out
    assert ",=1+1" not in out


def test_html_escapes_input():
    out = to_html([{"rule": "X", "ip": "<script>alert(1)</script>"}])
    assert "<script>alert" not in out
    assert "&lt;script&gt;" in out


def test_json_is_valid():
    data = json.loads(to_json(ALERTS))
    assert data["alert_count"] == 1
    assert data["alerts"][0]["rule"] == "BRUTE_FORCE"