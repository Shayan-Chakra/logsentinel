from logsentinel.reports import save_csv


def test_csv_blocks_formulas(tmp_path):
    path = tmp_path / "out.csv"
    save_csv([{"rule": "BRUTE_FORCE", "ip": "203.0.113.5", "user": "=2+2", "count": 6}], path)
    text = path.read_text(encoding="utf-8")
    assert "'=2+2" in text
    assert ",=2+2" not in text
    assert ",-," in text or text.rstrip().endswith(",-")  # missing fields still show "-"