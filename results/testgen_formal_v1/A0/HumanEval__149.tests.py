import pytest
from solution import sorted_list_sum


class TestSortedListSum:
    """Tests for the sorted_list_sum function."""

    # --- Basic functionality ---

    def test_basic_filter_and_sort(self):
        """Filter odd-length strings and sort even-length ones."""
        assert sorted_list_sum(["aa", "a", "aaa"]) == ["aa"]

    def test_multiple_even_strings(self):
        """Multiple even-length strings should be filtered and sorted."""
        assert sorted_list_sum(["ab", "a", "aaa", "cd"]) == ["ab", "cd"]

    def test_empty_list(self):
        """An empty list should return an empty list."""
        assert sorted_list_sum([]) == []

    def test_all_odd_lengths(self):
        """If all strings have odd lengths, result should be empty."""
        assert sorted_list_sum(["a", "abc", "hello"]) == []

    def test_all_even_lengths(self):
        """If all strings have even lengths, only sorting applies."""
        assert sorted_list_sum(["ab", "cd", "ef"]) == ["ab", "cd", "ef"]

    # --- Sorting by length ---

    def test_sort_by_length_ascending(self):
        """Strings should be sorted by length in ascending order."""
        assert sorted_list_sum(["aaaa", "bb", "cc", "dddd"]) == ["bb", "cc", "aaaa", "dddd"]

    def test_single_length_group(self):
        """When all words have the same even length, alphabetical sort applies."""
        assert sorted_list_sum(["zebraa", "applee", "mangoo"]) == ["applee", "mangoo", "zebraa"]

    # --- Alphabetical tie-breaking ---

    def test_alphabetical_order_same_length(self):
        """Same-length strings should be sorted alphabetically."""
        assert sorted_list_sum(["banana", "apple", "cherry"]) == ["apple", "banana", "cherry"]

    def test_mixed_length_with_ties(self):
        """Different lengths with ties within each length group."""
        result = sorted_list_sum(["b", "aa", "a", "cc", "dd", "ee"])
        assert result == ["aa", "cc", "dd", "ee"]

    def test_reverse_alpha_same_length(self):
        """Reverse alphabetical order should be corrected."""
        assert sorted_list_sum(["zz", "yy", "xx"]) == ["xx", "yy", "zz"]

    # --- Duplicates ---

    def test_duplicate_strings(self):
        """Duplicate strings should be preserved in the output."""
        assert sorted_list_sum(["ab", "ab", "cd", "cd"]) == ["ab", "ab", "cd", "cd"]

    def test_duplicate_after_filtering(self):
        """Duplicates among odd-length strings are removed naturally."""
        assert sorted_list_sum(["a", "a", "b"]) == []

    def test_mixed_duplicates_and_unique(self):
        """Mix of duplicates and unique strings."""
        assert sorted_list_sum(["ab", "ab", "cd", "ef", "ef"]) == ["ab", "ab", "cd", "ef", "ef"]

    # --- Edge cases ---

    def test_single_element_even(self):
        """A single even-length string should be returned as-is."""
        assert sorted_list_sum(["hi"]) == ["hi"]

    def test_single_element_odd(self):
        """A single odd-length string should result in empty list."""
        assert sorted_list_sum(["hello"]) == []

    def test_empty_strings(self):
        """Empty strings have length 0 (even), so they should be kept."""
        assert sorted_list_sum(["", "a", ""]) == ["", ""]

    def test_empty_string_with_even_words(self):
        """Empty string sorts before non-empty strings of same length."""
        assert sorted_list_sum(["", "ab", "cd"]) == ["", "ab", "cd"]

    def test_case_sensitive_sorting(self):
        """Sorting should be case-sensitive (uppercase comes before lowercase)."""
        assert sorted_list_sum(["Ab", "ab", "Ba", "ba"]) == ["Ab", "Ba", "ab", "ba"]

    def test_numbers_as_strings(self):
        """Strings that look like numbers should still be treated as strings."""
        assert sorted_list_sum(["1234", "56", "789"]) == ["56", "1234"]

    def test_special_characters(self):
        """Strings with special characters should work correctly."""
        assert sorted_list_sum(["!@", "#$", "%^&*"]) == ["!@", "#$", "%^&*"]

    def test_longer_strings(self):
        """Longer even-length strings should appear after shorter ones."""
        result = sorted_list_sum(["a", "abcd", "e", "ghij", "klmnop"])
        assert result == ["abcd", "ghij", "klmnop"]

    def test_large_input(self):
        """Test with a larger input to ensure correctness."""
        lst = [
            "a", "bb", "ccc", "dddd", "eeeeee",
            "z", "yy", "xxx", "wwww", "vvvvvv"
        ]
        # Odd lengths: "a"(1), "ccc"(3), "z"(1), "xxx"(3) → filtered out
        # Even lengths: "bb"(2), "dddd"(4), "eeeeee"(6), "yy"(2), "wwww"(4), "vvvvvv"(6)
        # Sorted: by length then alpha → ["bb", "yy", "dddd", "wwww", "eeeeee", "vvvvvv"]
        expected = ["bb", "yy", "dddd", "wwww", "eeeeee", "vvvvvv"]
        assert sorted_list_sum(lst) == expected

    def test_preserves_original_list(self):
        """The function should not mutate the original list."""
        original = ["ab", "c", "de"]
        sorted_list_sum(original)
        assert original == ["ab", "c", "de"]

    def test_complex_mixed_scenario(self):
        """A complex mix of lengths, duplicates, and ordering."""
        result = sorted_list_sum(["a", "bb", "ccc", "dddd", "ee", "ff", "ggg", "hhhh"])
        assert result == ["bb", "ee", "ff", "dddd", "hhhh"]
