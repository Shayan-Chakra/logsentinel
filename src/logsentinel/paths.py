import os
import sys
from pathlib import Path

APP_NAME = "LogSentinel"


def data_dir():
    """The one folder where LogSentinel keeps its database and reports."""
    override = os.environ.get("LOGSENTINEL_HOME")  # used by tests to stay out of your real data
    if override:
        base = Path(override)
    elif sys.platform == "win32":
        local = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        base = Path(local) / APP_NAME
    else:
        base = Path.home() / ".logsentinel"
    base.mkdir(parents=True, exist_ok=True)
    return base


def db_path():
    return str(data_dir() / "logsentinel.db")