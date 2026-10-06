import pytest
from solution import encrypt


class TestEncrypt:
    def test_basic_example_1(self):
        assert encrypt("hi") == "lm"

    def test_basic_example_2(self):
        assert encrypt("asdfghjkl") == "ewhjklnop"

    def test_basic_example_3(self):
        assert encrypt("gf") == "kj"

    def test_basic_example_4(self):
        assert encrypt("et") == "ix"

    def test_empty_string(self):
        assert encrypt("") == ""

    def test_single_char(self):
        assert encrypt("a") == "e"

    def test_wrapping_z(self):
        # 'z' shifted by 4 -> 'd'
        assert encrypt("z") == "d"

    def test_wrapping_y(self):
        # 'y' shifted by 4 -> 'c'
        assert encrypt("y") == "c"

    def test_all_lowercase(self):
        result = encrypt("abcdefghijklmnopqrstuvwxyz")
        expected = "efghijklmnopqrstuvwxyzabcd"
        assert result == expected

    def test_uppercase_unchanged(self):
        assert encrypt("ABC") == "ABC"

    def test_mixed_case(self):
        # Only lowercase letters are shifted; uppercase pass through unchanged
        assert encrypt("AbCd") == "AfCh"

    def test_numbers_unchanged(self):
        assert encrypt("abc123xyz") == "efg123bcd"

    def test_special_chars_unchanged(self):
        assert encrypt("!@#$%") == "!@#$%"

    def test_spaces_preserved(self):
        assert encrypt("hello world") == "lipps asvph"

    def test_whitespace_chars(self):
        # Only lowercase letters shift; tabs and newlines pass through
        assert encrypt("a\tb\nc") == "e\tf\ng"

    def test_consistent_deterministic(self):
        s = "python"
        assert encrypt(s) == encrypt(s)

    def test_round_trip_not_expected(self):
        """encrypt is not invertible without knowing the shift; just ensure no crash."""
        assert len(encrypt("test")) == len("test")
