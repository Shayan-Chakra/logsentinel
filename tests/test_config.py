from logsentinel.config import DEFAULT_RULES, load_rules


def write(tmp_path, text):
    path = tmp_path / "rules.yaml"
    path.write_text(text)
    return str(path)


def test_new_rules_have_defaults():
    assert DEFAULT_RULES["slow_brute_force"]["failed_attempts"] == 10
    assert DEFAULT_RULES["system_changes"]["enabled"] is True


def test_half_filled_section_keeps_the_other_defaults(tmp_path):
    rules = load_rules(write(tmp_path, "brute_force:\n  failed_attempts: 9\n"))
    assert rules["brute_force"] == {"enabled": True, "failed_attempts": 9, "window_seconds": 300}


def test_switching_a_rule_off_keeps_its_numbers(tmp_path):
    rules = load_rules(write(tmp_path, "password_spray:\n  enabled: false\n"))
    assert rules["password_spray"]["enabled"] is False
    assert rules["password_spray"]["unique_ips"] == 5


def test_allowlist_is_read(tmp_path):
    rules = load_rules(write(tmp_path, "allowlist:\n  ips:\n    - 10.0.0.10\n"))
    assert rules["allowlist"]["ips"] == ["10.0.0.10"]


def test_a_rules_file_that_is_not_a_mapping_falls_back_to_defaults(tmp_path):
    assert load_rules(write(tmp_path, "- just\n- a list\n")) == DEFAULT_RULES


def test_a_section_that_is_not_a_mapping_is_ignored(tmp_path):
    assert load_rules(write(tmp_path, "brute_force: nonsense\n"))["brute_force"] == DEFAULT_RULES["brute_force"]


def test_missing_file_falls_back_to_defaults(tmp_path):
    assert load_rules(str(tmp_path / "nope.yaml")) == DEFAULT_RULES
