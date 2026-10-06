"""Unit tests for sorted_list_sum."""

import pytest
from solution import sorted_list_sum


# ---------------------------------------------------------------------------
# Docstring examples
# ---------------------------------------------------------------------------

class TestDocstringExamples:
    def test_example_1(self):
        assert sorted_list_sum(["aa", "a", "aaa"]) == ["aa"]

    def test_example_2(self):
        assert sorted_list_sum(["ab", "a", "aaa", "cd"]) == ["ab", "cd"]


# ---------------------------------------------------------------------------
# Normal cases – typical inputs
# ---------------------------------------------------------------------------

class TestNormalCases:
    def test_all_even_length_strings(self):
        """All strings have even length; returned sorted alphabetically."""
        assert sorted_list_sum(["bb", "aa", "cc"]) == ["aa", "bb", "cc"]

    def test_mixed_lengths_sorted_by_length_then_alpha(self):
        """Strings of different even lengths are ordered by length, then alpha."""
        assert sorted_list_sum(["aaaa", "bbbb", "aa", "bb"]) == [
            "aa",
            "bb",
            "aaaa",
            "bbbb",
        ]

    def test_duplicates_preserved_and_sorted(self):
        """Duplicate strings are kept and appear in sorted order."""
        assert sorted_list_sum(["aaaa", "bbbb", "cccc", "aaaa"]) == [
            "aaaa",
            "aaaa",
            "bbbb",
            "cccc",
        ]

    def test_same_length_alphabetical_tie_break(self):
        """Same-length strings are sorted alphabetically."""
        assert sorted_list_sum(["ab", "ba", "cd", "dc"]) == [
            "ab",
            "ba",
            "cd",
            "dc",
        ]

    def test_longer_words_with_odd_filtered(self):
        """Only even-length words survive filtering."""
        # "hello"(5), "world"(5), "python"(6) -> keep "hi"(2), "python"(6)
        assert sorted_list_sum(["hello", "hi", "world", "python"]) == [
            "hi",
            "python",
        ]

    def test_many_strings_different_even_lengths(self):
        """Multiple distinct even lengths interleaved with odd ones."""
        assert sorted_list_sum(["a", "bb", "ccc", "dddd", "eeeee"]) == [
            "bb",
            "dddd",
        ]

    def test_all_same_even_length(self):
        """When every word has the same even length, pure alphabetical sort."""
        # All 6-char words
        assert sorted_list_sum(["zebras", "apples", "mangos"]) == [
            "apples",
            "mangos",
            "zebras",
        ]


# ---------------------------------------------------------------------------
# Boundary cases – edges of valid input ranges
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    def test_single_even_string(self):
        assert sorted_list_sum(["bb"]) == ["bb"]

    def test_single_odd_string(self):
        assert sorted_list_sum(["a"]) == []

    def test_two_strings_both_even(self):
        assert sorted_list_sum(["zz", "aa"]) == ["aa", "zz"]

    def test_two_strings_one_even_one_odd(self):
        assert sorted_list_sum(["a", "bb"]) == ["bb"]

    def test_two_strings_both_odd(self):
        assert sorted_list_sum(["a", "b"]) == []

    def test_empty_string_among_others(self):
        # "" has length 0 (even), so it survives and sorts first.
        assert sorted_list_sum(["", "a", "bb"]) == ["", "bb"]

    def test_only_empty_strings(self):
        assert sorted_list_sum(["", "", ""]) == ["", "", ""]

    def test_largest_common_even_length_words(self):
        """Words of length 10 (a common max for short-test assertions)."""
        result = sorted_list_sum(
            [
                "abcdefghij",
                "aaaaaaaaaa",
                "jjjjjjjjjj",
            ]
        )
        assert result == ["aaaaaaaaaa", "abcdefghij", "jjjjjjjjjj"]


# ---------------------------------------------------------------------------
# Empty / null-like inputs
# ---------------------------------------------------------------------------

class TestEmptyInputs:
    def test_empty_list(self):
        assert sorted_list_sum([]) == []

    def test_single_empty_string(self):
        assert sorted_list_sum([""]) == [""]


# ---------------------------------------------------------------------------
# Edge-case combinations
# ---------------------------------------------------------------------------

class TestEdgeCaseCombinations:
    def test_no_even_strings_at_all(self):
        assert sorted_list_sum(["x", "yyz", "abcde"]) == []

    def test_duplicate_after_filtering(self):
        """Duplicates that survive the filter remain in output."""
        assert sorted_list_sum(["ab", "cd", "ab", "ef"]) == [
            "ab",
            "ab",
            "cd",
            "ef",
        ]

    def test_reverse_order_input(self):
        """Input already in reverse-sorted order should still produce correct output."""
        assert sorted_list_sum(["zz", "yy", "xx", "ww"]) == [
            "ww",
            "xx",
            "yy",
            "zz",
        ]

    def test_case_sensitive_sorting(self):
        """Sorting is case-sensitive (uppercase < lowercase in ASCII)."""
        assert sorted_list_sum(["Ab", "ab", "Ba", "ba"]) == [
            "Ab",
            "Ba",
            "ab",
            "ba",
        ]

    def test_numbers_as_strings(self):
        """Numeric-looking strings are treated as plain strings."""
        assert sorted_list_sum(["12", "3456", "78"]) == ["12", "78", "3456"]

    def test_whitespace_in_strings(self):
        """Whitespace characters count toward length."""
        # " " has length 1 (odd) -> filtered out
        # "  " has length 2 (even) -> kept
        assert sorted_list_sum([" ", "  ", "   "]) == ["  "]
