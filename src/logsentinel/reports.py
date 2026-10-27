import csv
import html

FIELDS = ["rule", "ip", "user", "count", "failures"]

# Excel treats cells starting with these characters as formulas.
FORMULA_START = ("=", "+", "-", "@", "\t", "\r")


def safe_cell(value):
    """Make a value safe to open in Excel. A lone '-' means 'empty' and is kept."""
    text = str(value)
    if text != "-" and text.startswith(FORMULA_START):
        return "'" + text
    return text


def save_csv(alerts, path):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(FIELDS)
        for alert in alerts:
            writer.writerow([safe_cell(alert.get(field, "-")) for field in FIELDS])


def save_html(alerts, path):
    rows = ""
    for alert in alerts:
        cells = "".join(
            f"<td>{html.escape(str(alert.get(field, '-')))}</td>" for field in FIELDS
        )
        rows += f"<tr>{cells}</tr>\n"

    headers = "".join(f"<th>{field}</th>" for field in FIELDS)

    page = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>LogSentinel Report</title>
<style>
  body {{ font-family: Arial; margin: 40px; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
  th {{ background: #eee; }}
</style>
</head>
<body>
<h1>LogSentinel Report</h1>
<p>Total alerts: {len(alerts)}</p>
<table>
<tr>{headers}</tr>
{rows}</table>
</body>
</html>"""

    with open(path, "w", encoding="utf-8") as file:
        file.write(page)