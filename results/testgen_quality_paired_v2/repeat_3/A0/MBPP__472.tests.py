import pytest
from solution import check_Consecutive


class TestCheckConsecutive:
    """Tests for the check_Consecutive function."""

    # --- Positive cases: lists that ARE consecutive ---

    def test_simple_consecutive(self):
        assert check_Consecutive([1, 2, 3, 4, 5]) is True

    def test_consecutive_unsorted(self):
        assert check_Consecutive([5, 3, 1, 2, 4]) is True

    def test_two_consecutive_elements(self):
        assert check_Consecutive([3, 4]) is True

    def test_single_element(self):
        assert check_Consecutive([7]) is True

    def test_negative_consecutive(self):
        assert check_Consecutive([-3, -2, -1, 0, 1]) is True

    def test_mixed_positive_negative_consecutive(self):
        assert check_Consecutive([-2, -1, 0, 1, 2]) is True

    def test_large_consecutive_range(self):
        assert check_Consecutive(list(range(-100, 101))) is True

    def test_consecutive_with_zero(self):
        assert check_Consecutive([0, 1, 2, 3]) is True

    def test_consecutive_descending_input(self):
        assert check_Consecutive([5, 4, 3, 2, 1]) is True

    # --- Negative cases: lists that are NOT consecutive ---

    def test_missing_middle_element(self):
        assert check_Consecutive([1, 2, 4, 5]) is False

    def test_two_non_consecutive_elements(self):
        assert check_Consecutive([3, 5]) is False

    def test_large_gap(self):
        assert check_Consecutive([1, 100]) is False

    def test_duplicates(self):
        assert check_Consecutive([1, 2, 2, 3]) is False

    def test_all_same_elements(self):
        assert check_Consecutive([5, 5, 5]) is False

    def test_extra_element_breaks_consecutive(self):
        assert check_Consecutive([1, 2, 3, 5, 6]) is False

    def test_non_adjacent_pair(self):
        assert check_Consecutive([1, 4, 5]) is False

    # --- Edge cases ---

    def test_empty_list_raises_error(self):
        with pytest.raises(ValueError):
            check_Consecutive([])

    def test_negative_numbers_only(self):
        assert check_Consecutive([-5, -4, -3, -2, -1]) is True

    def test_negative_numbers_not_consecutive(self):
        assert check_Consecutive([-5, -3, -1]) is False

    def test_three_elements_consecutive(self):
        assert check_Consecutive([10, 11, 12]) is True

    def test_three_elements_not_consecutive(self):
        assert check_Consecutive([10, 11, 13]) is False

    def test_consecutive_with_duplicates_and_missing(self):
        assert check_Consecutive([1, 1, 2, 3, 5]) is False

    def test_large_list_consecutive(self):
        assert check_Consecutive(list(range(1000, 2000))) is True

    def test_large_list_non_consecutive(self):
        lst = list(range(1000, 2000))
        lst.append(9999)
        assert check_Consecutive(lst) is False
