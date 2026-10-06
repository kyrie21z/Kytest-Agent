import pytest
from solution import pairs_sum_to_zero


class TestPairsSumToZero:
    """Tests for the pairs_sum_to_zero function."""

    # --- Cases from docstring examples ---

    def test_no_pair_from_docstring_1(self):
        assert pairs_sum_to_zero([1, 3, 5, 0]) is False

    def test_no_pair_from_docstring_2(self):
        assert pairs_sum_to_zero([1, 3, -2, 1]) is False

    def test_no_pair_from_docstring_3(self):
        assert pairs_sum_to_zero([1, 2, 3, 7]) is False

    def test_has_pair_from_docstring(self):
        assert pairs_sum_to_zero([2, 4, -5, 3, 5, 7]) is True

    def test_single_element_from_docstring(self):
        assert pairs_sum_to_zero([1]) is False

    # --- Edge cases ---

    def test_empty_list(self):
        assert pairs_sum_to_zero([]) is False

    def test_two_elements_sum_to_zero(self):
        assert pairs_sum_to_zero([3, -3]) is True

    def test_two_elements_do_not_sum_to_zero(self):
        assert pairs_sum_to_zero([3, 4]) is False

    def test_single_zero(self):
        assert pairs_sum_to_zero([0]) is False

    def test_two_zeros(self):
        assert pairs_sum_to_zero([0, 0]) is True

    def test_three_zeros(self):
        assert pairs_sum_to_zero([0, 0, 0]) is True

    # --- Positive-only and negative-only lists ---

    def test_all_positive_numbers(self):
        assert pairs_sum_to_zero([1, 2, 3, 4, 5]) is False

    def test_all_negative_numbers(self):
        assert pairs_sum_to_zero([-1, -2, -3, -4, -5]) is False

    # --- Pairs with zero ---

    def test_zero_and_nonzero(self):
        assert pairs_sum_to_zero([0, 5]) is False

    def test_zero_with_itself(self):
        assert pairs_sum_to_zero([0, 0]) is True

    # --- Larger lists ---

    def test_large_list_with_pair(self):
        assert pairs_sum_to_zero(list(range(1, 100)) + [-50]) is True

    def test_large_list_without_pair(self):
        assert pairs_sum_to_zero(list(range(1, 100))) is False

    # --- Duplicate values ---

    def test_duplicate_values_no_pair(self):
        assert pairs_sum_to_zero([1, 1, 1, 1]) is False

    def test_duplicate_values_with_pair(self):
        assert pairs_sum_to_zero([1, 1, -1, -1]) is True

    def test_mixed_duplicates(self):
        assert pairs_sum_to_zero([2, 2, -2, 3]) is True

    # --- Symmetric pairs ---

    def test_negative_first(self):
        assert pairs_sum_to_zero([-5, 2, 3, 5]) is True

    def test_adjacent_pair(self):
        assert pairs_sum_to_zero([1, 2, -2, 3]) is True

    def test_last_pair(self):
        assert pairs_sum_to_zero([1, 2, 3, -3]) is True

    # --- Boundary values ---

    def test_large_values(self):
        assert pairs_sum_to_zero([1000000, -1000000]) is True

    def test_mixed_large_small(self):
        assert pairs_sum_to_zero([1000000, 1, -1, -1000000]) is True

    # --- Return type checks ---

    def test_returns_boolean_true(self):
        result = pairs_sum_to_zero([1, -1])
        assert isinstance(result, bool)
        assert result is True

    def test_returns_boolean_false(self):
        result = pairs_sum_to_zero([1, 2])
        assert isinstance(result, bool)
        assert result is False
