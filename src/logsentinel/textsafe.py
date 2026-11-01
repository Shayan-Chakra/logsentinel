"""Clean text that comes from log files.

Usernames and addresses in a log are chosen by whoever tried to log in, so an attacker
controls them. Strip anything that could mess with a terminal or hide the real text, and
cap the length so one huge value cannot bloat the database.
"""
import re

MAX_LENGTH = 100

# Removed: C0/C1 control characters (including ESC, used for terminal tricks), line and
# paragraph separators, zero-width characters and the left-to-right / right-to-left
# override characters. They are written as escape codes (never as the raw characters),
# so this file stays plain, visible ASCII.
_BAD = re.compile(r"[\x00-\x1f\x7f-\x9f\u2028\u2029\u202a-\u202e\u2066-\u2069\u200b-\u200f]")


def clean_text(value, limit=MAX_LENGTH):
    text = _BAD.sub("?", "" if value is None else str(value))
    return text[:limit]
