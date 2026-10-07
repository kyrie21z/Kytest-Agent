import pytest
from solution import sorted_list_sum


class TestNormalCases:
    """Tests with typical, non-edge-case inputs."""

    def test_basic_filter_and_sort(self):
        """Filter odd-length strings and sort remaining by length then alphabetically."""
        result = sorted_list_sum(["aa", "a", "aaa"])
        assert result == ["aa"]

    def test_multiple_even_strings_same_length(self):
        """Multiple even-length strings of the same length should be sorted alphabetically."""
        result = sorted_list_sum(["ab", "a", "aaa", "cd"])
        assert result == ["ab", "cd"]

    def test_mixed_lengths_sorted_by_length(self):
        """Strings of different even lengths should be sorted by length ascending."""
        result = sorted_list_sum(["aaaa", "bb", "cc", "dddddd"])
        assert result == ["bb", "cc", "aaaa", "dddddd"]

    def test_all_even_length_strings(self):
        """When all strings have even length, return them sorted."""
        result = sorted_list_sum(["bb", "aa", "cc"])
        assert result == ["aa", "bb", "cc"]

    def test_all_odd_length_strings(self):
        """When all strings have odd length, return empty list."""
        result = sorted_list_sum(["a", "bbb", "ccccccccc"])
        assert result == []

    def test_with_duplicates(self):
        """Duplicates of even-length strings should be preserved."""
        result = sorted_list_sum(["aa", "bb", "aa", "cc"])
        assert result == ["aa", "aa", "bb", "cc"]

    def test_duplicate_after_filtering(self):
        """Duplicate strings that survive filtering should appear multiple times."""
        result = sorted_list_sum(["aaaa", "bb", "aaaa", "cc", "bb"])
        assert result == ["bb", "bb", "cc", "aaaa", "aaaa"]

    def test_complex_mixed_input(self):
        """A more complex mix of odd/even lengths and varying alphabetic order."""
        result = sorted_list_sum(["hello", "world", "hi", "python", "code", "js", "rust"])
        # Filter: remove "hello"(5), "world"(5), "hi"(2->keep), "python"(6), "code"(4), "js"(2->keep), "rust"(4)
        # Keep: "hi"(2), "python"(6), "code"(4), "js"(2), "rust"(4)
        # Sort by length: "hi"(2), "js"(2), "code"(4), "rust"(4), "python"(6)
        assert result == ["hi", "js", "code", "rust", "python"]


class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_empty_list(self):
        """Empty list should return empty list."""
        result = sorted_list_sum([])
        assert result == []

    def test_single_string_even_length(self):
        """Single even-length string should return a list with that string."""
        result = sorted_list_sum(["ab"])
        assert result == ["ab"]

    def test_single_string_odd_length(self):
        """Single odd-length string should return empty list."""
        result = sorted_list_sum(["abc"])
        assert result == []

    def test_empty_string(self):
        """Empty string has length 0 (even), so it should be kept."""
        result = sorted_list_sum(["", "a", ""])
        assert result == ["", ""]

    def test_empty_string_alone(self):
        """Only an empty string in the list."""
        result = sorted_list_sum([""])
        assert result == [""]

    def test_longest_strings(self):
        """Very long strings should be handled correctly."""
        long_str = "a" * 100  # length 100, even
        result = sorted_list_sum([long_str, "ab", "c"])
        assert result == ["ab", long_str]

    def test_many_duplicates(self):
        """List with many identical even-length strings."""
        result = sorted_list_sum(["ab"] * 10)
        assert result == ["ab"] * 10

    def test_alternating_odd_even(self):
        """Alternating odd and even length strings."""
        result = sorted_list_sum(["a", "bb", "ccc", "dddd", "eeeeee"])
        assert result == ["bb", "dddd", "eeeeee"]


class TestSortingBehavior:
    """Tests specifically targeting the sorting logic."""

    def test_alpha_sort_same_length(self):
        """Same-length strings must be sorted alphabetically."""
        result = sorted_list_sum(["zz", "aa", "mm", "bb"])
        assert result == ["aa", "bb", "mm", "zz"]

    def test_length_then_alpha(self):
        """Primary sort by length, secondary by alphabetical."""
        result = sorted_list_sum(["bbbb", "aa", "cc", "aaaa"])
        # All have even length. aa(2), cc(2), aaaa(4), bbbb(4)
        # Sorted: aa, cc, aaaa, bbbb
        assert result == ["aa", "cc", "aaaa", "bbbb"]

    def test_case_sensitive_sort(self):
        """Sort should be case-sensitive (uppercase before lowercase in ASCII)."""
        result = sorted_list_sum(["BB", "aa", "CC", "bb"])
        assert result == ["BB", "CC", "aa", "bb"]

    def test_three_way_same_length(self):
        """Three strings of the same length sorted alphabetically."""
        # All have length 3 (odd), so all are filtered out
        result = sorted_list_sum(["ccc", "aaa", "bbb"])
        assert result == []

    def test_three_groups_different_lengths(self):
        """Multiple groups of same-length strings, each group sorted alphabetically."""
        result = sorted_list_sum(["zz", "aa", "yyyyyy", "xxxxxx", "b", "m", "nnnnnnnn"])
        # Even lengths: "zz"(2), "aa"(2), "yyyyyy"(6), "xxxxxx"(6), "nnnnnnnn"(8)
        # Odd lengths filtered: "b"(1), "m"(1)
        # Result: aa, zz, xxxxxx, yyyyyy, nnnnnnnn
        assert result == ["aa", "zz", "xxxxxx", "yyyyyy", "nnnnnnnn"]


class TestEdgeCaseInputs:
    """Tests with unusual but valid inputs."""

    def test_strings_with_spaces(self):
        """Strings containing spaces should be treated normally."""
        result = sorted_list_sum(["ab cd", "efg", "gh ij"])
        # "ab cd" has length 5 (odd) -> filtered
        # "efg" has length 3 (odd) -> filtered
        # "gh ij" has length 5 (odd) -> filtered
        assert result == []

    def test_strings_with_spaces_even(self):
        """Even-length strings with spaces should be kept."""
        result = sorted_list_sum(["ab cd", "ef gh", "xyz"])
        # "ab cd" length 5 (odd) -> filtered
        # "ef gh" length 5 (odd) -> filtered
        # "xyz" length 3 (odd) -> filtered
        assert result == []

    def test_strings_with_spaces_even_kept(self):
        """Even-length strings with spaces should be kept."""
        result = sorted_list_sum(["ab cde", "f ghij", "xyz"])
        # "ab cde" length 6 (even) -> kept
        # "f ghij" length 6 (even) -> kept
        # "xyz" length 3 (odd) -> filtered
        assert result == ["ab cde", "f ghij"]

    def test_numeric_strings(self):
        """Strings that look like numbers should be treated as strings."""
        result = sorted_list_sum(["1234", "56", "789"])
        assert result == ["56", "1234"]

    def test_special_characters(self):
        """Strings with special characters should be handled."""
        # "!!" length 2 (even), "@@" length 2 (even), "#" length 1 (odd), "$$" length 2 (even)
        # ASCII: '!' < '$' < '@', so order is "!!", "$$", "@@"
        result = sorted_list_sum(["!!", "@@", "#", "$$"])
        assert result == ["!!", "$$", "@@"]

    def test_unicode_strings(self):
        """Unicode strings should be handled correctly."""
        result = sorted_list_sum(["café", "a", "über", "b"])
        # "café" length 4 (even) -> kept
        # "a" length 1 (odd) -> filtered
        # "über" length 4 (even) -> kept
        # "b" length 1 (odd) -> filtered
        assert result == ["café", "über"]

    def test_already_sorted_input(self):
        """Input already in correct order should return same result."""
        result = sorted_list_sum(["aa", "bb", "cccc"])
        assert result == ["aa", "bb", "cccc"]

    def test_reverse_sorted_input(self):
        """Input in reverse order should be properly sorted."""
        result = sorted_list_sum(["zzzz", "bb", "aa"])
        assert result == ["aa", "bb", "zzzz"]


class TestTypeAssumptions:
    """Tests verifying behavior under assumed constraints."""

    def test_list_of_strings_only(self):
        """Function assumes list of strings; verify basic string behavior."""
        result = sorted_list_sum(["x" * i for i in range(1, 11)])
        # Keeps even-length strings: x*2, x*4, x*6, x*8, x*10
        expected = ["xx", "xxxx", "xxxxxx", "xxxxxxxx", "xxxxxxxxxx"]
        assert result == expected

    def test_preserves_order_for_equal_keys(self):
        """Stable sort: equal keys preserve original relative order."""
        result = sorted_list_sum(["bb", "aa", "bb", "aa"])
        assert result == ["aa", "aa", "bb", "bb"]
