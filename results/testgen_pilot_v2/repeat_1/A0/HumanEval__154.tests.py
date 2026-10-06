"""Unit tests for solution.cycpattern_check."""

import pytest
from solution import cycpattern_check


class TestCycpatternCheckBasic:
    """Test cases directly from the docstring examples."""

    def test_false_no_match(self):
        assert cycpattern_check("abcd", "abd") is False

    def test_true_direct_substring(self):
        assert cycpattern_check("hello", "ell") is True

    def test_false_no_rotation_match(self):
        assert cycpattern_check("whassup", "psus") is False

    def test_true_rotation_match(self):
        assert cycpattern_check("abab", "baa") is True

    def test_false_no_match_different_length(self):
        assert cycpattern_check("efef", "eeff") is False

    def test_true_another_rotation(self):
        assert cycpattern_check("himenss", "simen") is True


class TestCycpatternCheckEmptyStrings:
    """Edge cases involving empty strings."""

    def test_empty_b_returns_true(self):
        # An empty string is a substring of any string
        assert cycpattern_check("abc", "") is True

    def test_both_empty_returns_true(self):
        assert cycpattern_check("", "") is True

    def test_empty_a_nonempty_b_returns_false(self):
        assert cycpattern_check("", "a") is False


class TestCycpatternCheckEqualStrings:
    """When both strings are equal, b is trivially a substring of a."""

    def test_equal_strings_return_true(self):
        assert cycpattern_check("hello", "hello") is True

    def test_equal_single_char(self):
        assert cycpattern_check("a", "a") is True

    def test_equal_multi_char(self):
        assert cycpattern_check("abcdef", "abcdef") is True


class TestCycpatternCheckRotationCases:
    """Test various cyclic rotations of b being substrings of a."""

    def test_first_rotation_matches(self):
        # "bcd" is a rotation of "abcd" and is in "xabcdy"
        assert cycpattern_check("xabcdy", "abcd") is True

    def test_last_rotation_matches(self):
        # "dabc" is a rotation of "abcd" and is in "xdabc"
        assert cycpattern_check("xdabc", "abcd") is True

    def test_middle_rotation_matches(self):
        # "bcda" is a rotation of "abcd" and is in "xbcda"
        assert cycpattern_check("xbcda", "abcd") is True

    def test_single_char_b_always_true_if_present(self):
        assert cycpattern_check("hello", "h") is True

    def test_single_char_b_not_present(self):
        assert cycpattern_check("hello", "z") is False

    def test_single_char_b_with_empty_a(self):
        assert cycpattern_check("", "x") is False


class TestCycpatternCheckBLongerThanA:
    """When b is longer than a, no rotation can be a substring."""

    def test_b_longer_than_a(self):
        assert cycpattern_check("ab", "abcde") is False

    def test_b_much_longer_than_a(self):
        assert cycpattern_check("a", "longstring") is False


class TestCycpatternCheckSpecialCharacters:
    """Test with special characters and numbers."""

    def test_special_chars_in_b(self):
        assert cycpattern_check("hello!world", "!wor") is True

    def test_numbers_correct_rotation(self):
        # Rotations of "123": "123", "231", "312"
        assert cycpattern_check("x231y", "123") is True
        assert cycpattern_check("x312y", "123") is True
        assert cycpattern_check("x123y", "123") is True

    def test_numbers_no_rotation_match(self):
        # "451" is not a rotation of "12345" (different length)
        assert cycpattern_check("12345", "451") is False


class TestCycpatternCheckRepeatedPatterns:
    """Test with repeated character patterns."""

    def test_all_same_chars_b_shorter(self):
        assert cycpattern_check("aaaaa", "aa") is True

    def test_all_same_chars_b_equal(self):
        assert cycpattern_check("aaa", "aaa") is True

    def test_repeated_pattern_in_a(self):
        # "ab" rotations: "ab", "ba"
        assert cycpattern_check("ababab", "ab") is True
        assert cycpattern_check("ababab", "ba") is True


class TestCycpatternCheckBoundaryConditions:
    """Boundary and edge cases."""

    def test_b_at_start_of_a(self):
        assert cycpattern_check("hello", "hel") is True

    def test_b_at_end_of_a(self):
        assert cycpattern_check("hello", "llo") is True

    def test_b_in_middle_of_a(self):
        assert cycpattern_check("hello", "ell") is True

    def test_b_equals_a(self):
        assert cycpattern_check("test", "test") is True

    def test_b_is_one_char_less_than_a(self):
        assert cycpattern_check("abcde", "abcd") is True
        assert cycpattern_check("abcde", "bcde") is True
        # "eabc" is not a rotation of "abcd" (contains 'e'), use correct rotation
        assert cycpattern_check("abcde", "dabc") is True  # rotation of "abcd"

    def test_b_is_one_char_more_than_a(self):
        assert cycpattern_check("abc", "abcd") is False


class TestCycpatternCheckReturnTypes:
    """Ensure correct return types."""

    def test_returns_boolean_true(self):
        result = cycpattern_check("hello", "ell")
        assert isinstance(result, bool)
        assert result is True

    def test_returns_boolean_false(self):
        result = cycpattern_check("abcd", "abd")
        assert isinstance(result, bool)
        assert result is False
