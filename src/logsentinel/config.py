from pathlib import Path

import yaml

from logsentinel.paths import data_dir

DEFAULT_RULES = {
    "brute_force": {"enabled": True, "failed_attempts": 5, "window_seconds": 300},
    "username_enumeration": {"enabled": True, "unique_users": 5, "window_seconds": 300},
    "success_after_failure": {"enabled": True, "failed_attempts": 5, "window_seconds": 300},
    "password_spray": {"enabled": True, "unique_ips": 5, "window_seconds": 300},
    "anomaly": {"enabled": True, "factor": 5, "min_failures": 20},
    "allowlist": {"ips": []},
}


def find_rules_file(path=None):
    """Explicit path first, then rules.yaml in the current folder, then in the data folder."""
    if path:
        return Path(path)
    for candidate in (Path("rules.yaml"), data_dir() / "rules.yaml"):
        if candidate.exists():
            return candidate
    return None


def load_rules(path=None):
    """Read the rules. Missing file or missing sections fall back to the built-in defaults."""
    file = find_rules_file(path)
    if file is None or not file.exists():
        return DEFAULT_RULES
    with file.open(encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle)
    if not isinstance(loaded, dict):
        loaded = {}
    return {**DEFAULT_RULES, **loaded}