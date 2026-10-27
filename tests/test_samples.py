from pathlib import Path

from logsentinel.parser import parse_line
from logsentinel.detect import find_brute_force, find_password_spray

EXAMPLES = Path(__file__).parent.parent / "examples"


def load_failures(name):
    events = []
    for line in (EXAMPLES / name).read_text().splitlines():
        event = parse_line(line)
        if event and event["type"] == "FAILURE":
            events.append(event)
    return events


def test_normal_log_has_no_alerts():
    events = load_failures("normal.log")
    assert find_brute_force(events, 5, 300) == {}
    assert find_password_spray(events, 5, 300) == {}


def test_spray_log_is_detected():
    events = load_failures("password_spray.log")
    assert find_password_spray(events, 5, 300) == {"admin": 5}


def test_spray_log_is_not_brute_force():
    events = load_failures("password_spray.log")
    assert find_brute_force(events, 5, 300) == {}