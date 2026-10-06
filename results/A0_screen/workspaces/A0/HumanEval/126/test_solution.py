import pytest
from solution import is_sorted


class TestIsSorted:
    """Tests for the is_sorted function."""

    def test_single_element(self):
        assert is_sorted([5]) is True

    def test_empty_list(self):
        assert is_sorted([]) is True

    def test_already_sorted(self):
        assert is_sorted([1, 2, 3, 4, 5]) is True

    def test_not_sorted(self):
        assert is_sorted([1, 3, 2, 4, 5]) is False

    def test_fully_sorted_larger(self):
        assert is_sorted([1, 2, 3, 4, 5, 6]) is True
        assert is_sorted([1, 2, 3, 4, 5, 6, 7]) is True

    def test_unsorted_in_middle(self):
        assert is_sorted([1, 3, 2, 4, 5, 6, 7]) is False

    def test_duplicates_allowed_once(self):
        # [1, 2, 2, 3, 3, 4] - each number appears at most twice
        assert is_sorted([1, 2, 2, 3, 3, 4]) is True

    def test_duplicate_more_than_twice_returns_false(self):
        # [1, 2, 2, 2, 3, 4] - '2' appears three times
        assert is_sorted([1, 2, 2, 2, 3, 4]) is False

    def test_reverse_sorted(self):
        assert is_sorted([5, 4, 3, 2, 1]) is False

    def test_all_same_elements_one(self):
        assert is_sorted([3]) is True

    def test_all_same_elements_two(self):
        assert is_sorted([3, 3]) is True

    def test_all_same_elements_three(self):
        assert is_sorted([3, 3, 3]) is False

    def test_descending_with_duplicates(self):
        assert is_sorted([5, 5, 4, 4, 3, 3]) is False

    def test_mixed_sorted_and_unsorted(self):
        assert is_sorted([1, 2, 4, 3, 5]) is False

    def test_large_sorted_list(self):
        lst = list(range(100))
        assert is_sorted(lst) is True

    def test_large_unsorted_list(self):
        lst = list(range(100))
        lst[50], lst[51] = lst[51], lst[50]
        assert is_sorted(lst) is False

    def test_return_type_is_bool(self):
        result = is_sorted([1, 2, 3])
        assert isinstance(result, bool)

    def test_return_type_is_bool_false(self):
        result = is_sorted([3, 2, 1])
        assert isinstance(result, bool)
        assert result is False

    def test_return_type_is_bool_empty(self):
        assert isinstance(is_sorted([]), bool)
