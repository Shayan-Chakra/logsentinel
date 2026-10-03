from logsentinel.database import save_alerts, get_alerts


def test_same_alert_is_not_duplicated(tmp_path):
    db = str(tmp_path / "test.db")
    alert = {"rule": "BRUTE_FORCE", "ip": "203.0.113.10", "count": 5}

    assert save_alerts([alert], db) == (1, 0)
    assert save_alerts([alert], db) == (0, 1)

    rows = get_alerts(10, db)
    assert len(rows) == 1
    assert rows[0]["occurrences"] == 2