from datetime import datetime, timedelta

from logsentinel.detect import find_brute_force


def make_failures(count, gap_seconds):
    start = datetime(2026, 10, 3, 19, 0, 0)
    return [
        {
            "time": start + timedelta(seconds=i * gap_seconds),
            "user": "root",
            "ip": "203.0.113.10",
            "type": "FAILURE",
        }
        for i in range(count)
    ]


def test_five_fast_failures_trigger_alert():
    events = make_failures(5, 10)
    result = find_brute_force(events, threshold=5, window_seconds=300)
    assert "203.0.113.10" in result


def test_four_fast_failures_do_not_trigger():
    events = make_failures(4, 10)
    assert find_brute_force(events, threshold=5, window_seconds=300) == {}


def test_five_slow_failures_do_not_trigger():
    events = make_failures(5, 3600)  # one failure per hour
    assert find_brute_force(events, threshold=5, window_seconds=300) == {}

from logsentinel.detect import find_password_spray


def test_password_spray_detected():
    start = datetime(2026, 10, 3, 13, 0, 0)
    events = [
        {"time": start + timedelta(seconds=i * 30), "user": "admin",
         "ip": f"203.0.113.{20 + i}", "type": "FAILURE"}
        for i in range(5)
    ]
    assert find_password_spray(events, unique_ips=5, window_seconds=300) == {"admin": 5}


def test_same_ip_is_not_password_spray():
    start = datetime(2026, 10, 3, 13, 0, 0)
    events = [
        {"time": start + timedelta(seconds=i), "user": "admin",
         "ip": "203.0.113.10", "type": "FAILURE"}
        for i in range(5)
    ]
    assert find_password_spray(events, unique_ips=5, window_seconds=300) == {}