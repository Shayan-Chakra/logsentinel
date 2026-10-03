from logsentinel.scoring import risk_by_ip, severity


def build_incidents(rows):
    """Group stored alerts into one incident per IP."""
    groups = {}
    for row in rows:
        if row["ip"]:  # password-spray alerts have no IP, so skip them
            groups.setdefault(row["ip"], []).append(row)

    scores = risk_by_ip(rows)
    incidents = []

    for ip, items in groups.items():
        score = scores.get(ip, 0)
        incidents.append({
            "ip": ip,
            "first_seen": min(r["created_at"] for r in items),
            "last_seen": max(r["last_seen"] for r in items),
            "rules": sorted(r["rule"] for r in items),
            "risk_score": score,
            "severity": severity(score),
            "status": "OPEN",
        })

    return sorted(incidents, key=lambda i: -i["risk_score"])