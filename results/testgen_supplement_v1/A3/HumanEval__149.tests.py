"""Unit tests for sorted_list_sum in solution.py."""

import pytest
from solution import sorted_list_sum


class TestNormalCases:
    """Test typical inputs with normal data."""

    def test_basic_filter_and_sort(self):
        """Filter out odd-length strings, keep even-length ones."""
        assert sorted_list_sum(["aa", "a", "aaa"]) == ["aa"]

    def test_multiple_even_length_strings(self):
        """Multiple even-length strings after filtering."""
        assert sorted_list_sum(["ab", "a", "aaa", "cd"]) == ["ab", "cd"]

    def test_sort_by_length_then_alphabetical(self):
        """Sort first by length ascending, then alphabetically for ties."""
        assert sorted_list_sum(["abc", "defg", "hijklm", "no"]) == [
            "no", "defg", "hijklm"
        ]

    def test_alphabetical_order_for_same_length(self):
        """Strings of same length sorted alphabetically."""
        assert sorted_list_sum(["zz", "aa", "mm", "bb"]) == ["aa", "bb", "mm", "zz"]

    def test_mixed_lengths_with_duplicates(self):
        """Mix of lengths with duplicate strings."""
        assert sorted_list_sum(["ab", "cd", "ab", "efg", "gh"]) == [
            "ab", "ab", "cd", "gh"
        ]

    def test_all_even_length_strings(self):
        """All strings have even length — no filtering needed."""
        assert sorted_list_sum(["aabb", "ccdd", "eeff"]) == ["aabb", "ccdd", "eeff"]

    def test_single_odd_string_removed(self):
        """Single odd-length string is removed."""
        assert sorted_list_sum(["hello"]) == []

    def test_single_even_string_kept(self):
        """Single even-length string is kept."""
        assert sorted_list_sum(["hi"]) == ["hi"]

    def test_preserves_duplicates_after_sorting(self):
        """Duplicate strings are preserved in output."""
        assert sorted_list_sum(["aa", "aa", "bb"]) == ["aa", "aa", "bb"]

    def test_longer_strings_sorted_correctly(self):
        """Longer even-length strings appear after shorter ones."""
        assert sorted_list_sum(["abcd", "efgh", "ijklmnop", "mn"]) == [
            "mn", "abcd", "efgh", "ijklmnop"
        ]


class TestBoundaryCases:
    """Test edge cases at boundaries of valid input ranges."""

    def test_empty_string_in_list(self):
        """Empty string has length 0 (even), so it is kept."""
        assert sorted_list_sum(["", "a", "b"]) == [""]

    def test_only_empty_strings(self):
        """List containing only empty strings."""
        assert sorted_list_sum(["", "", ""]) == ["", "", ""]

    def test_empty_string_with_other_even_strings(self):
        """Empty string alongside other even-length strings."""
        assert sorted_list_sum(["", "ab", "cd"]) == ["", "ab", "cd"]

    def test_two_character_strings(self):
        """Two-character strings (minimum even length > 0)."""
        assert sorted_list_sum(["ab", "ba", "cd"]) == ["ab", "ba", "cd"]

    def test_large_even_length_string(self):
        """A very long even-length string."""
        long_str = "a" * 100
        assert sorted_list_sum([long_str, "ab"]) == ["ab", long_str]

    def test_many_duplicates(self):
        """Many duplicate strings."""
        result = sorted_list_sum(["ab"] * 10 + ["cd"] * 5)
        assert result == ["ab"] * 10 + ["cd"] * 5

    def test_reverse_alphabetical_input(self):
        """Input already in reverse alphabetical order, same length."""
        assert sorted_list_sum(["zzz", "yyy", "xxx"]) == []

    def test_alternating_odd_even_lengths(self):
        """Alternating odd and even length strings."""
        assert sorted_list_sum(["a", "bb", "ccc", "dddd", "eeeeee"]) == [
            "bb", "dddd", "eeeeee"
        ]


class TestEmptyAndNullInputs:
    """Test empty, null, or zero-size inputs."""

    def test_empty_list(self):
        """Empty list returns empty list."""
        assert sorted_list_sum([]) == []

    def test_list_with_only_odd_length_strings(self):
        """All strings have odd length — nothing remains."""
        assert sorted_list_sum(["a", "bbb", "ccccc"]) == []

    def test_list_with_only_empty_strings(self):
        """Only empty strings (length 0, even) — all kept."""
        assert sorted_list_sum([""]) == [""]

    def test_list_with_one_empty_string_and_odds(self):
        """One empty string mixed with odd-length strings."""
        assert sorted_list_sum(["", "a", "bb"]) == ["", "bb"]


class TestInvalidInputs:
    """Test inputs that violate documented constraints."""

    def test_none_input_raises_error(self):
        """Passing None should raise an error (not a valid list)."""
        with pytest.raises(TypeError):
            sorted_list_sum(None)

    def test_non_string_elements_integers(self):
        """Non-string elements like integers — len() fails on int."""
        with pytest.raises(TypeError):
            sorted_list_sum([1, 2, 3])

    def test_mixed_types(self):
        """Mixed types including non-iterables."""
        with pytest.raises(TypeError):
            sorted_list_sum(["ab", 42, "cd"])


class TestSortingCorrectness:
    """Verify sorting logic is correct in various scenarios."""

    def test_same_length_all_odd_filtered(self):
        """Same-length strings all have odd length — all filtered out."""
        assert sorted_list_sum(["zebra", "apple", "mango"]) == []

    def test_same_length_even_strings_sorted(self):
        """Same-length even strings sorted alphabetically; odd ones filtered."""
        # cat(3,odd)->removed, bat(3,odd)->removed, at(2,even)->kept
        assert sorted_list_sum(["cat", "bat", "at"]) == ["at"]

    def test_whitespace_strings_ascii_order(self):
        """Whitespace strings sorted by ASCII values: tab(9) < space(32)."""
        # "  " = two spaces, "\t\t" = two tabs, " \t" = space+tab
        # Tab (9) < Space (32), so "\t\t" < " \t" < "  "
        assert sorted_list_sum(["  ", "\t\t", " \t"]) == ["\t\t", " \t", "  "]

    def test_unicode_strings_filtered_and_sorted(self):
        """Unicode strings: café(4,even), naïve(5,odd), résumé(6,even)."""
        # After filter: ["café", "résumé"], sorted by length then alpha
        assert sorted_list_sum(["café", "naïve", "résumé"]) == ["café", "résumé"]

    def test_numbers_as_strings(self):
        """Numeric strings sorted alphabetically."""
        assert sorted_list_sum(["12", "34", "5678"]) == ["12", "34", "5678"]

    def test_special_characters(self):
        """Strings with special characters."""
        assert sorted_list_sum(["!@", "#$", "%^&*"]) == ["!@", "#$", "%^&*"]

    def test_complex_mixed_scenario(self):
        """Complex scenario with many strings of varying lengths."""
        input_list = [
            "a",       # odd -> removed
            "bb",      # even -> kept, len 2
            "ccc",     # odd -> removed
            "dddd",    # even -> kept, len 4
            "eeeee",   # odd -> removed
            "ffffff",  # even -> kept, len 6
            "ggggggg", # odd -> removed
            "hhhhhhhh",# even -> kept, len 8
            "i",       # odd -> removed
        ]
        expected = ["bb", "dddd", "ffffff", "hhhhhhhh"]
        assert sorted_list_sum(input_list) == expected

    def test_case_sensitive_sorting(self):
        """Uppercase vs lowercase — ASCII ordering applies."""
        # 'A' (65) < 'a' (97) in ASCII
        assert sorted_list_sum(["Ab", "aB", "AB"]) == ["AB", "Ab", "aB"]

    def test_different_lengths_same_prefix(self):
        """Different lengths but same prefix characters."""
        assert sorted_list_sum(["ab", "abcd", "abcde", "abcdef"]) == [
            "ab", "abcd", "abcdef"
        ]
