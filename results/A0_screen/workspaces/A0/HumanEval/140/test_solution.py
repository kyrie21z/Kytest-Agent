import pytest
from solution import fix_spaces


class TestFixSpaces:
    """Tests for the fix_spaces function."""

    # --- Docstring examples ---
    def test_no_spaces(self):
        assert fix_spaces("Example") == "Example"

    def test_single_space(self):
        assert fix_spaces("Example 1") == "Example_1"

    def test_leading_space(self):
        assert fix_spaces(" Example 2") == "_Example_2"

    def test_three_consecutive_spaces(self):
        assert fix_spaces(" Example   3") == "_Example-3"

    # --- Edge cases: empty string ---
    def test_empty_string(self):
        assert fix_spaces("") == ""

    # --- Edge cases: only spaces ---
    def test_only_two_spaces(self):
        assert fix_spaces("  ") == "__"

    def test_only_three_spaces(self):
        assert fix_spaces("   ") == "-"

    def test_only_four_spaces(self):
        assert fix_spaces("    ") == "-"

    def test_only_five_spaces(self):
        assert fix_spaces("     ") == "-"

    def test_only_ten_spaces(self):
        assert fix_spaces("          ") == "-"

    # --- Single and double spaces ---
    def test_single_space_replaced_with_underscore(self):
        assert fix_spaces("a b") == "a_b"

    def test_double_space_replaced_with_two_underscores(self):
        assert fix_spaces("a  b") == "a__b"

    def test_multiple_single_spaces(self):
        assert fix_spaces("a b c d") == "a_b_c_d"

    # --- Three or more consecutive spaces become dash ---
    def test_three_spaces_between_words(self):
        assert fix_spaces("a   b") == "a-b"

    def test_four_spaces_between_words(self):
        assert fix_spaces("a    b") == "a-b"

    def test_five_spaces_between_words(self):
        assert fix_spaces("a     b") == "a-b"

    def test_many_spaces_between_words(self):
        assert fix_spaces("a          b") == "a-b"

    # --- Mixed scenarios ---
    def test_mixed_spaces_and_consecutive(self):
        assert fix_spaces("a b  c   d") == "a_b__c-d"

    def test_trailing_consecutive_spaces(self):
        assert fix_spaces("hello   ") == "hello-"

    def test_leading_consecutive_spaces(self):
        assert fix_spaces("   hello") == "-hello"

    def test_leading_and_trailing_spaces(self):
        assert fix_spaces("  hello  ") == "__hello__"

    def test_consecutive_spaces_at_start_middle_end(self):
        assert fix_spaces("  a   b  c   ") == "__a-b__c-"

    # --- Single character strings ---
    def test_single_character_no_space(self):
        assert fix_spaces("a") == "a"

    def test_single_space(self):
        assert fix_spaces(" ") == "_"

    def test_two_spaces(self):
        assert fix_spaces("  ") == "__"

    # --- Strings with special characters ---
    def test_special_chars_with_spaces(self):
        assert fix_spaces("! @ #") == "!_@_#"

    def test_numbers_with_spaces(self):
        assert fix_spaces("1 2 3") == "1_2_3"

    def test_numbers_with_consecutive_spaces(self):
        assert fix_spaces("1   2   3") == "1-2-3"

    # --- Long strings ---
    def test_long_string_with_various_spaces(self):
        text = "a b  c   d    e     f"
        result = fix_spaces(text)
        assert result == "a_b__c-d-e-f"

    def test_all_same_char_no_spaces(self):
        assert fix_spaces("aaaaa") == "aaaaa"

    def test_all_spaces(self):
        assert fix_spaces("      ") == "-"
