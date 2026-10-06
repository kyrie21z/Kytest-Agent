import pytest
from solution import solve


class TestSolve:
    """Unit tests for the solve() function."""

    # --- Basic case-swapping with letters present ---

    def test_all_lowercase(self):
        assert solve("ab") == "AB"

    def test_all_uppercase(self):
        assert solve("AB") == "ab"

    def test_mixed_case(self):
        assert solve("#a@C") == "#A@c"

    def test_single_lowercase_letter(self):
        assert solve("a") == "A"

    def test_single_uppercase_letter(self):
        assert solve("A") == "a"

    # --- Strings with no letters (should reverse the whole string) ---

    def test_all_digits(self):
        assert solve("1234") == "4321"

    def test_empty_string(self):
        assert solve("") == ""

    def test_single_digit(self):
        assert solve("5") == "5"

    def test_special_characters_only(self):
        assert solve("!@#$") == "$#@!"

    def test_spaces_only(self):
        assert solve("   ") == "   "

    def test_mixed_no_letters(self):
        assert solve("1!2@3") == "3@2!1"

    # --- Mixed letters and non-letters ---

    def test_leading_non_letters(self):
        assert solve("12ab") == "12AB"

    def test_trailing_non_letters(self):
        assert solve("ab12") == "AB12"

    def test_interleaved_letters_and_symbols(self):
        assert solve("a#b@c") == "A#B@C"

    def test_numbers_between_letters(self):
        assert solve("a1b2c") == "A1B2C"

    def test_whitespace_between_letters(self):
        assert solve("a b c") == "A B C"

    def test_punctuation_with_letters(self):
        assert solve("hello, world!") == "HELLO, WORLD!"

    def test_underscore_in_string(self):
        assert solve("a_b_c") == "A_B_C"

    # --- Edge cases ---

    def test_longer_string(self):
        assert solve("Python3IsFun") == "pYTHON3iSfUN"

    def test_unicode_letters(self):
        # Unicode letters should also be swapped
        result = solve("café")
        assert result == "CAFÉ"

    def test_numeric_string_with_negative_sign(self):
        assert solve("-123") == "321-"

    def test_tabs_and_newlines(self):
        assert solve("a\tb\n") == "A\tB\n"

    def test_duplicate_chars(self):
        assert solve("aaBBcc") == "AAbbCC"

    def test_alternating_case(self):
        assert solve("AbCdEf") == "aBcDeF"
