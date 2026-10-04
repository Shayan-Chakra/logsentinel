from datetime import datetime, timedelta

from logsentinel.detect import find_anomalies


def make_events(counts_per_hour):
    events = []
    start = datetime(2026, 10, 3, 8, 0, 0)
    for hour_offset, count in enumerate(counts_per_hour):
        for i in range(count):
            events.append({
                "time": start + timedelta(hours=hour_offset, seconds=i),
                "user": "bob", "ip": "198.51.100.7", "type": "FAILURE",
            })
    return events


def test_spike_is_flagged():
    events = make_events([3, 3, 3, 3, 60, 3])
    result = find_anomalies(events, factor=5, min_failures=20)
    assert len(result) == 1
    assert result[0]["count"] == 60


def test_steady_traffic_is_not_flagged():
    events = make_events([3, 4, 3, 3, 4, 3])
    assert find_anomalies(events, factor=5, min_failures=20) == []