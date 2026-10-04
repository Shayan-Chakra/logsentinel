from collections import defaultdict, deque
import statistics


def group_by_ip(events):
    groups = defaultdict(list)
    for event in events:
        groups[event["ip"]].append(event)
    return groups


def find_brute_force(events, threshold=5, window_seconds=300):
    suspicious = {}

    for ip, ip_events in group_by_ip(events).items():
        ip_events.sort(key=lambda e: e["time"])
        window = deque()

        for event in ip_events:
            window.append(event)

            # remove failures that are too old
            while (event["time"] - window[0]["time"]).total_seconds() > window_seconds:
                window.popleft()

            if len(window) >= threshold:
                suspicious[ip] = len(window)
                break

    return suspicious
def find_username_enumeration(events, unique_users=5, window_seconds=300):
    suspicious = {}

    for ip, ip_events in group_by_ip(events).items():
        ip_events.sort(key=lambda e: e["time"])
        window = deque()

        for event in ip_events:
            window.append(event)

            while (event["time"] - window[0]["time"]).total_seconds() > window_seconds:
                window.popleft()

            usernames = {e["user"] for e in window}  # a set keeps only unique names

            if len(usernames) >= unique_users:
                suspicious[ip] = len(usernames)
                break

    return suspicious
def find_success_after_failure(events, failed_attempts=5, window_seconds=300):
    alerts = []
    recent_failures = defaultdict(deque)

    for event in sorted(events, key=lambda e: e["time"]):
        ip = event["ip"]

        if event["type"] == "FAILURE":
            recent_failures[ip].append(event)

        elif event["type"] == "SUCCESS":
            window = recent_failures[ip]

            # remove failures that are too old
            while window and (event["time"] - window[0]["time"]).total_seconds() > window_seconds:
                window.popleft()

            if len(window) >= failed_attempts:
                alerts.append({"ip": ip, "user": event["user"], "failures": len(window)})

    return alerts

def find_password_spray(events, unique_ips=5, window_seconds=300):
    groups = defaultdict(list)
    for event in events:
        groups[event["user"]].append(event)

    suspicious = {}

    for user, user_events in groups.items():
        user_events.sort(key=lambda e: e["time"])
        window = deque()

        for event in user_events:
            window.append(event)

            while (event["time"] - window[0]["time"]).total_seconds() > window_seconds:
                window.popleft()

            ips = {e["ip"] for e in window}

            if len(ips) >= unique_ips:
                suspicious[user] = len(ips)
                break

    return suspicious

def find_anomalies(events, factor=5, min_failures=20):
    buckets = defaultdict(int)
    for event in events:
        hour = event["time"].replace(minute=0, second=0, microsecond=0)
        buckets[hour] += 1

    if len(buckets) < 3:  # not enough data to know what "normal" is
        return []

    baseline = statistics.median(buckets.values())
    anomalies = []

    for hour, count in sorted(buckets.items()):
        if count >= min_failures and count >= factor * baseline:
            anomalies.append({
                "bucket": hour.strftime("%b %d %H:00"),
                "count": count,
                "baseline": baseline,
            })

    return anomalies