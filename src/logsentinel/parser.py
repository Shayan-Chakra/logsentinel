import re
from datetime import datetime

TIME = r"^(?P<time>[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})"

FAIL_PATTERN = re.compile(
    TIME + r".*Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\S+)"
)
SUCCESS_PATTERN = re.compile(
    TIME + r".*Accepted (?:password|publickey) for (?P<user>\S+) from (?P<ip>\S+)"
)


def make_event(match, event_type):
    time = datetime.strptime(
        f"{datetime.now().year} {match['time']}", "%Y %b %d %H:%M:%S"
    )
    return {"time": time, "user": match["user"], "ip": match["ip"], "type": event_type}


def parse_line(line):
    match = FAIL_PATTERN.search(line)
    if match:
        return make_event(match, "FAILURE")

    match = SUCCESS_PATTERN.search(line)
    if match:
        return make_event(match, "SUCCESS")

    return None