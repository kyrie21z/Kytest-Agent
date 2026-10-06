import pytest
from solution import add_elements


class TestAddElementsBasic:
    """Test basic functionality from the docstring example."""

    def test_docstring_example(self):
        arr = [111, 21, 3, 4000, 5, 6, 7, 8, 9]
        k = 4
        assert add_elements(arr, k) == 24  # 21 + 3

    def test_single_element(self):
        arr = [42]
        k = 1
        assert add_elements(arr, k) == 42

    def test_all_two_digit_numbers(self):
        arr = [10, 20, 30, 40]
        k = 4
        assert add_elements(arr, k) == 100  # 10 + 20 + 30 + 40

    def test_mixed_digits(self):
        arr = [1, 10, 100, 1000]
        k = 4
        assert add_elements(arr, k) == 11  # 1 + 10


class TestAddElementsSingleDigit:
    """Test with single-digit numbers."""

    def test_all_single_digit_positive(self):
        arr = [1, 2, 3, 4, 5]
        k = 5
        assert add_elements(arr, k) == 15

    def test_single_zero(self):
        arr = [0]
        k = 1
        assert add_elements(arr, k) == 0

    def test_single_digit_with_larger_k(self):
        arr = [5, 100, 200]
        k = 3
        assert add_elements(arr, k) == 5  # only 5 qualifies


class TestAddElementsTwoDigit:
    """Test with two-digit numbers."""

    def test_smallest_two_digit(self):
        arr = [10]
        k = 1
        assert add_elements(arr, k) == 10

    def test_largest_two_digit(self):
        arr = [99]
        k = 1
        assert add_elements(arr, k) == 99

    def test_boundary_100_excluded(self):
        arr = [100]
        k = 1
        assert add_elements(arr, k) == 0  # 100 has 3 digits

    def test_negative_two_digit_included(self):
        arr = [-99]
        k = 1
        assert add_elements(arr, k) == -99  # -99 has 2 digits

    def test_negative_one_digit_included(self):
        arr = [-5]
        k = 1
        assert add_elements(arr, k) == -5  # -5 has 1 digit


class TestAddElementsNegativeNumbers:
    """Test with negative numbers."""

    def test_negative_three_digits_excluded(self):
        arr = [-100]
        k = 1
        assert add_elements(arr, k) == 0  # -100 has 3 digits

    def test_mixed_positive_negative(self):
        arr = [10, -20, 300, -40]
        k = 4
        assert add_elements(arr, k) == -50  # 10 + (-20) + (-40)

    def test_all_negative_two_digit(self):
        arr = [-10, -20, -30]
        k = 3
        assert add_elements(arr, k) == -60

    def test_negative_single_digit(self):
        arr = [-1, -2, -3]
        k = 3
        assert add_elements(arr, k) == -6


class TestAddElementsEdgeCases:
    """Test edge cases."""

    def test_k_equals_length(self):
        arr = [10, 20, 30]
        k = 3
        assert add_elements(arr, k) == 60

    def test_k_is_one(self):
        arr = [500, 42, 1000]
        k = 1
        assert add_elements(arr, k) == 0  # 500 has 3 digits

    def test_none_qualify(self):
        arr = [100, 200, 300]
        k = 3
        assert add_elements(arr, k) == 0

    def test_all_qualify(self):
        arr = [1, 2, 3]
        k = 3
        assert add_elements(arr, k) == 6

    def test_empty_result_from_filter(self):
        arr = [1000, 2000, 3000]
        k = 3
        assert add_elements(arr, k) == 0

    def test_large_array_minimal_k(self):
        arr = list(range(1, 101))
        k = 1
        assert add_elements(arr, k) == 1  # only first element (1) qualifies

    def test_large_array_full_k(self):
        arr = list(range(1, 101))
        k = 100
        # Sum of all 1-99 (single and double digit positive numbers)
        expected = sum(i for i in range(1, 100))
        assert add_elements(arr, k) == expected

    def test_duplicates(self):
        arr = [42, 42, 42]
        k = 3
        assert add_elements(arr, k) == 126  # 42 * 3

    def test_zeros(self):
        arr = [0, 0, 0]
        k = 3
        assert add_elements(arr, k) == 0

    def test_mixed_with_zeros(self):
        arr = [0, 5, 10, 100, -5]
        k = 5
        assert add_elements(arr, k) == 10  # 0 + 5 + 10 + (-5)


class TestAddElementsConstraints:
    """Test within stated constraints."""

    def test_minimum_array_length(self):
        arr = [42]
        k = 1
        assert add_elements(arr, k) == 42

    def test_maximum_array_length(self):
        arr = list(range(1, 101))
        k = 100
        expected = sum(i for i in range(1, 100))
        assert add_elements(arr, k) == expected

    def test_k_at_boundaries(self):
        arr = [10, 20, 30]
        assert add_elements(arr, 1) == 10
        assert add_elements(arr, 2) == 30
        assert add_elements(arr, 3) == 60
