import pytest
from solution import add_elements


class TestAddElements:
    """Tests for the add_elements function."""

    # --- Basic functionality ---

    def test_example_from_docstring(self):
        """Test the example given in the docstring."""
        assert add_elements([111, 21, 3, 4000, 5, 6, 7, 8, 9], 4) == 24

    def test_single_digit_elements(self):
        """Elements with 1 digit are included."""
        assert add_elements([1, 2, 3, 4], 4) == 10

    def test_two_digit_elements(self):
        """Elements with exactly 2 digits are included."""
        assert add_elements([10, 20, 30, 40], 4) == 100

    def test_three_plus_digit_elements_excluded(self):
        """Elements with 3+ digits are excluded."""
        assert add_elements([100, 200, 300, 400], 4) == 0

    def test_mixed_digits(self):
        """Mix of 1-digit, 2-digit, and 3+ digit elements."""
        assert add_elements([5, 12, 345, 6, 78, 9012], 6) == 5 + 12 + 6 + 78

    # --- Boundary values for digit count ---

    def test_boundary_99_included(self):
        """99 is the largest 2-digit number and should be included."""
        assert add_elements([99], 1) == 99

    def test_boundary_100_excluded(self):
        """100 is the smallest 3-digit number and should be excluded."""
        assert add_elements([100], 1) == 0

    def test_boundary_negative_99_included(self):
        """-99 has 2 digits and should be included."""
        assert add_elements([-99], 1) == -99

    def test_boundary_negative_100_excluded(self):
        """-100 has 3 digits and should be excluded."""
        assert add_elements([-100], 1) == 0

    # --- Zero handling ---

    def test_zero_included(self):
        """Zero has 1 digit and should be included."""
        assert add_elements([0], 1) == 0

    def test_zero_with_other_elements(self):
        """Zero alongside other elements."""
        assert add_elements([0, 5, 100], 3) == 5

    # --- Negative numbers ---

    def test_negative_one_digit(self):
        """-5 has 1 digit and should be included."""
        assert add_elements([-5], 1) == -5

    def test_negative_two_digits(self):
        """-12 has 2 digits and should be included."""
        assert add_elements([-12], 1) == -12

    def test_negative_three_digits_excluded(self):
        """-123 has 3 digits and should be excluded."""
        assert add_elements([-123], 1) == 0

    def test_mixed_positive_and_negative(self):
        """Mix of positive and negative elements with varying digits."""
        result = add_elements([-5, 12, -34, 567, -89], 5)
        assert result == -5 + 12 + (-34) + (-89)

    # --- Edge cases on k ---

    def test_k_equals_array_length(self):
        """k equals the full array length."""
        assert add_elements([1, 2, 3], 3) == 6

    def test_k_is_one(self):
        """k is 1, only the first element is considered."""
        assert add_elements([999, 12, 34], 1) == 0
        assert add_elements([12, 999, 34], 1) == 12

    def test_partial_selection(self):
        """Only some of the first k elements qualify."""
        assert add_elements([1, 2, 3, 4, 5], 3) == 6  # 1 + 2 + 3

    # --- No qualifying elements ---

    def test_no_qualifying_elements(self):
        """None of the first k elements have <= 2 digits."""
        assert add_elements([1000, 2000, 3000], 3) == 0

    # --- All qualifying elements ---

    def test_all_qualifying_elements(self):
        """All of the first k elements have <= 2 digits."""
        assert add_elements([1, 2, 3], 3) == 6

    # --- Large arrays within constraints ---

    def test_max_array_size(self):
        """Test with maximum allowed array size (100 elements)."""
        arr = list(range(1, 101))  # [1, 2, ..., 100]
        # First 100 elements: 1-9 (9 elements), 10-99 (90 elements), 100 (1 element)
        # Qualifying: 1-99 => sum = 99*100//2 = 4950
        assert add_elements(arr, 100) == 4950

    def test_largest_k(self):
        """k equals len(arr) with large array."""
        arr = [99] * 100
        assert add_elements(arr, 100) == 9900

    # --- Duplicate values ---

    def test_duplicate_values(self):
        """Array with duplicate values."""
        assert add_elements([10, 10, 10, 100], 4) == 30

    # --- Single qualifying element among many ---

    def test_only_one_qualifies(self):
        """Only one element among the first k has <= 2 digits."""
        assert add_elements([1000, 2000, 5, 4000], 4) == 5
