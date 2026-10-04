import ipaddress
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path


def load_blocklist(path="blocklist.txt"):
    """Read bad IPs from a text file (one per line, # for comments)."""
    file = Path(path)
    if not file.exists():
        return set()
    lines = file.read_text(encoding="utf-8").splitlines()
    return {line.strip() for line in lines if line.strip() and not line.startswith("#")}


def check_abuseipdb(ip, api_key):
    """Ask AbuseIPDB about one IP. Returns a note, or None."""
    url = "https://api.abuseipdb.com/api/v2/check?" + urllib.parse.urlencode(
        {"ipAddress": ip, "maxAgeInDays": 90}
    )
    request = urllib.request.Request(
        url, headers={"Key": api_key, "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            data = json.load(response)["data"]
    except Exception:
        return None  # no internet or bad key: skip quietly

    return (
        f"AbuseIPDB score {data['abuseConfidenceScore']}/100, "
        f"{data['totalReports']} reports"
    )


def lookup(ip, blocklist):
    """Return a list of notes about this IP."""
    notes = []

    if ip in blocklist:
        notes.append("is in your local blocklist.txt")

    api_key = os.environ.get("ABUSEIPDB_API_KEY")
    if api_key:
        try:
            is_public = ipaddress.ip_address(ip).is_global
        except ValueError:
            is_public = False
        if is_public:  # private and example IPs are not in public databases
            note = check_abuseipdb(ip, api_key)
            if note:
                notes.append(note)

    return notes