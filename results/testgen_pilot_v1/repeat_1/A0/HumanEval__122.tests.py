import pytest
from solution import add_elements


class TestAddElementsBasic:
    """Tests covering basic functionality as described in the docstring."""

    def test_example_from_docstring(self):
        """Example from the docstring: arr = [111,21,3,4000,5,6,7,8,9], k = 4"""
        assert add_elements([111, 21, 3, 4000, 5, 6, 7, 8, 9], 4) == 24

    def test_all_two_digit_numbers(self):
        """All first k elements have at most two digits."""
        assert add_elements([10, 20, 30], 3) == 60

    def test_no_qualifying_elements(self):
        """None of the first k elements have at most two digits."""
        assert add_elements([100, 200, 300], 3) == 0

    def test_single_element with two digits(self):
        """Single qualifying element."""
        assert add_elements([42], 1) == 42

    def test_single_element with three digits(self):
        """Single non-qualifying element."""
        assert add_elements([100], 1) == 0


class TestAddElementsBoundaryValues:
    """Tests for boundary values of digit counts."""

    def test_99_is_two_digits(self):
        """99 should be counted (exactly 2 digits)."""
        assert add_elements([99], 1) == 99

    def test_100_is_three_digits(self):
        """100 should NOT be counted (3 digits)."""
        assert add_elements([100], 1) == 0

    def test_9_is_one_digit(self):
        """9 should be counted (1 digit)."""
        assert add_elements([9], 1) == 9

    def test_zero_is_one_digit(self):
        """0 should be counted (1 digit)."""
        assert add_elements([0], 1) == 0

    def test_negative_two_digit(self):
        """-5 has 2 digits and should be counted."""
        assert add_elements([-5], 1) == -5

    def test_negative_two_digit_boundary(self):
        """-99 has 2 digits and should be counted."""
        assert add_elements([-99], 1) == -99

    def test_negative_three_digit(self):
        """-100 has 3 digits and should NOT be counted."""
        assert add_elements([-100], 1) == 0

    def test_mixed_positive_and_negative_two_digit(self):
        """Mix of positive and negative two-digit numbers."""
        assert add_elements([-10, 10, -99, 99], 4) == 0  # -10 + 10 + (-99) + 99 = 0


class TestAddElementsKValue:
    """Tests varying the value of k."""

    def test_k_equals_len_arr(self):
        """k equals the length of the array."""
        assert add_elements([1, 2, 3], 3) == 6

    def test_k_is_one(self):
        """k is 1, only check the first element."""
        assert add_elements([100, 20, 30], 1) == 0

    def test_k_larger_than_needed(self):
        """k covers all elements but only some qualify."""
        assert add_elements([1, 2, 3, 4, 5], 5) == 15

    def test_partial_selection(self):
        """Only a subset of first k elements qualify."""
        assert add_elements([1000, 10, 20, 3000], 4) == 10


class TestAddElementsEdgeCases:
    """Additional edge cases."""

    def test_empty_sum_result(self):
        """Result is 0 when no elements qualify."""
        assert add_elements([1000, 2000, 3000], 3) == 0

    def test_large_array(self):
        """Test with a larger array (up to constraint limit of 100)."""
        arr = list(range(1, 101))  # [1, 2, ..., 100]
        # First 100 elements: 1-99 are 1-2 digits, 100 is 3 digits
        # Sum of 1..99 = 99*100//2 = 4950
        assert add_elements(arr, 100) == 4950

    def test_all_same_value(self):
        """Array where all elements are the same."""
        assert add_elements([5, 5, 5, 5], 4) == 20

    def test_all_same_non_qualifying_value(self):
        """Array where all elements are the same but don't qualify."""
        assert add_elements([1000, 1000, 1000], 3) == 0

    def test_mixed_with_zeros(self):
        """Zeros mixed with other numbers."""
        assert add_elements([0, 100, 0, 50], 4) == 50  # 0 + 0 + 50 = 50

    def test_negative_k_not_allowed_by_constraint(self):
        """Constraint says k >= 1, so we trust valid input."""
        pass  # Constraints guarantee 1 <= k <= len(arr)

    def test_consecutive_two_digit_numbers(self):
        """Consecutive two-digit numbers summed."""
        assert add_elements(list(range(10, 20)), 10) == sum(range(10, 20))  # 145

    def test_skip_then_include(self):
        """First few don't qualify, then they do."""
        assert add_elements([999, 888, 12, 34], 4) == 46  # 12 + 34
