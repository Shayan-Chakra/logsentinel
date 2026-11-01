from logsentinel.winparser import rows_to_events


def row(**kw):
    base = {"Time": "2026-10-27 10:00:00", "EventId": "4625", "User": "bob", "Ip": "203.0.113.5", "LogonType": "3"}
    base.update(kw)
    return base


def test_failed_logon_becomes_failure():
    event = rows_to_events([row()])[0]
    assert event["type"] == "FAILURE" and event["ip"] == "203.0.113.5"


def test_local_failure_is_labelled_local():
    assert rows_to_events([row(Ip="-")])[0]["ip"] == "LOCAL"


def test_local_success_is_ignored():
    assert rows_to_events([row(EventId="4624", Ip="127.0.0.1")]) == []


def test_attacker_chosen_username_is_cleaned():
    event = rows_to_events([row(User="admin\x1b[2J" + "x" * 500)])[0]
    assert "\x1b" not in event["user"]
    assert len(event["user"]) <= 100
