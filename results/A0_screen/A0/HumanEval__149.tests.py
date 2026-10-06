import pytest
from solution import sorted_list_sum


class TestSortedListSumBasic:
    """Tests for basic functionality of sorted_list_sum."""

    def test_example_from_docstring_1(self):
        assert sorted_list_sum(["aa", "a", "aaa"]) == ["aa"]

    def test_example_from_docstring_2(self):
        assert sorted_list_sum(["ab", "a", "aaa", "cd"]) == ["ab", "cd"]

    def test_single_even_length_string(self):
        # "hi" has length 2 (even) -> kept
        assert sorted_list_sum(["hi"]) == ["hi"]

    def test_single_odd_length_string(self):
        # "abc" has length 3 (odd) -> removed
        assert sorted_list_sum(["abc"]) == []

    def test_empty_list(self):
        assert sorted_list_sum([]) == []


class TestFilteringOddLengths:
    """Tests that strings with odd lengths are removed."""

    def test_all_odd_lengths(self):
        assert sorted_list_sum(["a", "bbb", "ccccc"]) == []

    def test_mixed_lengths(self):
        result = sorted_list_sum(["a", "bb", "ccc", "dddd", "eeeeee"])
        assert result == ["bb", "dddd", "eeeeee"]

    def test_no_odd_strings_kept(self):
        assert sorted_list_sum(["ab", "cd", "ef"]) == ["ab", "cd", "ef"]

    def test_only_one_even_length(self):
        assert sorted_list_sum(["a", "b", "c", "abcd"]) == ["abcd"]


class TestSortingByLength:
    """Tests that results are sorted by string length (ascending)."""

    def test_different_lengths_sorted(self):
        result = sorted_list_sum(["aaaa", "bb", "cccccc", "dd"])
        assert result == ["bb", "dd", "aaaa", "cccccc"]

    def test_already_sorted_by_length(self):
        result = sorted_list_sum(["a", "bb", "ccc", "dddd"])
        assert result == ["bb", "dddd"]

    def test_reverse_length_order(self):
        result = sorted_list_sum(["dddd", "ccc", "bb", "a"])
        assert result == ["bb", "dddd"]


class TestAlphabeticalSorting:
    """Tests that strings of the same length are sorted alphabetically."""

    def test_same_length_alphabetical(self):
        # All have length 4 (even)
        result = sorted_list_sum(["zebraa", "applee", "mangoo"])
        assert result == ["applee", "mangoo", "zebraa"]

    def test_mixed_length_and_alpha(self):
        result = sorted_list_sum(["zz", "aa", "mmm", "bb", "nnn"])
        assert result == ["aa", "bb", "zz"]

    def test_same_length_reverse_alpha(self):
        # All have length 6 (even)
        result = sorted_list_sum(["zebraa", "applee", "kiwiie"])
        assert result == ["applee", "kiwiie", "zebraa"]

    def test_same_length_with_duplicates(self):
        result = sorted_list_sum(["bb", "aa", "bb", "aa"])
        assert result == ["aa", "aa", "bb", "bb"]


class TestDuplicates:
    """Tests handling of duplicate strings."""

    def test_duplicate_even_strings(self):
        result = sorted_list_sum(["ab", "ab", "cd", "cd"])
        assert result == ["ab", "ab", "cd", "cd"]

    def test_duplicate_with_different_lengths(self):
        result = sorted_list_sum(["ab", "ab", "abcde", "ab"])
        assert result == ["ab", "ab", "ab"]

    def test_all_duplicates(self):
        assert sorted_list_sum(["xx", "xx", "xx"]) == ["xx", "xx", "xx"]


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_empty_strings(self):
        # Empty string has length 0, which is even
        result = sorted_list_sum(["", "a", "", "bb"])
        assert result == ["", "", "bb"]

    def test_single_character(self):
        assert sorted_list_sum(["a"]) == []

    def test_two_character_strings(self):
        result = sorted_list_sum(["ba", "ab", "cd"])
        assert result == ["ab", "ba", "cd"]

    def test_long_strings(self):
        long_str = "a" * 100
        result = sorted_list_sum([long_str, "ab", "a"])
        assert result == ["ab", long_str]

    def test_case_sensitive_sorting(self):
        # Uppercase letters come before lowercase in ASCII
        result = sorted_list_sum(["Apple!", "apple!", "Banana", "banana"])
        assert result == ["Apple!", "Banana", "apple!", "banana"]

    def test_special_characters(self):
        result = sorted_list_sum(["!@", "#$", "%^"])
        assert result == ["!@", "#$", "%^"]

    def test_whitespace_strings(self):
        # Use even-length whitespace strings
        result = sorted_list_sum(["  ", "    ", "a", "    "])
        assert result == ["  ", "    ", "    "]

    def test_numbers_as_strings(self):
        result = sorted_list_sum(["12", "123", "1234", "1"])
        assert result == ["12", "1234"]


class TestReturnTypes:
    """Tests that return types are correct."""

    def test_returns_list(self):
        result = sorted_list_sum(["ab", "cd"])
        assert isinstance(result, list)

    def test_returns_new_list(self):
        original = ["ab", "cd", "ef"]
        result = sorted_list_sum(original)
        assert result is not original

    def test_does_not_modify_original(self):
        original = ["ef", "ab", "cd"]
        sorted_list_sum(original)
        assert original == ["ef", "ab", "cd"]
