import sys

from logsentinel.elevate import build_command, relaunch_as_admin


def test_running_from_python_uses_the_module():
    program, params = build_command(["start", "--hours", "24"], frozen=False, executable="C:\\v\\python.exe")
    assert program == "C:\\v\\python.exe"
    assert params == "-m logsentinel.cli start --hours 24"


def test_packaged_exe_runs_itself():
    program, params = build_command(["start"], frozen=True, executable="C:\\x\\logsentry.exe")
    assert program == "C:\\x\\logsentry.exe"
    assert params == "start"


def test_paths_with_spaces_are_quoted():
    _, params = build_command(["start", "--rules", "C:\\My Rules\\r.yaml"], frozen=True, executable="x")
    assert params == 'start --rules "C:\\My Rules\\r.yaml"'


def test_cannot_elevate_when_not_windows(monkeypatch):
    monkeypatch.setattr(sys, "platform", "linux")
    assert relaunch_as_admin(["start"]) is False