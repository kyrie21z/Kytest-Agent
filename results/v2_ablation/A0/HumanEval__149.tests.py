import pytest
from solution import sorted_list_sum


class TestSortedListSum:
    """Tests for the sorted_list_sum function."""

    # --- Basic functionality ---

    def test_basic_filter_and_sort(self):
        """Filter odd-length strings and sort remaining by length then alphabetically."""
        assert sorted_list_sum(["aa", "a", "aaa"]) == ["aa"]

    def test_multiple_even_strings(self):
        """Multiple even-length strings should be kept and sorted."""
        assert sorted_list_sum(["ab", "a", "aaa", "cd"]) == ["ab", "cd"]

    def test_empty_list(self):
        """An empty list should return an empty list."""
        assert sorted_list_sum([]) == []

    def test_all_odd_lengths(self):
        """If all strings have odd lengths, result should be empty."""
        assert sorted_list_sum(["a", "abc", "hello"]) == []

    def test_all_even_lengths(self):
        """If all strings have even lengths, they should be sorted."""
        assert sorted_list_sum(["bb", "aa", "cc"]) == ["aa", "bb", "cc"]

    # --- Sorting by length ---

    def test_sort_by_length_ascending(self):
        """Strings should be sorted by length in ascending order."""
        assert sorted_list_sum(["aaaa", "bb", "cccc", "dd"]) == ["bb", "dd", "aaaa", "cccc"]

    def test_single_even_string(self):
        """A single even-length string should be returned as-is."""
        assert sorted_list_sum(["hello"]) == []  # "hello" has length 5 (odd)
        assert sorted_list_sum(["hi"]) == ["hi"]  # "hi" has length 2 (even)

    # --- Alphabetical sorting for same length ---

    def test_alphabetical_order_same_length(self):
        """Strings of the same length should be sorted alphabetically."""
        assert sorted_list_sum(["zz", "aa", "mm"]) == ["aa", "mm", "zz"]

    def test_mixed_length_and_alpha(self):
        """Mixed lengths: sort by length first, then alphabetically within same length."""
        assert sorted_list_sum(["ccc", "bb", "aa", "dddd"]) == ["aa", "bb", "dddd"]

    def test_reverse_alpha_same_length(self):
        """Reverse alphabetical order should be corrected."""
        assert sorted_list_sum(["zebra", "apple"]) == []  # both length 5 (odd)
        assert sorted_list_sum(["ze", "ba", "ca"]) == ["ba", "ca", "ze"]

    # --- Duplicates ---

    def test_duplicate_strings(self):
        """Duplicates should be preserved in the output."""
        assert sorted_list_sum(["aa", "aa", "bb"]) == ["aa", "aa", "bb"]

    def test_all_duplicates(self):
        """All duplicate even-length strings."""
        assert sorted_list_sum(["ab", "ab", "ab"]) == ["ab", "ab", "ab"]

    def test_duplicate_with_different_lengths(self):
        """Duplicates mixed with different-length strings."""
        assert sorted_list_sum(["a", "bb", "bb", "ccc"]) == ["bb", "bb"]

    # --- Edge cases ---

    def test_empty_strings(self):
        """Empty string has length 0 (even), so it should be included."""
        assert sorted_list_sum(["", "a", ""]) == ["", ""]

    def test_only_empty_strings(self):
        """Only empty strings — all have even length 0."""
        assert sorted_list_sum(["", "", ""]) == ["", "", ""]

    def test_long_strings(self):
        """Longer strings should still work correctly."""
        assert sorted_list_sum(["abcdefgh", "ab", "abcdef"]) == [
            "ab",
            "abcdef",
            "abcdefgh",
        ]

    def test_case_sensitive_sorting(self):
        """Sorting should be case-sensitive (uppercase before lowercase in ASCII)."""
        result = sorted_list_sum(["Bb", "Aa", "Cc"])
        assert result == ["Aa", "Bb", "Cc"]

    def test_no_change_when_already_sorted(self):
        """When input is already filtered and sorted, output should match."""
        assert sorted_list_sum(["aa", "bb", "cc"]) == ["aa", "bb", "cc"]

    def test_alternating_odd_even(self):
        """Alternating odd and even length strings."""
        assert sorted_list_sum(["a", "bb", "ccc", "dddd", "eeeee"]) == [
            "bb",
            "dddd",
        ]

    def test_single_character(self):
        """Single character strings are always odd length."""
        assert sorted_list_sum(["x"]) == []

    def test_many_items(self):
        """Test with a larger list to ensure correctness."""
        lst = ["a", "bb", "ccc", "dddd", "eeee", "fffff", "gggggg"]
        # "a"(1,odd), "bb"(2,even), "ccc"(3,odd), "dddd"(4,even), "eeee"(4,even), "fffff"(5,odd), "gggggg"(6,even)
        expected = ["bb", "dddd", "eeee", "gggggg"]
        assert sorted_list_sum(lst) == expected
