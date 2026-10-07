import pytest
from solution import sorted_list_sum


class TestSortedListSumNormalCases:
    """Test normal / typical inputs."""

    def test_simple_filter(self):
        # Only one even-length string survives; odd ones removed
        assert sorted_list_sum(["aa", "a", "aaa"]) == ["aa"]

    def test_multiple_even_strings(self):
        # Two even-length strings survive, sorted by length then alpha
        assert sorted_list_sum(["ab", "a", "aaa", "cd"]) == ["ab", "cd"]

    def test_with_duplicates(self):
        # Duplicates are preserved
        assert sorted_list_sum(["ab", "ab", "cd"]) == ["ab", "ab", "cd"]

    def test_already_sorted(self):
        # Input already in correct order
        assert sorted_list_sum(["ab", "cd", "efgh"]) == ["ab", "cd", "efgh"]

    def test_different_even_lengths(self):
        # Even-length strings of different lengths, sorted by length
        assert sorted_list_sum(["abcdef", "ab", "cd"]) == ["ab", "cd", "abcdef"]

    def test_same_length_alphabetical(self):
        # Same length → sorted alphabetically
        assert sorted_list_sum(["ba", "ab", "cd"]) == ["ab", "ba", "cd"]

    def test_mixed_lengths_and_alpha(self):
        # Combination of length-based and alphabetical sorting
        assert sorted_list_sum(["zz", "aa", "mm", "b", "ccc"]) == ["aa", "mm", "zz"]

    def test_longer_words_first_filtered(self):
        # Longer odd-length words are removed; shorter even ones kept
        assert sorted_list_sum(["a", "bb", "cccc", "d"]) == ["bb", "cccc"]


class TestSortedListSumBoundaryCases:
    """Test boundary conditions at edges of valid input ranges."""

    def test_single_even_string(self):
        # One even-length string
        assert sorted_list_sum(["ab"]) == ["ab"]

    def test_single_odd_string(self):
        # One odd-length string → empty result
        assert sorted_list_sum(["abc"]) == []

    def test_all_even_lengths(self):
        # Every element survives
        assert sorted_list_sum(["ab", "cd", "ef"]) == ["ab", "cd", "ef"]

    def test_all_odd_lengths(self):
        # Every element is filtered out (all have odd lengths)
        assert sorted_list_sum(["a", "abc", "cde"]) == []

    def test_two_elements_both_even(self):
        assert sorted_list_sum(["ab", "cd"]) == ["ab", "cd"]

    def test_two_elements_one_even_one_odd(self):
        assert sorted_list_sum(["ab", "c"]) == ["ab"]

    def test_two_elements_both_odd(self):
        assert sorted_list_sum(["a", "bcde"]) == ["bcde"]


class TestSortedListSumEmptyAndSpecialInputs:
    """Test empty, null-like, and zero-size inputs."""

    def test_empty_list(self):
        assert sorted_list_sum([]) == []

    def test_empty_string_in_list(self):
        # Empty string has length 0 (even), so it survives
        assert sorted_list_sum(["", "a", "b"]) == [""]

    def test_only_empty_strings(self):
        # All empty strings → all survive (length 0 is even)
        assert sorted_list_sum(["", "", ""]) == ["", "", ""]

    def test_empty_string_with_other_evens(self):
        # Empty string sorts first (length 0 < any positive length)
        assert sorted_list_sum(["", "ab", "cd"]) == ["", "ab", "cd"]

    def test_empty_string_among_same_length(self):
        # Only empty string present
        assert sorted_list_sum([""]) == [""]


class TestSortedListSumEdgeSorting:
    """Test edge cases around sorting behavior."""

    def test_reverse_order_input(self):
        # Input in reverse sorted order should be reordered correctly
        assert sorted_list_sum(["zz", "mm", "aa"]) == ["aa", "mm", "zz"]

    def test_length_then_alpha_tiebreak(self):
        # Length primary, alphabetical secondary
        assert sorted_list_sum(["ba", "ab", "cc", "dd"]) == ["ab", "ba", "cc", "dd"]

    def test_many_same_length(self):
        # Many strings of the same even length, sorted alphabetically
        result = sorted_list_sum(["dcba", "abcd", "badc", "cdba"])
        assert result == ["abcd", "badc", "cdba", "dcba"]

    def test_interleaved_lengths(self):
        # Alternating even/odd lengths
        assert sorted_list_sum(["a", "bb", "ccc", "dddd", "eeeee"]) == [
            "bb",
            "dddd",
        ]

    def test_duplicate_same_length_alpha(self):
        # Duplicates with same length stay in place after stable sort
        assert sorted_list_sum(["ba", "ba", "ab"]) == ["ab", "ba", "ba"]


class TestSortedListSumLargeInput:
    """Test with larger inputs to ensure correctness scales."""

    def test_many_strings(self):
        large_input = [f"{'a' * i}" for i in range(1, 21)]
        # Keep only even-length strings: lengths 2,4,6,...,20
        expected = sorted(
            [f"{'a' * i}" for i in range(2, 21, 2)],
            key=lambda s: (len(s), s),
        )
        assert sorted_list_sum(large_input) == expected

    def test_diverse_strings(self):
        diverse = ["a", "bb", "ccc", "dddd", "eeeee", "ffffff", "ggggggg", "hhhhhhhh"]
        expected = ["bb", "dddd", "ffffff", "hhhhhhhh"]
        assert sorted_list_sum(diverse) == expected
