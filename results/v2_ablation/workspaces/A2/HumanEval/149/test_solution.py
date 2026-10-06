import pytest
from solution import sorted_list_sum


class TestSortedListSumNormalCases:
    """Tests with typical, non-edge-case inputs."""

    def test_mixed_odd_even_lengths(self):
        """Mix of odd and even length strings — keep evens, sort them."""
        result = sorted_list_sum(["aa", "a", "aaa"])
        assert result == ["aa"]

    def test_multiple_evens_different_lengths(self):
        """Even-length strings of varying lengths — sorted by length."""
        result = sorted_list_sum(["ab", "a", "aaa", "cd"])
        assert result == ["ab", "cd"]

    def test_all_even_same_length_alpha_sorted(self):
        """All even-length strings of the same length — sorted alphabetically."""
        result = sorted_list_sum(["zz", "aa", "bb"])
        assert result == ["aa", "bb", "zz"]

    def test_all_even_different_lengths_then_alpha(self):
        """Even-length strings with mixed lengths; ties broken alphabetically."""
        result = sorted_list_sum(["abcd", "ab", "efgh", "cd"])
        assert result == ["ab", "cd", "abcd", "efgh"]

    def test_preserves_duplicates(self):
        """Duplicate strings are preserved in the output."""
        result = sorted_list_sum(["aa", "bb", "aa"])
        assert result == ["aa", "aa", "bb"]

    def test_no_odds_to_filter(self):
        """No odd-length strings to remove — just sorting."""
        result = sorted_list_sum(["ab", "cd", "efgh"])
        assert result == ["ab", "cd", "efgh"]

    def test_all_removed(self):
        """All strings have odd lengths — result is empty."""
        result = sorted_list_sum(["a", "b", "ccc"])
        assert result == []

    def test_longer_strings_first_filtered_out(self):
        """Longer odd-length strings are removed; shorter evens remain."""
        # "abcdef" has length 6 (even), "ghi" has length 3 (odd), "jk" has length 2 (even)
        result = sorted_list_sum(["abcdef", "ghi", "jk"])
        assert result == ["jk", "abcdef"]

    def test_empty_string_kept_with_other_evens(self):
        """Empty string (length 0, even) is kept alongside other even-length strings."""
        result = sorted_list_sum(["", "ab", "cd"])
        assert result == ["", "ab", "cd"]


class TestSortedListSumBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_empty_list(self):
        """Empty input list returns an empty list."""
        result = sorted_list_sum([])
        assert result == []

    def test_single_even_length_element(self):
        """Single even-length string — returned as-is."""
        result = sorted_list_sum(["ab"])
        assert result == ["ab"]

    def test_single_odd_length_element(self):
        """Single odd-length string — filtered out, returns empty."""
        result = sorted_list_sum(["a"])
        assert result == []

    def test_single_empty_string(self):
        """A single empty string (length 0, even) is kept."""
        result = sorted_list_sum([""])
        assert result == [""]

    def test_two_elements_both_even(self):
        """Two even-length strings — sorted correctly."""
        result = sorted_list_sum(["zz", "aa"])
        assert result == ["aa", "zz"]

    def test_two_elements_one_even_one_odd(self):
        """One even, one odd — only the even remains."""
        result = sorted_list_sum(["ab", "c"])
        assert result == ["ab"]

    def test_two_elements_both_odd(self):
        """Both odd — both removed."""
        result = sorted_list_sum(["a", "bbb"])
        assert result == []

    def test_many_duplicates_same_length(self):
        """Many duplicate strings of the same even length."""
        result = sorted_list_sum(["ab", "ab", "ab", "ab"])
        assert result == ["ab", "ab", "ab", "ab"]

    def test_alternating_odd_even(self):
        """Alternating odd and even lengths."""
        result = sorted_list_sum(["a", "bb", "ccc", "dddd"])
        assert result == ["bb", "dddd"]

    def test_even_length_6_vs_even_length_2(self):
        """Large difference in even lengths — longer ones come after shorter."""
        result = sorted_list_sum(["abcdef", "ab"])
        assert result == ["ab", "abcdef"]


class TestSortedListSumEdgeCases:
    """Tests for unusual but valid inputs."""

    def test_only_empty_strings(self):
        """List of only empty strings — all kept, no reordering needed."""
        result = sorted_list_sum(["", "", ""])
        assert result == ["", "", ""]

    def test_empty_string_with_same_length_evens(self):
        """Empty string among other even-length strings of same length (0)."""
        result = sorted_list_sum(["", ""])
        assert result == ["", ""]

    def test_case_sensitive_sorting(self):
        """Sorting is case-sensitive — uppercase letters come before lowercase."""
        result = sorted_list_sum(["Ab", "aB", "AB", "ab"])
        # ASCII order: 'A' < 'B' < 'a' < 'b', so AB < Ab < aB < ab
        assert result == ["AB", "Ab", "aB", "ab"]

    def test_strings_with_spaces(self):
        """Strings containing spaces — space counts toward length."""
        result = sorted_list_sum(["a b", "ab", "c d e"])
        # "a b" has length 3 (odd), "ab" has length 2 (even), "c d e" has length 5 (odd)
        assert result == ["ab"]

    def test_strings_with_numbers(self):
        """Strings containing digits — treated as regular characters."""
        result = sorted_list_sum(["a1", "b23", "c4"])
        # "a1" len=2 (even), "b23" len=3 (odd), "c4" len=2 (even)
        assert result == ["a1", "c4"]

    def test_already_sorted_input(self):
        """Input already in correct order — output matches."""
        result = sorted_list_sum(["ab", "cd", "efgh"])
        assert result == ["ab", "cd", "efgh"]

    def test_reverse_sorted_input(self):
        """Input in reverse order — output is properly sorted."""
        result = sorted_list_sum(["efgh", "cd", "ab"])
        assert result == ["ab", "cd", "efgh"]


class TestSortedListSumInvalidInputs:
    """Tests for invalid or unexpected inputs that may raise exceptions."""

    def test_none_in_list_raises_error(self):
        """List containing None raises TypeError because len(None) fails."""
        with pytest.raises(TypeError):
            sorted_list_sum([None])

    def test_integer_in_list_raises_error(self):
        """List containing integers raises TypeError because len(int) fails."""
        with pytest.raises(TypeError):
            sorted_list_sum([123])

    def test_mixed_types_raises_error(self):
        """List with mixed types (str and int) raises TypeError."""
        with pytest.raises(TypeError):
            sorted_list_sum(["ab", 123])

    def test_string_input_returns_empty(self):
        """Passing a string iterates over characters (all length 1, odd), returning []."""
        result = sorted_list_sum("not a list")
        assert result == []

    def test_tuple_input_works_fine(self):
        """Tuples are iterable like lists — processed normally."""
        result = sorted_list_sum(("ab", "c", "de"))
        assert result == ["ab", "de"]
