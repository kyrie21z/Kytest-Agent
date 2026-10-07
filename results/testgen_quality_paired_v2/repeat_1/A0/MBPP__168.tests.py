import pytest
from solution import frequency


class TestFrequency:
    """Tests for the frequency function."""

    # --- Basic positive cases ---

    def test_single_occurrence(self):
        assert frequency([1, 2, 3], 2) == 1

    def test_multiple_occurrences(self):
        assert frequency([1, 2, 2, 3, 2], 2) == 3

    def test_first_element(self):
        assert frequency([5, 1, 2, 3], 5) == 1

    def test_last_element(self):
        assert frequency([1, 2, 3, 4], 4) == 1

    def test_all_same_elements(self):
        assert frequency([7, 7, 7, 7], 7) == 4

    # --- Element not found ---

    def test_element_not_in_list(self):
        assert frequency([1, 2, 3], 5) == 0

    def test_zero_not_in_list(self):
        assert frequency([1, 2, 3], 0) == 0

    # --- Empty list ---

    def test_empty_list(self):
        assert frequency([], 5) == 0

    # --- Single element list ---

    def test_single_element_found(self):
        assert frequency([42], 42) == 1

    def test_single_element_not_found(self):
        assert frequency([42], 99) == 0

    # --- Negative numbers ---

    def test_negative_numbers(self):
        assert frequency([-1, -2, -3, -2], -2) == 2

    def test_negative_search_value(self):
        assert frequency([1, -1, 2, -1], -1) == 2

    # --- Zero as search value ---

    def test_zero_occurrences(self):
        assert frequency([0, 0, 1, 2], 0) == 2

    def test_zero_not_present(self):
        assert frequency([1, 2, 3], 0) == 0

    # --- Floating point numbers ---

    def test_float_occurrences(self):
        assert frequency([1.5, 2.5, 1.5, 3.5], 1.5) == 2

    def test_float_not_present(self):
        assert frequency([1.0, 2.0, 3.0], 4.0) == 0

    # --- Mixed types ---

    def test_mixed_integers(self):
        assert frequency([1, 1, 2, 2, 3, 3], 2) == 2

    # --- Large list ---

    def test_large_list(self):
        large = [1] * 1000 + [2] * 500
        assert frequency(large, 1) == 1000
        assert frequency(large, 2) == 500
        assert frequency(large, 3) == 0

    # --- String-like behavior with edge values ---

    def test_none_values(self):
        assert frequency([None, None, 1], None) == 2

    def test_duplicate_consecutive(self):
        assert frequency([1, 1, 1, 2, 2], 1) == 3
