import pytest
from solution import count_distinct_characters


class TestCountDistinctCharacters:
    """Tests for the count_distinct_characters function."""

    # --- Docstring examples ---

    def test_docstring_example_xyz(self):
        assert count_distinct_characters('xyzXYZ') == 3

    def test_docstring_example_jerry(self):
        assert count_distinct_characters('Jerry') == 4

    # --- Basic cases ---

    def test_empty_string(self):
        assert count_distinct_characters('') == 0

    def test_single_character(self):
        assert count_distinct_characters('a') == 1

    def test_single_uppercase_character(self):
        assert count_distinct_characters('A') == 1

    def test_all_same_lowercase(self):
        assert count_distinct_characters('aaaa') == 1

    def test_all_same_uppercase(self):
        assert count_distinct_characters('AAAA') == 1

    def test_mixed_case_same_letter(self):
        assert count_distinct_characters('AaAaA') == 1

    # --- Two distinct characters ---

    def test_two_distinct_lowercase(self):
        assert count_distinct_characters('ab') == 2

    def test_two_distinct_uppercase(self):
        assert count_distinct_characters('AB') == 2

    def test_two_distinct_mixed_case(self):
        assert count_distinct_characters('aB') == 2

    def test_two_distinct_repeated(self):
        assert count_distinct_characters('abab') == 2

    def test_two_distinct_mixed_case_repeated(self):
        assert count_distinct_characters('AbBa') == 2

    # --- Case insensitivity ---

    def test_case_insensitive_a_b(self):
        assert count_distinct_characters('aBcDeF') == 6

    def test_case_insensitive_hello(self):
        assert count_distinct_characters('Hello') == 4  # h, e, l, o

    def test_case_insensitive_hello_mixed(self):
        assert count_distinct_characters('hElLo') == 4

    # --- Spaces and special characters ---

    def test_with_spaces(self):
        assert count_distinct_characters('a b') == 3  # a, space, b

    def test_only_spaces(self):
        assert count_distinct_characters('   ') == 1  # just space

    def test_sentence(self):
        result = count_distinct_characters('hello world')
        # h, e, l, o, space, w, r, d = 8
        assert result == 8

    def test_tabs_and_newlines(self):
        assert count_distinct_characters('a\tb\n') == 4  # a, \t, b, \n

    # --- Numbers and special characters ---

    def test_with_numbers(self):
        assert count_distinct_characters('abc123') == 6

    def test_with_special_chars(self):
        assert count_distinct_characters('a!@#') == 4

    def test_alphanumeric_mixed_case(self):
        assert count_distinct_characters('A1b2C3') == 6

    # --- Longer strings ---

    def test_longer_string(self):
        s = 'abcdefghijklmnopqrstuvwxyz'
        assert count_distinct_characters(s) == 26

    def test_longer_string_with_duplicates(self):
        s = 'abcdefghijabcdefghij'
        assert count_distinct_characters(s) == 10

    def test_random_like_string(self):
        assert count_distinct_characters('programming') == 8  # p, r, o, g, a, m, i, n

    # --- Edge cases ---

    def test_unicode_characters(self):
        assert count_distinct_characters('café') == 4  # c, a, f, é

    def test_unicode_case(self):
        # Turkish İ/i edge case — basic unicode handling
        assert count_distinct_characters('İi') == 2

    def test_whitespace_only(self):
        assert count_distinct_characters(' \t\n\r') == 4  # space, tab, newline, carriage return

    def test_alternating_pattern(self):
        assert count_distinct_characters('abababab') == 2

    def test_palindrome(self):
        assert count_distinct_characters('racecar') == 4  # r, a, c, e
