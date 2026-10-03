from logsentinel.scoring import risk_by_ip, severity


def test_scores_add_up_per_ip():
    alerts = [
        {"rule": "BRUTE_FORCE", "ip": "203.0.113.10"},
        {"rule": "USERNAME_ENUMERATION", "ip": "203.0.113.10"},
        {"rule": "SUCCESS_AFTER_FAILURE", "ip": "203.0.113.10"},
    ]
    assert risk_by_ip(alerts) == {"203.0.113.10": 95}


def test_severity_levels():
    assert severity(10) == "LOW"
    assert severity(30) == "MEDIUM"
    assert severity(50) == "HIGH"
    assert severity(95) == "CRITICAL"