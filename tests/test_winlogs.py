import json

import pytest

from logsentinel import winlogs
from logsentinel.winlogs import WindowsLogError, parse_output, read_windows_events


def rows_json(*rows):
    return json.dumps(list(rows))


FAIL = {"Time": "2026-10-27 10:00:00", "EventId": 4625, "User": "bob", "Ip": "203.0.113.5", "LogonType": "3"}


def test_empty_output_means_no_events():
    assert parse_output("") == []
    assert parse_output("[]") == []


def test_one_row_is_accepted_even_if_not_in_a_list():
    assert len(parse_output(json.dumps(FAIL))) == 1


def test_rows_become_events():
    events = parse_output(rows_json(FAIL))
    assert events[0]["type"] == "FAILURE" and events[0]["ip"] == "203.0.113.5"


def test_new_event_kinds_come_through():
    cleared = {"Time": "2026-10-27 10:00:00", "EventId": 1102, "Subject": "Mallory"}
    assert parse_output(rows_json(cleared))[0]["type"] == "LOG_CLEARED"


def test_access_denied_gives_a_friendly_message():
    with pytest.raises(WindowsLogError) as error:
        parse_output("ERROR: Attempted to perform an unauthorized operation.")
    assert "Administrator" in str(error.value)


def test_missing_file_gives_a_friendly_message():
    with pytest.raises(WindowsLogError) as error:
        parse_output("ERROR: The system cannot find the file specified.")
    assert "could not find" in str(error.value).lower()


def test_unreadable_output_is_reported_not_crashed():
    with pytest.raises(WindowsLogError):
        parse_output("this is not json")


def test_hours_and_path_are_passed_to_powershell_as_environment_values():
    seen = {}

    def runner(env):
        seen.update(env)
        return "[]"

    read_windows_events(path="C:\\logs\\a.evtx", hours=6, runner=runner)
    assert seen == {"LS_PATH": "C:\\logs\\a.evtx", "LS_HOURS": "6"}


@pytest.mark.parametrize("bad", ["abc", 0, -3])
def test_bad_hours_are_refused(bad):
    with pytest.raises(WindowsLogError):
        read_windows_events(hours=bad, runner=lambda env: "[]")


def test_other_systems_get_a_clear_message(monkeypatch):
    monkeypatch.setattr(winlogs, "_is_windows", lambda: False)
    with pytest.raises(WindowsLogError) as error:
        read_windows_events()
    assert "only works on Windows" in str(error.value)
