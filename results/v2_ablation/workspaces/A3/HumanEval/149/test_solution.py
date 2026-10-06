"""Unit tests for sorted_list_sum."""

import pytest
from solution import sorted_list_sum


class TestSortedListSumBasic:
    """Tests covering normal / typical inputs."""

    def test_basic_filter_and_sort(self):
        """Example from docstring: keep even-length, drop odd-length."""
        result = sorted_list_sum(["aa", "a", "aaa"])
        assert result == ["aa"]

    def test_multiple_even_length_words(self):
        """Example from docstring: multiple even-length words kept."""
        result = sorted_list_sum(["ab", "a", "aaa", "cd"])
        assert result == ["ab", "cd"]

    def test_same_length_alphabetical_sort(self):
        """Words of equal length should be sorted alphabetically."""
        result = sorted_list_sum(["zz", "aa", "mm"])
        assert result == ["aa", "mm", "zz"]

    def test_mixed_lengths_then_alpha(self):
        """Different lengths sorted by length; ties broken alphabetically."""
        result = sorted_list_sum(["aaaa", "bb", "cc", "dddd", "ee"])
        assert result == ["bb", "cc", "ee", "aaaa", "dddd"]

    def test_duplicates_preserved(self):
        """Duplicate strings should appear in the output."""
        result = sorted_list_sum(["ab", "ab", "cd"])
        assert result == ["ab", "ab", "cd"]

    def test_dups_with_different_lengths(self):
        """Duplicates across different lengths are all kept."""
        result = sorted_list_sum(["abcd", "ab", "abcd", "ef"])
        assert result == ["ab", "ef", "abcd", "abcd"]

    def test_already_sorted_input(self):
        """Input already in correct order should return unchanged."""
        result = sorted_list_sum(["ab", "cd", "efgh"])
        assert result == ["ab", "cd", "efgh"]

    def test_reverse_order_input(self):
        """Input in reverse order should still be correctly sorted."""
        result = sorted_list_sum(["zzzz", "yy", "xx", "wwwwww"])
        assert result == ["xx", "yy", "zzzz", "wwwwww"]


class TestSortedListSumBoundary:
    """Tests at the edges of valid input ranges."""

    def test_single_even_length_element(self):
        """One element with even length — should be returned."""
        result = sorted_list_sum(["ab"])
        assert result == ["ab"]

    def test_single_odd_length_element(self):
        """One element with odd length — should be filtered out."""
        result = sorted_list_sum(["abc"])
        assert result == []

    def test_all_elements_have_odd_lengths(self):
        """Every string has odd length — entire list filtered."""
        result = sorted_list_sum(["a", "bbb", "hello"])
        assert result == []

    def test_all_elements_have_even_lengths(self):
        """Every string has even length — all kept and sorted."""
        result = sorted_list_sum(["dc", "ba", "fe"])
        assert result == ["ba", "dc", "fe"]

    def test_empty_string_is_kept(self):
        """Empty string has length 0 (even) — should be kept."""
        result = sorted_list_sum(["", "ab", ""])
        assert result == ["", "", "ab"]

    def test_longest_strings_at_end(self):
        """Longer strings should appear after shorter ones."""
        result = sorted_list_sum(
            ["a", "bc", "defg", "hijklmno", "pqrstuvwxy"]
        )
        assert result == ["bc", "defg", "hijklmno", "pqrstuvwxy"]

    def test_many_same_length_words(self):
        """All same odd-length words — all filtered out."""
        # All have length 5 (odd)
        words = ["zebra", "apple", "mango", "peach", "grape"]
        result = sorted_list_sum(words)
        assert result == []

    def test_many_same_even_length_words(self):
        """All same even-length words sorted alphabetically."""
        # All have length 6 (even)
        words = ["zebraa", "applee", "mangoo", "banann", "cherry"]
        result = sorted_list_sum(words)
        assert result == ["applee", "banann", "cherry", "mangoo", "zebraa"]


class TestSortedListSumEmptyAndEdge:
    """Tests for empty, zero-size, and minimal inputs."""

    def test_empty_list(self):
        """Empty list should return an empty list."""
        result = sorted_list_sum([])
        assert result == []

    def test_only_odd_length_strings(self):
        """List containing only odd-length strings returns empty."""
        result = sorted_list_sum(["x", "yyy", "zzzzz"])
        assert result == []

    def test_only_even_length_strings(self):
        """List containing only even-length strings returns sorted copy."""
        result = sorted_list_sum(["ab", "cd", "ef"])
        assert result == ["ab", "cd", "ef"]

    def test_single_empty_string(self):
        """A single empty string (length 0) is kept."""
        result = sorted_list_sum([""])
        assert result == [""]

    def test_alternating_even_odd_lengths(self):
        """Alternating even/odd lengths interleaved."""
        result = sorted_list_sum(["a", "bb", "ccc", "dddd", "eeeeee"])
        assert result == ["bb", "dddd", "eeeeee"]


class TestSortedListSumSpecialCases:
    """Additional edge and special-case scenarios."""

    def test_case_sensitive_sorting(self):
        """Sorting should respect lexicographic (ASCII) ordering."""
        result = sorted_list_sum(["Bb", "Aa", "Cc"])
        assert result == ["Aa", "Bb", "Cc"]

    def test_numbers_as_strings(self):
        """Strings that look like numbers are treated as regular strings."""
        result = sorted_list_sum(["12", "3456", "78"])
        assert result == ["12", "78", "3456"]

    def test_spaces_in_strings(self):
        """Strings containing spaces are handled normally.
        'ab cd' has 5 chars (odd) -> filtered out.
        'ef' has 2 chars (even) -> kept.
        'gh ij kl' has 8 chars (even) -> kept.
        """
        result = sorted_list_sum(["ab cd", "ef", "gh ij kl"])
        assert result == ["ef", "gh ij kl"]

    def test_special_characters(self):
        """Strings with special characters are sorted by ASCII value."""
        result = sorted_list_sum(["!@", "#$", "%^"])
        assert result == ["!@", "#$", "%^"]

    def test_large_list(self):
        """A larger list exercises sorting correctness."""
        data = [
            "a", "bb", "ccc", "dddd", "eeee", "fffff",
            "gggggg", "hhhhhhi", "jjjjjjkk", "lllllll"
        ]
        result = sorted_list_sum(data)
        expected = ["bb", "dddd", "eeee", "gggggg", "jjjjjjkk"]
        assert result == expected

    def test_all_duplicates_same_length(self):
        """All identical strings of even length."""
        result = sorted_list_sum(["ab", "ab", "ab"])
        assert result == ["ab", "ab", "ab"]

    def test_all_duplicates_different_lengths(self):
        """Identical strings appearing at different positions."""
        result = sorted_list_sum(["ab", "abcd", "ab", "abcd"])
        assert result == ["ab", "ab", "abcd", "abcd"]
