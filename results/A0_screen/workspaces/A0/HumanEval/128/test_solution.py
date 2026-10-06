import pytest
from solution import prod_signs


class TestProdSigns:
    """Tests for the prod_signs function."""

    # --- Empty input ---
    def test_empty_list(self):
        assert prod_signs([]) is None

    # --- Input containing zero ---
    def test_single_zero(self):
        assert prod_signs([0]) == 0

    def test_zero_in_middle(self):
        assert prod_signs([1, 0, 3]) == 0

    def test_zero_at_end(self):
        assert prod_signs([2, 5, 0]) == 0

    def test_multiple_zeros(self):
        assert prod_signs([0, 0, 0]) == 0

    # --- All positive numbers ---
    def test_all_positive(self):
        assert prod_signs([1, 2, 2, -4]) == -9  # sign product = -1, sum abs = 9

    def test_all_positive_no_negatives(self):
        assert prod_signs([1, 2, 3]) == 6  # sign product = 1, sum abs = 6

    def test_single_positive(self):
        assert prod_signs([5]) == 5

    def test_large_positive_values(self):
        assert prod_signs([10, 20, 30]) == 60

    # --- All negative numbers ---
    def test_even_count_of_negatives(self):
        assert prod_signs([-1, -2, -3, -4]) == 10  # sign product = 1, sum abs = 10

    def test_odd_count_of_negatives(self):
        assert prod_signs([-1, -2, -3]) == -6  # sign product = -1, sum abs = 6

    def test_single_negative(self):
        assert prod_signs([-7]) == -7

    def test_two_negatives(self):
        assert prod_signs([-3, -5]) == 8

    # --- Mixed positive and negative ---
    def test_mixed_with_example(self):
        assert prod_signs([1, 2, 2, -4]) == -9

    def test_mixed_positive_and_negative(self):
        assert prod_signs([3, -2, 4]) == -9  # sign product = -1, sum abs = 9

    def test_mixed_with_equal_abs(self):
        # [5, -5]: sign product = -1, sum abs = 10 => result = -10
        assert prod_signs([5, -5]) == -10

    def test_more_complex_mixed(self):
        assert prod_signs([1, -1, 2, -2, 3]) == 9  # sign product = 1, sum abs = 9

    # --- Edge cases with single elements ---
    def test_single_element_positive(self):
        assert prod_signs([42]) == 42

    def test_single_element_negative(self):
        assert prod_signs([-42]) == -42

    # --- Larger arrays ---
    def test_larger_array_all_positive(self):
        arr = list(range(1, 11))
        assert prod_signs(arr) == 55

    def test_larger_array_all_negative(self):
        arr = [-i for i in range(1, 11)]
        assert prod_signs(arr) == 55  # 10 negatives => sign product = 1

    def test_larger_array_alternating_signs(self):
        # [1, -2, 3, -4, 5]: signs are +,-,+,-,+ => product = +1, sum abs = 15
        arr = [1, -2, 3, -4, 5]
        assert prod_signs(arr) == 15

    # --- Duplicate values ---
    def test_duplicate_values(self):
        assert prod_signs([3, 3, 3]) == 9

    def test_duplicate_negative_values(self):
        assert prod_signs([-3, -3, -3]) == -9

    # --- Zero combined with other tests ---
    def test_zero_with_negatives(self):
        assert prod_signs([-1, -2, 0]) == 0

    def test_zero_with_positives(self):
        assert prod_signs([1, 2, 3, 0]) == 0

    # --- Boundary: large magnitude values ---
    def test_large_magnitude_values(self):
        assert prod_signs([1000, -2000, 3000]) == -6000

    def test_very_large_value(self):
        assert prod_signs([10**9]) == 10**9

    def test_very_large_negative_value(self):
        assert prod_signs([-10**9]) == -(10**9)
