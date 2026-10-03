# LogSentinel

A small command-line tool that reads SSH login logs and detects suspicious activity.

## What it detects
- Brute force (many failed logins in a short time)
- Username enumeration (one IP trying many usernames)
- Password spraying (many IPs attacking one username)
- Successful login after many failures (possible break-in)

## Install
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

## Use
```
logsentry analyze examples\auth.log
logsentry analyze examples\auth.log --csv report.csv --html report.html
logsentry monitor live.log
logsentry history
```

## Dashboard
```
uvicorn logsentinel.api:app --reload
```
Then open http://127.0.0.1:8000

## Settings
All detection limits are in `rules.yaml`. You can turn a rule on or off there and add trusted IPs to the allowlist.

## Tests
```
pytest
```

## Note
The example logs use fake documentation IPs (203.0.113.x and 198.51.100.x), not real addresses.