import pytest
from solution import filter_oddnumbers


class TestFilterOddnumbers:
    """Tests for the filter_oddnumbers function."""

    def test_empty_list(self):
        assert filter_oddnumbers([]) == []

    def test_no_odd_numbers(self):
        assert filter_oddnumbers([2, 4, 6, 8]) == []

    def test_all_odd_numbers(self):
        assert filter_oddnumbers([1, 3, 5, 7]) == [1, 3, 5, 7]

    def test_mixed_numbers(self):
        assert filter_oddnumbers([1, 2, 3, 4, 5]) == [1, 3, 5]

    def test_single_odd_number(self):
        assert filter_oddnumbers([3]) == [3]

    def test_single_even_number(self):
        assert filter_oddnumbers([2]) == []

    def test_negative_numbers(self):
        assert filter_oddnumbers([-1, -2, -3, -4, -5]) == [-1, -3, -5]

    def test_negative_and_positive_mixed(self):
        assert filter_oddnumbers([-3, 2, -1, 0, 1, 4]) == [-3, -1, 1]

    def test_zero_included_as_even(self):
        assert filter_oddnumbers([0, 1, 2]) == [1]

    def test_duplicates_preserved(self):
        assert filter_oddnumbers([1, 1, 2, 3, 3]) == [1, 1, 3, 3]

    def test_large_list(self):
        nums = list(range(1, 101))
        expected = [x for x in nums if x % 2 != 0]
        assert filter_oddnumbers(nums) == expected

    def test_returns_new_list(self):
        original = [1, 2, 3, 4, 5]
        result = filter_oddnumbers(original)
        assert result == [1, 3, 5]
        # Ensure original list is unchanged
        assert original == [1, 2, 3, 4, 5]

    def test_returns_list_type(self):
        result = filter_oddnumbers([1, 2, 3])
        assert isinstance(result, list)
