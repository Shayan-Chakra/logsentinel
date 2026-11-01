# Security Policy

## Supported versions

Only the latest release receives security fixes.

## Reporting a vulnerability

Please do **not** open a public issue for a security problem.

Use GitHub's private reporting instead: open the **Security** tab of this repository and
click **Report a vulnerability**. Include what you found, how to reproduce it, and which
version you used.

You can expect a first reply within 7 days.

## What LogSentinel does and does not do

- It only reads logs and writes reports. It never changes firewall rules, accounts or settings.
- The dashboard listens on `127.0.0.1` only and needs a random secret token.
- Text from logs (usernames, addresses) is treated as untrusted: it is cleaned, length-limited
  and never inserted into the dashboard as HTML.
- Optional AbuseIPDB lookups (only when `ABUSEIPDB_API_KEY` is set) send public IP addresses
  to abuseipdb.com. Nothing else is sent anywhere.

## Known limitations

- The Windows installer and exe are not code-signed, so SmartScreen may warn.
- During a live scan the program runs with administrator rights, including its local
  dashboard. Report anything that lets another program on the same PC reach it.
