"""Unit tests for solution.cycpattern_check."""

import pytest
from solution import cycpattern_check


class TestCycPatternCheckDocstringExamples:
    """Test cases taken directly from the docstring."""

    def test_abcd_abd(self):
        assert cycpattern_check("abcd", "abd") is False

    def test_hello_ell(self):
        assert cycpattern_check("hello", "ell") is True

    def test_whassup_psus(self):
        assert cycpattern_check("whassup", "psus") is False

    def test_abab_baa(self):
        assert cycpattern_check("abab", "baa") is True

    def test_efef_eeff(self):
        assert cycpattern_check("efef", "eeff") is False

    def test_himenss_simen(self):
        assert cycpattern_check("himenss", "simen") is True


class TestCycPatternCheckExactMatch:
    """When b exactly matches a, or b is a substring of a."""

    def test_exact_match(self):
        assert cycpattern_check("abc", "abc") is True

    def test_b_is_substring(self):
        assert cycpattern_check("abcdef", "bcd") is True

    def test_b_at_start(self):
        assert cycpattern_check("abcdef", "abc") is True

    def test_b_at_end(self):
        assert cycpattern_check("abcdef", "def") is True


class TestCycPatternCheckRotations:
    """Tests where a rotation of b is found in a."""

    def test_rotation_found(self):
        # Rotation "cab" of "abc" is in "zcabx"
        assert cycpattern_check("zcabx", "abc") is True

    def test_full_rotation(self):
        # Full rotation of "abc" is "bca"
        assert cycpattern_check("xbca", "abc") is True

    def test_multi_char_rotation(self):
        # Rotation "world" of "orldw" is in "helloworld"
        assert cycpattern_check("helloworld", "orldw") is True

    def test_single_char_no_rotation_needed(self):
        assert cycpattern_check("xyz", "y") is True

    def test_all_same_chars_in_b(self):
        # All rotations of "aaa" are "aaa"
        assert cycpattern_check("baaac", "aaa") is True

    def test_palindrome_like_b(self):
        # "aba" rotations: "aba", "baa", "aab" — "aba" is in "xabay"
        assert cycpattern_check("xabay", "aba") is True


class TestCycPatternCheckEmptyStrings:
    """Edge cases involving empty strings."""

    def test_empty_b(self):
        assert cycpattern_check("anything", "") is True

    def test_empty_a_with_nonempty_b(self):
        assert cycpattern_check("", "a") is False

    def test_both_empty(self):
        assert cycpattern_check("", "") is True


class TestCycPatternCheckBLongerThanA:
    """When b (or any rotation) is longer than a, it cannot be a substring."""

    def test_b_longer_than_a(self):
        assert cycpattern_check("ab", "abcd") is False

    def test_b_much_longer(self):
        assert cycpattern_check("a", "abcde") is False


class TestCycPatternCheckNoMatch:
    """Cases where no rotation of b appears in a."""

    def test_completely_different_chars(self):
        assert cycpattern_check("abc", "xyz") is False

    def test_partial_overlap_but_no_rotation(self):
        assert cycpattern_check("abcde", "fgh") is False

    def test_one_char_differs(self):
        assert cycpattern_check("abc", "abd") is False


class TestCycPatternCheckSingleCharacter:
    """Edge cases with single-character strings."""

    def test_single_char_match(self):
        assert cycpattern_check("abc", "b") is True

    def test_single_char_no_match(self):
        assert cycpattern_check("abc", "d") is False

    def test_both_single_char_same(self):
        assert cycpattern_check("a", "a") is True

    def test_both_single_char_different(self):
        assert cycpattern_check("a", "b") is False


class TestCycPatternCheckRepeatingPatterns:
    """Tests with repeating patterns in a and/or b."""

    def test_repeating_a(self):
        # "ab" rotations: "ab", "ba" — "ab" is in "abab"
        assert cycpattern_check("abab", "ab") is True

    def test_repeating_b(self):
        # "abab" rotations include "abab", "baba", "abab", "baba"
        assert cycpattern_check("xbabax", "abab") is True

    def test_long_repeating_pattern(self):
        assert cycpattern_check("aaaa", "aa") is True

    def test_alternating_pattern(self):
        # "abab" rotations: "abab", "baba", "abab", "baba"
        assert cycpattern_check("zbabaw", "abab") is True


class TestCycPatternCheckCaseSensitivity:
    """Verify that the comparison is case-sensitive."""

    def test_case_mismatch(self):
        assert cycpattern_check("ABC", "abc") is False

    def test_case_match(self):
        assert cycpattern_check("Hello", "ell") is True

    def test_mixed_case(self):
        assert cycpattern_check("AbCaB", "abc") is False
