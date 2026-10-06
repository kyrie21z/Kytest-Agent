import pytest
from solution import add_elements


class TestAddElementsBasic:
    """Test basic functionality of add_elements."""

    def test_example_from_docstring(self):
        """Test the example provided in the docstring."""
        arr = [111, 21, 3, 4000, 5, 6, 7, 8, 9]
        k = 4
        assert add_elements(arr, k) == 24  # 21 + 3

    def test_single_element_one_digit(self):
        """Single element with one digit."""
        assert add_elements([5], 1) == 5

    def test_single_element_two_digits(self):
        """Single element with two digits."""
        assert add_elements([42], 1) == 42

    def test_single_element_three_digits(self):
        """Single element with three digits is excluded."""
        assert add_elements([100], 1) == 0

    def test_all_elements_included(self):
        """All first-k elements have at most two digits."""
        arr = [1, 2, 3, 4, 5]
        assert add_elements(arr, 5) == 15

    def test_no_elements_included(self):
        """None of the first-k elements have at most two digits."""
        arr = [100, 200, 300]
        assert add_elements(arr, 3) == 0

    def test_mixed_positive_and_negative(self):
        """Mix of positive and negative numbers with varying digit counts."""
        arr = [100, -12, 3, -400, 50]
        assert add_elements(arr, 5) == -12 + 3 + 50  # 41


class TestAddElementsNegativeNumbers:
    """Test handling of negative numbers."""

    def test_negative_one_digit(self):
        """Negative number with one digit is included."""
        assert add_elements([-5], 1) == -5

    def test_negative_two_digits(self):
        """Negative number with two digits is included."""
        assert add_elements([-12], 1) == -12

    def test_negative_three_digits(self):
        """Negative number with three digits is excluded."""
        assert add_elements([-100], 1) == 0

    def test_negative_four_digits(self):
        """Negative number with four digits is excluded."""
        assert add_elements([-1000], 1) == 0

    def test_mixed_negatives_with_two_digits(self):
        """Multiple negative numbers with two digits."""
        arr = [-10, -20, -30]
        assert add_elements(arr, 3) == -60

    def test_mixed_negatives_excluding_some(self):
        """Some negatives included, some excluded based on digit count."""
        arr = [-100, -12, -3, -4000]
        assert add_elements(arr, 4) == -12 + -3  # -15


class TestAddElementsZeroHandling:
    """Test handling of zero."""

    def test_zero_is_included(self):
        """Zero has one digit and should be included."""
        assert add_elements([0], 1) == 0

    def test_zero_among_others(self):
        """Zero mixed with other numbers."""
        arr = [0, 1, 2, 100]
        assert add_elements(arr, 4) == 0 + 1 + 2  # 3


class TestAddElementsBoundaryCases:
    """Test boundary conditions."""

    def test_k_equals_array_length(self):
        """k equals the length of the array."""
        arr = [1, 2, 3]
        assert add_elements(arr, 3) == 6

    def test_k_is_one(self):
        """k is 1, only first element considered."""
        arr = [100, 21, 3]
        assert add_elements(arr, 1) == 0  # 100 has 3 digits

    def test_k_is_one_included(self):
        """k is 1 and first element qualifies."""
        arr = [42, 100, 200]
        assert add_elements(arr, 1) == 42

    def test_largest_valid_two_digit_number(self):
        """99 is the largest 2-digit number and should be included."""
        assert add_elements([99], 1) == 99

    def test_smallest_invalid_three_digit_number(self):
        """100 is the smallest 3-digit number and should be excluded."""
        assert add_elements([100], 1) == 0

    def test_smallest_negative_two_digit(self):
        """-99 is the smallest 2-digit negative and should be included."""
        assert add_elements([-99], 1) == -99

    def test_largest_negative_two_digit(self):
        """-10 is the largest 2-digit negative and should be included."""
        assert add_elements([-10], 1) == -10

    def test_boundary_between_two_and_three_digits(self):
        """Test transition between 2 and 3 digit numbers."""
        arr = [99, 100]
        assert add_elements(arr, 2) == 99  # only 99 qualifies

    def test_boundary_between_negative_two_and_three_digits(self):
        """Test transition between negative 2 and 3 digit numbers."""
        arr = [-99, -100]
        assert add_elements(arr, 2) == -99  # only -99 qualifies


class TestAddElementsLargerInputs:
    """Test with larger arrays and various combinations."""

    def test_all_two_digit_numbers(self):
        """Array of all two-digit numbers."""
        arr = list(range(10, 100))
        assert add_elements(arr, 10) == sum(range(10, 20))

    def test_alternating_qualifying_and_non_qualifying(self):
        """Alternating pattern of qualifying and non-qualifying elements."""
        arr = [1, 100, 2, 200, 3, 300]
        assert add_elements(arr, 6) == 1 + 2 + 3  # 6

    def test_only_first_k_considered(self):
        """Elements beyond k are not considered even if they qualify."""
        arr = [100, 100, 1, 2]
        assert add_elements(arr, 2) == 0  # first 2 are both 100

    def test_many_elements_few_qualify(self):
        """Large array where few elements qualify."""
        arr = [1000] * 50 + [5, 10]
        assert add_elements(arr, 52) == 5 + 10  # 15

    def test_all_elements_qualify_large_array(self):
        """All elements in first k qualify."""
        arr = [i % 100 for i in range(100)]
        assert add_elements(arr, 100) == sum(i % 100 for i in range(100))


class TestAddElementsEdgeValues:
    """Test with edge-case numeric values."""

    def test_min_value_for_two_digits(self):
        """Smallest 2-digit positive number."""
        assert add_elements([10], 1) == 10

    def test_max_value_for_two_digits(self):
        """Largest 2-digit positive number."""
        assert add_elements([99], 1) == 99

    def test_min_value_for_two_digits_negative(self):
        """Smallest 2-digit negative number."""
        assert add_elements([-99], 1) == -99

    def test_max_value_for_two_digits_negative(self):
        """Largest 2-digit negative number."""
        assert add_elements([-10], 1) == -10

    def test_exact_three_digits(self):
        """Exactly 3 digits should be excluded."""
        assert add_elements([100, 999], 2) == 0

    def test_exact_negative_three_digits(self):
        """Exactly -3 digits should be excluded."""
        assert add_elements([-100, -999], 2) == 0

    def test_ten(self):
        """10 is a 2-digit number."""
        assert add_elements([10], 1) == 10

    def test_negative_ten(self):
        """-10 is a 2-digit number."""
        assert add_elements([-10], 1) == -10
