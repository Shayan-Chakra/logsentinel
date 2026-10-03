SCORES = {
    "BRUTE_FORCE": 40,
    "USERNAME_ENUMERATION": 25,
    "SUCCESS_AFTER_FAILURE": 30,
}


def severity(score):
    if score >= 70:
        return "CRITICAL"
    if score >= 50:
        return "HIGH"
    if score >= 30:
        return "MEDIUM"
    return "LOW"


def risk_by_ip(alerts):
    totals = {}
    for alert in alerts:
        ip = alert.get("ip")
        if ip:
            totals[ip] = totals.get(ip, 0) + SCORES.get(alert["rule"], 0)
    return {ip: min(score, 100) for ip, score in totals.items()}