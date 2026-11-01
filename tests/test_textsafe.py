from logsentinel.textsafe import clean_text, MAX_LENGTH


def test_terminal_escape_codes_are_removed():
    assert "\x1b" not in clean_text("admin\x1b[2J\x1b[31m")


def test_newlines_and_hidden_direction_marks_are_removed():
    out = clean_text("ro\not‮txt.exe")
    assert "\n" not in out and "‮" not in out


def test_very_long_values_are_cut():
    assert len(clean_text("a" * 5000)) == MAX_LENGTH


def test_normal_names_are_unchanged():
    assert clean_text("Administrator") == "Administrator"
    assert clean_text("jane.doe@example.com") == "jane.doe@example.com"
    assert clean_text(None) == ""
