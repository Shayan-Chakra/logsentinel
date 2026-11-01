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


def test_usernames_are_not_case_sensitive():
    events = rows_to_events([row(User="Administrator"), row(User="ADMINISTRATOR")])
    assert {e["user"] for e in events} == {"administrator"}


def test_network_cleartext_logon_counts_as_success():
    assert rows_to_events([row(EventId="4624", LogonType="8")])[0]["type"] == "SUCCESS"


def test_log_cleared_event():
    event = rows_to_events([row(EventId="1102", User="", Ip="", Subject="Mallory")])[0]
    assert event["type"] == "LOG_CLEARED" and event["user"] == "mallory"


def test_account_created_event_uses_the_new_account_name():
    event = rows_to_events([row(EventId="4720", User="Backdoor", Subject="Mallory", Ip="")])[0]
    assert event["type"] == "ACCOUNT_CREATED" and event["user"] == "backdoor"


def test_admin_added_only_for_the_administrators_group():
    admin = row(EventId="4732", User="Administratoren", Target="Administratoren", TargetSid="S-1-5-32-544", Subject="Mallory", Ip="")
    other = row(EventId="4732", User="Users", Target="Users", TargetSid="S-1-5-32-545", Subject="Mallory", Ip="")
    events = rows_to_events([admin, other])
    assert [e["type"] for e in events] == ["ADMIN_ADDED"]
    assert events[0]["user"] == "mallory"
