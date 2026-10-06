import pytest
from solution import how_many_times


class TestHowManyTimesBasic:
    """Test basic functionality of how_many_times."""

    def test_empty_string(self):
        assert how_many_times('', 'a') == 0

    def test_empty_substring_in_nonempty_string(self):
        # Empty substring matches at each starting index (loop-based)
        assert how_many_times('abc', '') == 3

    def test_both_empty(self):
        assert how_many_times('', '') == 0

    def test_single_char_match(self):
        assert how_many_times('a', 'a') == 1

    def test_no_match(self):
        assert how_many_times('abc', 'd') == 0

    def test_partial_no_match(self):
        assert how_many_times('abc', 'ac') == 0


class TestHowManyTimesOverlapping:
    """Test overlapping substring counting."""

    def test_overlapping_aa_in_aaaa(self):
        assert how_many_times('aaaa', 'aa') == 3

    def test_overlapping_abab_in_ababab(self):
        assert how_many_times('ababab', 'abab') == 2

    def test_overlapping_aba_in_ababa(self):
        assert how_many_times('ababa', 'aba') == 2

    def test_overlapping_aaa_in_aaaa(self):
        assert how_many_times('aaaa', 'aaa') == 2

    def test_overlapping_a_in_aaa(self):
        assert how_many_times('aaa', 'a') == 3

    def test_overlapping_pattern(self):
        assert how_many_times('aaaaa', 'aa') == 4


class TestHowManyTimesNonOverlapping:
    """Test cases where substrings don't overlap."""

    def test_non_overlapping_hello_world(self):
        assert how_many_times('hello world hello', 'hello') == 2

    def test_non_overlapping_spaces(self):
        assert how_many_times('a b a b a', 'a b') == 2

    def test_exact_match(self):
        assert how_many_times('abc', 'abc') == 1

    def test_longer_substring(self):
        assert how_many_times('abc', 'abcd') == 0


class TestHowManyTimesEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_substring_longer_than_string(self):
        assert how_many_times('ab', 'abc') == 0

    def test_substring_equals_string(self):
        assert how_many_times('abc', 'abc') == 1

    def test_multiple_occurrences(self):
        assert how_many_times('abababab', 'ab') == 4

    def test_special_characters(self):
        assert how_many_times('a!b!c!', '!') == 3

    def test_whitespace_substring(self):
        assert how_many_times('a b c', ' ') == 2

    def test_newline_substring(self):
        assert how_many_times('a\nb\nc', '\n') == 2

    def test_unicode_characters(self):
        assert how_many_times('café café', 'café') == 2

    def test_case_sensitive(self):
        assert how_many_times('AbCaBcA', 'a') == 1

    def test_all_same_chars(self):
        assert how_many_times('aaaaa', 'a') == 5

    def test_alternating_pattern(self):
        assert how_many_times('ababab', 'ab') == 3


class TestHowManyTimesDoctests:
    """Verify the examples from the docstring pass."""

    def test_docstring_example_1(self):
        assert how_many_times('', 'a') == 0

    def test_docstring_example_2(self):
        assert how_many_times('aaa', 'a') == 3

    def test_docstring_example_3(self):
        assert how_many_times('aaaa', 'aa') == 3
