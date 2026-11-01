from logsentinel.textsafe import clean_text, MAX_LENGTH

ESC = chr(27)
RLO = chr(0x202e)  # the "right-to-left override" character, used to fake file names


def test_terminal_escape_codes_are_removed():
    assert ESC not in clean_text("admin" + ESC + "[2J" + ESC + "[31m")


def test_newlines_and_hidden_direction_marks_are_removed():
    out = clean_text("ro" + chr(10) + "ot" + RLO + "txt.exe")
    assert chr(10) not in out and RLO not in out


def test_very_long_values_are_cut():
    assert len(clean_text("a" * 5000)) == MAX_LENGTH


def test_normal_names_are_unchanged():
    assert clean_text("Administrator") == "Administrator"
    assert clean_text("jane.doe@example.com") == "jane.doe@example.com"
    assert clean_text(None) == ""
