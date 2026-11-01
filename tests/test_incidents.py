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


def test_password_spray_becomes_its_own_incident():
    rows = [
        {"rule": "PASSWORD_SPRAY", "ip": None, "username": "admin",
         "created_at": "2026-10-04T10:02:00", "last_seen": "2026-10-04T10:03:00"},
    ]
    result = build_incidents(rows)

    assert len(result) == 1
    assert result[0]["ip"] == "user:admin"
    assert result[0]["rules"] == ["PASSWORD_SPRAY"]
    assert result[0]["risk_score"] == 30
    assert result[0]["severity"] == "MEDIUM"


def test_log_cleared_and_admin_added_make_one_incident_for_the_account():
    rows = [
        {"rule": "LOG_CLEARED", "ip": "LOCAL", "username": None,
         "created_at": "2026-10-04T10:00:00", "last_seen": "2026-10-04T10:00:00"},
        {"rule": "LOG_CLEARED", "ip": None, "username": "mallory",
         "created_at": "2026-10-04T10:00:00", "last_seen": "2026-10-04T10:00:00"},
        {"rule": "ADMIN_ADDED", "ip": None, "username": "mallory",
         "created_at": "2026-10-04T10:01:00", "last_seen": "2026-10-04T10:01:00"},
    ]
    result = [i for i in build_incidents(rows) if i["ip"] == "user:mallory"]
    assert len(result) == 1
    assert result[0]["risk_score"] == 100
    assert result[0]["severity"] == "CRITICAL"
