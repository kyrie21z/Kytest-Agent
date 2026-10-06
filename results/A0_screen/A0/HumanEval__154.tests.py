import pytest
from solution import cycpattern_check


class TestCycpatternCheckBasicCases:
    """Test cases directly from the docstring."""

    def test_false_no_match(self):
        assert cycpattern_check("abcd", "abd") is False

    def test_true_direct_substring(self):
        assert cycpattern_check("hello", "ell") is True

    def test_false_no_rotation_match(self):
        assert cycpattern_check("whassup", "psus") is False

    def test_true_rotation_match(self):
        assert cycpattern_check("abab", "baa") is True

    def test_false_no_match_longer(self):
        assert cycpattern_check("efef", "eeff") is False

    def test_true_rotation_match_2(self):
        assert cycpattern_check("himenss", "simen") is True


class TestCycpatternCheckEmptyStrings:
    """Edge cases involving empty strings."""

    def test_empty_b_returns_true(self):
        assert cycpattern_check("hello", "") is True

    def test_empty_a_with_nonempty_b(self):
        assert cycpattern_check("", "a") is False

    def test_both_empty(self):
        assert cycpattern_check("", "") is True


class TestCycpatternCheckIdenticalStrings:
    """When both strings are identical."""

    def test_identical_strings(self):
        assert cycpattern_check("abc", "abc") is True

    def test_identical_single_char(self):
        assert cycpattern_check("a", "a") is True


class TestCycpatternCheckSingleCharacterB:
    """When b is a single character."""

    def test_single_char_in_string(self):
        assert cycpattern_check("hello", "e") is True

    def test_single_char_not_in_string(self):
        assert cycpattern_check("hello", "z") is False

    def test_single_char_at_start(self):
        assert cycpattern_check("hello", "h") is True

    def test_single_char_at_end(self):
        assert cycpattern_check("hello", "o") is True


class TestCycpatternCheckRotationMatching:
    """Tests specifically for cyclic rotation matching."""

    def test_first_rotation_matches(self):
        # "ab" rotated by 1 -> "ba", which is in "cba"
        assert cycpattern_check("cba", "ab") is True

    def test_second_rotation_matches(self):
        # "abc" rotated by 1 -> "bca", which is in "xbca"
        assert cycpattern_check("xbca", "abc") is True

    def test_last_rotation_matches(self):
        # "abc" rotated by 2 -> "cab", which is in "xcab"
        assert cycpattern_check("xcab", "abc") is True

    def test_full_rotation_equals_original(self):
        # Rotating "abc" by 3 gives "abc" again
        assert cycpattern_check("abc", "abc") is True

    def test_repeated_pattern(self):
        # "ab" rotations: "ab", "ba". "ba" is in "ababa"
        assert cycpattern_check("ababa", "ab") is True

    def test_all_rotations_same(self):
        # "aa" rotations are all "aa"
        assert cycpattern_check("aaa", "aa") is True


class TestCycpatternCheckNoMatch:
    """Tests where no rotation of b is a substring of a."""

    def test_different_lengths_no_match(self):
        assert cycpattern_check("abc", "abcd") is False

    def test_completely_different_chars(self):
        assert cycpattern_check("xyz", "abc") is False

    def test_partial_overlap_but_no_rotation(self):
        assert cycpattern_check("abcdef", "axc") is False

    def test_b_longer_than_a(self):
        assert cycpattern_check("ab", "abcdef") is False


class TestCycpatternCheckLongerStrings:
    """Tests with longer strings."""

    def test_long_string_with_matching_rotation(self):
        a = "thisisaverylongstring"
        b = "verylon"
        # "verylon" is directly in "thisisaverylongstring" (at index 7)
        assert cycpattern_check(a, b) is True

    def test_long_string_with_matching_rotation_2(self):
        a = "abcdefghij"
        b = "fghij"
        # "fghij" is directly in "abcdefghij"
        assert cycpattern_check(a, b) is True

    def test_long_string_with_rotated_match(self):
        a = "xxabcdefghijyy"
        b = "fghij"
        # "fghij" is in a
        assert cycpattern_check(a, b) is True

    def test_long_string_no_match(self):
        a = "thisisaverylongstring"
        b = "xyz"
        # "xyz" and all its rotations are not in a
        assert cycpattern_check(a, b) is False


class TestCycpatternCheckSpecialCharacters:
    """Tests with special characters and numbers."""

    def test_numbers(self):
        assert cycpattern_check("12345", "345") is True

    def test_numbers_rotation(self):
        # "345" rotations: "345", "453", "534"
        # None of these are in "51234"
        assert cycpattern_check("51234", "345") is False

    def test_numbers_rotation_match(self):
        # "345" rotations: "345", "453", "534"
        # "534" is in "15342"
        assert cycpattern_check("15342", "345") is True

    def test_mixed_alphanumeric(self):
        assert cycpattern_check("abc123def", "123") is True

    def test_special_chars(self):
        assert cycpattern_check("!@#$%", "@#$") is True


class TestCycpatternCheckCaseSensitivity:
    """Tests for case sensitivity."""

    def test_case_sensitive(self):
        assert cycpattern_check("Hello", "ELL") is False

    def test_lowercase_match(self):
        assert cycpattern_check("hello", "ell") is True

    def test_uppercase_match(self):
        assert cycpattern_check("HELLO", "ELL") is True


class TestCycpatternCheckEdgeRotations:
    """Tests for edge cases in rotation logic."""

    def test_two_char_b(self):
        # "ab" rotations: "ab", "ba"
        assert cycpattern_check("xba", "ab") is True

    def test_three_char_b_all_rotations(self):
        # "abc" rotations: "abc", "bca", "cab"
        assert cycpattern_check("xbca", "abc") is True
        assert cycpattern_check("xcab", "abc") is True
        assert cycpattern_check("xabc", "abc") is True

    def test_four_char_b(self):
        # "abcd" has rotations: abcd, bcda, cdab, dabc
        assert cycpattern_check("xcdab", "abcd") is True
        assert cycpattern_check("xdabc", "abcd") is True
        assert cycpattern_check("xbcda", "abcd") is True

    def test_b_length_equals_a_length(self):
        assert cycpattern_check("abc", "abc") is True
        # "bca" rotations: "bca", "cab", "abc" -> "abc" is in "abc"
        assert cycpattern_check("abc", "bca") is True
        # "cab" rotations: "cab", "abc", "bca" -> "abc" is in "abc"
        assert cycpattern_check("abc", "cab") is True


class TestCycpatternCheckRepeatedPatterns:
    """Tests with repeated patterns."""

    def test_repeated_ab(self):
        # "ab" rotations: "ab", "ba"
        assert cycpattern_check("abab", "ab") is True
        assert cycpattern_check("abab", "ba") is True

    def test_repeated_abc(self):
        # "abc" rotations: "abc", "bca", "cab"
        assert cycpattern_check("abcabc", "abc") is True
        assert cycpattern_check("abcabc", "bca") is True
        assert cycpattern_check("abcabc", "cab") is True

    def test_repeated_single_char(self):
        assert cycpattern_check("aaaa", "aa") is True
