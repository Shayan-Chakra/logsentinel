from logsentinel import paths
from logsentinel.config import DEFAULT_RULES, load_rules


def test_home_override_creates_folder(tmp_path, monkeypatch):
    monkeypatch.setenv("LOGSENTINEL_HOME", str(tmp_path / "x"))
    assert paths.data_dir() == tmp_path / "x"
    assert (tmp_path / "x").is_dir()


def test_database_lives_in_data_folder(tmp_path, monkeypatch):
    monkeypatch.setenv("LOGSENTINEL_HOME", str(tmp_path))
    assert paths.db_path() == str(tmp_path / "logsentinel.db")


def test_rules_are_found_in_data_folder(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    (home / "rules.yaml").write_text(
        "brute_force:\n  enabled: false\n  failed_attempts: 9\n  window_seconds: 60\n"
    )
    monkeypatch.setenv("LOGSENTINEL_HOME", str(home))
    monkeypatch.chdir(tmp_path)  # a folder with no rules.yaml
    rules = load_rules()
    assert rules["brute_force"]["failed_attempts"] == 9
    assert rules["password_spray"] == DEFAULT_RULES["password_spray"]  # missing section filled in


def test_defaults_when_no_rules_file(tmp_path, monkeypatch):
    monkeypatch.setenv("LOGSENTINEL_HOME", str(tmp_path / "h"))
    monkeypatch.chdir(tmp_path)
    assert load_rules() == DEFAULT_RULES