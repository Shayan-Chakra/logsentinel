from logsentinel.demo import make_sample_rows
from logsentinel.detect import find_brute_force
from logsentinel.winparser import rows_to_events


def test_demo_rows_make_events_and_a_brute_force():
    events = rows_to_events(make_sample_rows())
    failures = [e for e in events if e["type"] == "FAILURE"]
    assert len(failures) == 20
    assert len([e for e in events if e["type"] == "SUCCESS"]) == 1
    found = find_brute_force(failures, threshold=5, window_seconds=60)
    assert "203.0.113.50" in found