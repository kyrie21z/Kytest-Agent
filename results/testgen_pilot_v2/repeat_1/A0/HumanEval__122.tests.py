import pytest
from solution import add_elements


class TestAddElements:
    """Tests for the add_elements function."""

    # --- Basic functionality ---

    def test_example_from_docstring(self):
        """Test the example given in the docstring."""
        arr = [111, 21, 3, 4000, 5, 6, 7, 8, 9]
        k = 4
        assert add_elements(arr, k) == 24  # 21 + 3

    def test_single_digit_numbers_only(self):
        """All single-digit numbers within first k should be summed."""
        arr = [1, 2, 3, 4, 5]
        k = 3
        assert add_elements(arr, k) == 6  # 1 + 2 + 3

    def test_two_digit_numbers_only(self):
        """All two-digit numbers within first k should be summed."""
        arr = [10, 20, 30, 40, 50]
        k = 3
        assert add_elements(arr, k) == 60  # 10 + 20 + 30

    def test_mixed_digits_included(self):
        """Mix of 1-, 2-, and 3+-digit numbers; only <=2 digits counted."""
        arr = [5, 12, 100, 3, 4567]
        k = 5
        assert add_elements(arr, k) == 20  # 5 + 12 + 3

    # --- Edge cases on digit count ---

    def test_no_elements_with_few_digits(self):
        """When no element in first k has <=2 digits, return 0."""
        arr = [100, 200, 300, 400]
        k = 4
        assert add_elements(arr, k) == 0

    def test_all_elements_qualify(self):
        """Every element in first k has <=2 digits."""
        arr = [1, 10, 99, 5, 20]
        k = 5
        assert add_elements(arr, k) == 135  # 1 + 10 + 99 + 5 + 20

    def test_boundary_two_digits(self):
        """Exactly 2-digit numbers: 99 and -99 should be included."""
        arr = [99, -99, 100, -100]
        k = 4
        assert add_elements(arr, k) == 0  # 99 + (-99) = 0

    def test_three_digit_excluded(self):
        """3-digit numbers should not be included."""
        arr = [100, 999, -100, -999]
        k = 4
        assert add_elements(arr, k) == 0

    def test_zero_included(self):
        """Zero is a 1-digit number and should be included."""
        arr = [0, 100, 200]
        k = 3
        assert add_elements(arr, k) == 0  # just 0

    def test_negative_two_digit_included(self):
        """Negative numbers with 2 digits should be included."""
        arr = [-10, -50, -100]
        k = 3
        assert add_elements(arr, k) == -60  # -10 + -50

    def test_negative_one_digit_included(self):
        """Negative numbers with 1 digit should be included."""
        arr = [-5, -3, 100]
        k = 3
        assert add_elements(arr, k) == -8  # -5 + -3

    # --- Boundary values for k ---

    def test_k_equals_array_length(self):
        """k equals the full length of the array."""
        arr = [1, 22, 333, 4444]
        k = 4
        assert add_elements(arr, k) == 23  # 1 + 22

    def test_k_is_one(self):
        """Only the first element is considered."""
        arr = [42, 100, 200]
        k = 1
        assert add_elements(arr, k) == 42

    def test_k_is_one_no_qualify(self):
        """First element has >2 digits, k=1."""
        arr = [1000, 2, 3]
        k = 1
        assert add_elements(arr, k) == 0

    # --- Constraints boundary ---

    def test_min_array_length(self):
        """Array with minimum allowed length (1)."""
        arr = [42]
        k = 1
        assert add_elements(arr, k) == 42

    def test_max_array_length(self):
        """Array with maximum allowed length (100)."""
        arr = list(range(1, 101))  # [1, 2, ..., 100]
        k = 100
        # Elements with <=2 digits: 1..99 => sum = 99*100/2 = 4950
        assert add_elements(arr, k) == 4950

    def test_large_k_within_bounds(self):
        """Large k value near max constraint."""
        arr = [i for i in range(1, 101)]
        k = 99
        # Elements with <=2 digits from first 99: 1..99 => 4950
        assert add_elements(arr, k) == 4950

    # --- Additional numeric edge cases ---

    def test_all_zeros(self):
        """Array filled with zeros."""
        arr = [0, 0, 0, 0]
        k = 4
        assert add_elements(arr, k) == 0

    def test_positive_and_negative_mix(self):
        """Mix of positive and negative qualifying numbers."""
        arr = [10, -20, 30, -40, 500]
        k = 4
        assert add_elements(arr, k) == -20  # 10 + (-20) + 30 + (-40)

    def test_largest_two_digit_number(self):
        """99 is the largest 2-digit positive number."""
        arr = [99, 100]
        k = 2
        assert add_elements(arr, k) == 99

    def test_smallest_three_digit_number(self):
        """100 is the smallest 3-digit positive number — should be excluded."""
        arr = [100, 99]
        k = 2
        assert add_elements(arr, k) == 99

    def test_negative_boundary(self):
        """-99 is the smallest 2-digit negative number — should be included."""
        arr = [-99, -100]
        k = 2
        assert add_elements(arr, k) == -99

    def test_duplicate_values(self):
        """Array with duplicate values."""
        arr = [5, 5, 5, 5, 5]
        k = 3
        assert add_elements(arr, k) == 15  # 5 + 5 + 5

    def test_all_same_two_digit(self):
        """All same two-digit number."""
        arr = [77, 77, 77, 77]
        k = 4
        assert add_elements(arr, k) == 308  # 77 * 4
