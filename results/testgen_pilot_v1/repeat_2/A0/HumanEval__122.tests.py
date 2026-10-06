import pytest
from solution import add_elements


class TestAddElementsBasic:
    """Test basic functionality of add_elements."""

    def test_example_from_docstring(self):
        """Example from the docstring: arr = [111,21,3,4000,5,6,7,8,9], k = 4"""
        assert add_elements([111, 21, 3, 4000, 5, 6, 7, 8, 9], 4) == 24

    def test_all_single_digit_elements(self):
        """All elements are single-digit; all should be included."""
        assert add_elements([1, 2, 3, 4, 5], 5) == 15

    def test_no_elements_with_at_most_two_digits(self):
        """No qualifying elements; result should be 0."""
        assert add_elements([100, 2000, 30000], 3) == 0

    def test_mixed_digits(self):
        """Mix of 1, 2, and 3+ digit numbers."""
        # First 5: [1, 12, 123, 4, 56] -> qualifying: 1 + 12 + 4 + 56 = 73
        assert add_elements([1, 12, 123, 4, 56, 789], 5) == 73


class TestEdgeCases:
    """Test edge cases around boundaries."""

    def test_k_equals_1(self):
        """Only the first element is considered."""
        assert add_elements([42, 100, 200], 1) == 42

    def test_k_equals_len_arr(self):
        """k equals the full length of the array."""
        assert add_elements([10, 20, 30], 3) == 60

    def test_single_element_array(self):
        """Array with only one element."""
        assert add_elements([5], 1) == 5

    def test_single_element_not_qualifying(self):
        """Single element with more than 2 digits."""
        assert add_elements([1000], 1) == 0

    def test_boundary_two_digit_number(self):
        """Exactly two-digit number (99) should be included."""
        assert add_elements([99], 1) == 99

    def test_boundary_three_digit_number(self):
        """Exactly three-digit number (100) should NOT be included."""
        assert add_elements([100], 1) == 0

    def test_negative_one_digit(self):
        """Negative single-digit number (-5) has 1 digit, should be included."""
        assert add_elements([-5], 1) == -5

    def test_negative_two_digits(self):
        """Negative two-digit number (-99) has 2 digits, should be included."""
        assert add_elements([-99], 1) == -99

    def test_negative_three_digits(self):
        """Negative three-digit number (-100) has 3 digits, should NOT be included."""
        assert add_elements([-100], 1) == 0

    def test_zero(self):
        """Zero has 1 digit, should be included."""
        assert add_elements([0], 1) == 0

    def test_zero_in_mixed_list(self):
        """Zero among other numbers."""
        # First 3: [0, 100, 5] -> qualifying: 0 + 5 = 5
        assert add_elements([0, 100, 5], 3) == 5


class TestNegativeNumbers:
    """Test behavior with negative numbers specifically."""

    def test_all_negative_two_digits(self):
        """All negative numbers with exactly 2 digits."""
        # [-10, -20, -30] -> all qualify -> sum = -60
        assert add_elements([-10, -20, -30], 3) == -60

    def test_mixed_positive_and_negative(self):
        """Mix of positive and negative numbers with <= 2 digits."""
        # First 4: [10, -20, 300, -40] -> qualifying: 10 + (-20) + (-40) = -50
        assert add_elements([10, -20, 300, -40], 4) == -50

    def test_large_negative_excluded(self):
        """Large negative numbers (>2 digits) should be excluded."""
        # First 3: [-1000, -50, -2000] -> qualifying: -50
        assert add_elements([-1000, -50, -2000], 3) == -50

    def test_negative_boundary(self):
        """-99 (2 digits) included, -100 (3 digits) excluded."""
        assert add_elements([-99, -100], 2) == -99


class TestConstraints:
    """Test within stated constraints."""

    def test_max_length_array(self):
        """Array with maximum allowed length (100)."""
        arr = list(range(1, 101))  # [1, 2, ..., 100]
        # First 100 elements: single/double digits qualify, 100 does not
        # Numbers 1-99 all qualify -> sum = 1+2+...+99 = 4950
        assert add_elements(arr, 100) == 4950

    def test_min_constraints(self):
        """Minimum constraint values: len(arr)=1, k=1."""
        assert add_elements([1], 1) == 1

    def test_k_within_bounds(self):
        """k is always between 1 and len(arr) inclusive."""
        arr = [1, 2, 3, 4, 5]
        for k in range(1, len(arr) + 1):
            result = add_elements(arr, k)
            assert isinstance(result, int)


class TestReturnTypes:
    """Test that return types are correct."""

    def test_returns_integer(self):
        """Result should be an integer."""
        assert isinstance(add_elements([1, 2, 3], 3), int)

    def test_empty_sum_returns_zero(self):
        """When no elements qualify, returns 0 (integer)."""
        result = add_elements([1000, 2000], 2)
        assert result == 0
        assert isinstance(result, int)
