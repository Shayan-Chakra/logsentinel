from logsentinel.parser import parse_line


def test_failed_login_is_parsed():
    line = "Oct 03 19:20:01 server sshd[1]: Failed password for root from 203.0.113.10 port 50001 ssh2"
    event = parse_line(line)
    assert event["type"] == "FAILURE"
    assert event["user"] == "root"
    assert event["ip"] == "203.0.113.10"


def test_successful_login_is_parsed():
    line = "Oct 03 19:21:12 server sshd[9]: Accepted password for root from 203.0.113.10 port 50009 ssh2"
    assert parse_line(line)["type"] == "SUCCESS"


def test_unrelated_line_is_ignored():
    assert parse_line("this is not a login line") is None