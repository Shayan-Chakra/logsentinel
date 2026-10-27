from logsentinel.threatintel import load_blocklist, lookup


def test_blocklist_ignores_comments(tmp_path):
    file = tmp_path / "blocklist.txt"
    file.write_text("# comment\n203.0.113.10\n\n")
    assert load_blocklist(str(file)) == {"203.0.113.10"}


def test_lookup_finds_blocklisted_ip(monkeypatch):
    monkeypatch.delenv("ABUSEIPDB_API_KEY", raising=False)
    assert lookup("203.0.113.10", {"203.0.113.10"}) != []
    assert lookup("198.51.100.7", {"203.0.113.10"}) == []