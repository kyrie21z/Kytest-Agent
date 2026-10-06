import pytest
from solution import add_elements


class TestAddElements:
    """Tests for the add_elements function."""

    def test_example_from_docstring(self):
        """Test the example provided in the docstring."""
        arr = [111, 21, 3, 4000, 5, 6, 7, 8, 9]
        k = 4
        assert add_elements(arr, k) == 24  # 21 + 3

    def test_all_elements_have_two_digits_or_less(self):
        """When all first-k elements have at most 2 digits, sum them all."""
        arr = [10, 20, 30, 40, 50]
        k = 3
        assert add_elements(arr, k) == 60  # 10 + 20 + 30

    def test_no_elements_have_two_digits_or_less(self):
        """When no first-k elements have at most 2 digits, return 0."""
        arr = [100, 200, 300, 400, 500]
        k = 3
        assert add_elements(arr, k) == 0

    def test_single_digit_numbers(self):
        """Single digit numbers should be included."""
        arr = [1, 2, 3, 4, 5]
        k = 5
        assert add_elements(arr, k) == 15  # 1 + 2 + 3 + 4 + 5

    def test_negative_numbers_with_at_most_two_digits(self):
        """Negative numbers with at most 2 digits should be included."""
        arr = [-10, -20, 30, 400, 500]
        k = 3
        assert add_elements(arr, k) == 0  # -10 + (-20) + 30 = 0

    def test_negative_three_digit_numbers_excluded(self):
        """Negative numbers with more than 2 digits should be excluded."""
        arr = [-100, -200, 5, 6, 7]
        k = 5
        assert add_elements(arr, k) == 18  # 5 + 6 + 7

    def test_k_equals_one(self):
        """When k is 1, only consider the first element."""
        arr = [42, 100, 200]
        k = 1
        assert add_elements(arr, k) == 42

    def test_k_equals_array_length(self):
        """When k equals the array length, consider all elements."""
        arr = [1, 2, 3, 4, 5]
        k = 5
        assert add_elements(arr, k) == 15

    def test_mixed_positive_and_negative_two_digit_numbers(self):
        """Mix of positive and negative two-digit numbers."""
        arr = [-99, 99, -50, 50, 1000]
        k = 4
        assert add_elements(arr, k) == 0  # -99 + 99 + (-50) + 50 = 0

    def test_boundary_two_digit_number_99(self):
        """99 is a 2-digit number and should be included."""
        arr = [99, 100]
        k = 2
        assert add_elements(arr, k) == 99

    def test_boundary_negative_two_digit_number_minus_99(self):
        """-99 is a 2-digit number and should be included."""
        arr = [-99, -100]
        k = 2
        assert add_elements(arr, k) == -99

    def test_boundary_three_digit_number_100(self):
        """100 is a 3-digit number and should be excluded."""
        arr = [100, 99]
        k = 2
        assert add_elements(arr, k) == 99

    def test_boundary_negative_three_digit_number_minus_100(self):
        """-100 is a 3-digit number and should be excluded."""
        arr = [-100, -99]
        k = 2
        assert add_elements(arr, k) == -99

    def test_zero_is_included(self):
        """Zero has one digit and should be included."""
        arr = [0, 100, 200]
        k = 3
        assert add_elements(arr, k) == 0  # 0 is included but adds nothing

    def test_only_zeros(self):
        """Array of zeros."""
        arr = [0, 0, 0]
        k = 3
        assert add_elements(arr, k) == 0

    def test_large_k_with_few_valid_elements(self):
        """Large k but only few elements qualify."""
        arr = [1000, 2000, 3, 4, 5, 6000, 7000]
        k = 7
        assert add_elements(arr, k) == 12  # 3 + 4 + 5

    def test_consecutive_two_digit_numbers(self):
        """Consecutive two-digit numbers."""
        arr = list(range(10, 100))
        k = 5
        assert add_elements(arr, k) == 10 + 11 + 12 + 13 + 14  # 60

    def test_single_element_array(self):
        """Array with a single element."""
        arr = [42]
        k = 1
        assert add_elements(arr, k) == 42

    def test_single_element_array_excluded(self):
        """Array with a single element that has more than 2 digits."""
        arr = [1000]
        k = 1
        assert add_elements(arr, k) == 0

    def test_all_negative_two_digit_numbers(self):
        """All negative two-digit numbers."""
        arr = [-10, -20, -30, -40, -50]
        k = 5
        assert add_elements(arr, k) == -150  # -10 + -20 + -30 + -40 + -50

    def test_elements_after_k_are_ignored(self):
        """Elements beyond index k-1 should not affect the result."""
        arr = [10, 20, 30, 9999, 8888]
        k = 3
        assert add_elements(arr, k) == 60  # 10 + 20 + 30
