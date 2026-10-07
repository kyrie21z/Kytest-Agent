import pytest

from solution import check_Consecutive


class TestCheckConsecutive:
    """Tests for the check_Consecutive function."""

    # --- Positive cases: lists with consecutive numbers ---

    def test_already_sorted_consecutive(self):
        assert check_Consecutive([1, 2, 3, 4, 5]) is True

    def test_unsorted_consecutive(self):
        assert check_Consecutive([5, 3, 1, 2, 4]) is True

    def test_reversed_consecutive(self):
        assert check_Consecutive([5, 4, 3, 2, 1]) is True

    def test_mixed_order_consecutive(self):
        assert check_Consecutive([3, 1, 5, 4, 2]) is True

    def test_negative_numbers(self):
        assert check_Consecutive([-1, 0, 1, 2]) is True

    def test_all_negative_consecutive(self):
        assert check_Consecutive([-5, -4, -3, -2, -1]) is True

    def test_crossing_zero_consecutive(self):
        assert check_Consecutive([-2, -1, 0, 1, 2]) is True

    def test_single_element(self):
        assert check_Consecutive([42]) is True

    def test_two_consecutive_elements(self):
        assert check_Consecutive([1, 2]) is True

    def test_three_consecutive_elements(self):
        assert check_Consecutive([10, 11, 12]) is True

    def test_larger_consecutive_set(self):
        assert check_Consecutive([100, 101, 102, 103, 104, 105]) is True

    # --- Negative cases: lists without consecutive numbers ---

    def test_gaps_everywhere(self):
        assert check_Consecutive([1, 3, 5, 7]) is False

    def test_missing_middle_element(self):
        assert check_Consecutive([1, 2, 4, 5]) is False

    def test_duplicate_elements(self):
        assert check_Consecutive([1, 2, 2, 3]) is False

    def test_two_non_consecutive_elements(self):
        assert check_Consecutive([1, 3]) is False

    def test_large_gap(self):
        assert check_Consecutive([1, 100]) is False

    def test_three_elements_with_gap(self):
        assert check_Consecutive([1, 3, 4]) is False

    def test_multiple_duplicates(self):
        assert check_Consecutive([1, 1, 2, 3]) is False

    def test_all_same_elements(self):
        assert check_Consecutive([5, 5, 5, 5]) is False

    def test_sparse_sequence(self):
        assert check_Consecutive([0, 10, 20, 30]) is False

    # --- Edge cases ---

    def test_empty_list_raises_value_error(self):
        with pytest.raises(ValueError):
            check_Consecutive([])
