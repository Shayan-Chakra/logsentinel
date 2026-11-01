"""Clean text that comes from log files.

Usernames and addresses in a log are chosen by whoever tried to log in, so an attacker
controls them. Strip anything that could mess with a terminal or hide the real text, and
cap the length so one huge value cannot bloat the database.
"""
import re

MAX_LENGTH = 100

# C0/C1 control characters (including ESC, used for terminal tricks), line/paragraph
# separators, and the invisible left-to-right / right-to-left override characters.
_BAD = re.compile("[\x00-\x1f\x7f-\x9f  ‪-‮⁦-⁩​-‏]")


def clean_text(value, limit=MAX_LENGTH):
    text = _BAD.sub("?", "" if value is None else str(value))
    return text[:limit]
