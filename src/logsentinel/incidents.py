from logsentinel.scoring import SCORES, severity


# Rules about an ACCOUNT (not an address). They become incidents named "user:<account>".
ACCOUNT_RULES = ("PASSWORD_SPRAY", "LOG_CLEARED", "ACCOUNT_CREATED", "ADMIN_ADDED")


def incident_key(row):
    """Who an alert belongs to: an IP address, or 'user:<name>' for password spraying."""
    if row["ip"]:
        return row["ip"]
    # These rules are about one account, not one address.
    if row["rule"] in ACCOUNT_RULES and row.get("username"):
        return "user:" + row["username"]
    return None


def build_incidents(rows):
    """Group stored alerts into one incident per IP (or per sprayed account)."""
    groups = {}
    for row in rows:
        key = incident_key(row)
        if key:
            groups.setdefault(key, []).append(row)

    incidents = []

    for key, items in groups.items():
        score = min(sum(SCORES.get(r["rule"], 0) for r in items), 100)
        incidents.append({
            "ip": key,
            "first_seen": min(r["created_at"] for r in items),
            "last_seen": max(r["last_seen"] for r in items),
            "rules": sorted(r["rule"] for r in items),
            "risk_score": score,
            "severity": severity(score),
            "status": "OPEN",
        })

    return sorted(incidents, key=lambda i: -i["risk_score"])
