from datetime import datetime

from logsentinel import monitor as monitor_module
from logsentinel.config import DEFAULT_RULES
from logsentinel.database import get_alerts
from logsentinel.monitor import check, follow


def fail_line(second, ip="203.0.113.10", user="root"):
    stamp = datetime.now().strftime("%b %d %H:%M:") + f"{second:02d}"
    return f"{stamp} server sshd[1]: Failed password for {user} from {ip} port 5000 ssh2\n"


def test_check_finds_brute_force():
    from logsentinel.parser import parse_line
    events = [parse_line(fail_line(s)) for s in range(0, 10)]
    rules = [r[0] for r in check(events, DEFAULT_RULES)]
    assert "BRUTE_FORCE" in rules


def test_follow_yields_only_new_lines(tmp_path, monkeypatch):
    log = tmp_path / "a.log"
    log.write_text("old line\n")

    def fake_sleep(_seconds):
        with open(log, "a") as handle:
            handle.write("new line\n")

    monkeypatch.setattr(monitor_module.time, "sleep", fake_sleep)
    assert next(follow(str(log))) == "new line\n"


def test_monitor_alerts_once_and_saves(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("LOGSENTINEL_HOME", str(tmp_path))
    lines = [fail_line(s) for s in range(0, 12)]
    monkeypatch.setattr(monitor_module, "follow", lambda path: iter(lines))

    monitor_module.monitor("ignored.log", None)

    out = capsys.readouterr().out
    assert out.count("possible brute force") == 1  # alerted once, not 8 times
    assert [a["rule"] for a in get_alerts(10)] == ["BRUTE_FORCE"]
