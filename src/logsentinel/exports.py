"""Build CSV / HTML / JSON reports as text, so the dashboard can send them as downloads."""
import csv
import html
import io
import json
from datetime import datetime

FIELDS = ["last_seen", "rule", "ip", "username", "occurrences"]
DANGEROUS_START = ("=", "+", "-", "@", "\t", "\r")


def safe_cell(value):
    """Stop spreadsheet programs from running a cell as a formula."""
    text = "" if value is None else str(value)
    if text.startswith(DANGEROUS_START):
        text = "'" + text
    return text


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def to_csv(alerts):
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\r\n")
    writer.writerow(FIELDS)
    for alert in alerts:
        writer.writerow([safe_cell(alert.get(field)) for field in FIELDS])
    return "\ufeff" + out.getvalue()  # the BOM makes Excel read it as UTF-8


def to_json(alerts):
    report = {
        "tool": "LogSentinel",
        "generated": _now(),
        "alert_count": len(alerts),
        "alerts": alerts,
    }
    return json.dumps(report, indent=2, default=str)


def to_html(alerts):
    head = "".join(f"<th>{html.escape(field)}</th>" for field in FIELDS)
    rows = ""
    for alert in alerts:
        cells = "".join(
            f"<td>{html.escape('' if alert.get(f) is None else str(alert.get(f)))}</td>"
            for f in FIELDS
        )
        rows += f"<tr>{cells}</tr>\n"
    if not rows:
        rows = f'<tr><td colspan="{len(FIELDS)}">No alerts.</td></tr>'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">
<title>LogSentinel report</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 24px; color: #1a1f2e; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ccd; padding: 8px 10px; text-align: left; }}
  th {{ background: #eef1f8; }}
  .muted {{ color: #667; }}
</style></head><body>
<h1>LogSentinel report</h1>
<p class="muted">Generated {html.escape(_now())} on this PC. {len(alerts)} alerts.</p>
<table><tr>{head}</tr>
{rows}</table>
</body></html>
"""


# kind -> (function that builds the text, content type)
REPORTS = {
    "csv": (to_csv, "text/csv; charset=utf-8"),
    "html": (to_html, "text/html; charset=utf-8"),
    "json": (to_json, "application/json"),
}