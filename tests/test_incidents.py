from logsentinel.incidents import build_incidents


def test_alerts_are_grouped_into_one_incident_per_ip():
    rows = [
        {"rule": "BRUTE_FORCE", "ip": "203.0.113.10",
         "created_at": "2026-10-04T10:00:00", "last_seen": "2026-10-04T10:05:00"},
        {"rule": "SUCCESS_AFTER_FAILURE", "ip": "203.0.113.10",
         "created_at": "2026-10-04T10:01:00", "last_seen": "2026-10-04T10:06:00"},
        {"rule": "PASSWORD_SPRAY", "ip": None,
         "created_at": "2026-10-04T10:02:00", "last_seen": "2026-10-04T10:02:00"},
    ]
    result = build_incidents(rows)

    assert len(result) == 1
    assert result[0]["risk_score"] == 70
    assert result[0]["severity"] == "CRITICAL"
    assert result[0]["first_seen"] == "2026-10-04T10:00:00"