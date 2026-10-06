import pytest
from solution import will_it_fly


class TestWillItFly:
    """Unit tests for the will_it_fly function."""

    # --- Examples from docstring ---

    def test_docstring_example_1(self):
        """Unbalanced, weight OK -> False"""
        assert will_it_fly([1, 2], 5) is False

    def test_docstring_example_2(self):
        """Balanced, weight exceeded -> False"""
        assert will_it_fly([3, 2, 3], 1) is False

    def test_docstring_example_3(self):
        """Balanced, weight OK -> True"""
        assert will_it_fly([3, 2, 3], 9) is True

    def test_docstring_example_4(self):
        """Single element, balanced, weight OK -> True"""
        assert will_it_fly([3], 5) is True

    # --- Balanced + weight condition combinations ---

    @pytest.mark.parametrize("q,w,expected", [
        ([1, 2, 1], 4, True),   # balanced, sum == w
        ([1, 2, 1], 5, True),   # balanced, sum < w
        ([1, 2, 1], 3, False),  # balanced, sum > w
        ([], 0, True),           # empty list is palindrome, sum=0 <= 0
        ([], 10, True),          # empty list, plenty of weight
    ])
    def test_balanced_weight_combinations(self, q, w, expected):
        assert will_it_fly(q, w) is expected

    # --- Palindrome checks ---

    @pytest.mark.parametrize("q,w,expected", [
        ([1], 1, True),          # single element is always palindrome
        ([1, 1], 2, True),       # two identical elements
        ([1, 2, 3, 2, 1], 10, True),  # longer palindrome
        ([1, 2, 3, 2, 1], 8, False),   # longer palindrome but weight too low
        ([1, 2, 3, 4], 10, False),     # not a palindrome
        ([1, 2, 3, 1], 10, False),     # not a palindrome
        ([1, 2, 3, 2, 2], 10, False),  # not a palindrome
    ])
    def test_palindrome_variations(self, q, w, expected):
        assert will_it_fly(q, w) is expected

    # --- Edge cases with weight ---

    @pytest.mark.parametrize("q,w,expected", [
        ([5], 5, True),            # sum exactly equals w
        ([5], 4, False),           # sum exceeds w by 1
        ([1, 1, 1, 1, 1], 5, True),  # five 1s, sum == w
        ([1, 1, 1, 1, 1], 4, False), # five 1s, sum > w
        ([100], 100, True),        # large value, exact match
        ([100], 99, False),        # large value, just over
    ])
    def test_weight_boundary_cases(self, q, w, expected):
        assert will_it_fly(q, w) is expected

    # --- Negative numbers ---

    @pytest.mark.parametrize("q,w,expected", [
        ([-1, 0, -1], 0, True),    # negative numbers, balanced, sum=0 <= 0
        ([-1, 0, -1], -2, True),   # negative numbers, balanced, sum == w
        ([-1, 0, -1], -3, False),  # negative numbers, balanced, sum > w
        ([-5, -5], -10, True),     # all negatives, balanced, sum == w
        ([-5, -5], -11, False),    # all negatives, balanced, sum > w
        ([-1, 2, -1], 0, True),    # mixed signs, balanced, sum=0 <= 0
    ])
    def test_negative_numbers(self, q, w, expected):
        assert will_it_fly(q, w) is expected

    # --- Zero weight ---

    @pytest.mark.parametrize("q,w,expected", [
        ([0], 0, True),            # zero element, zero weight
        ([0, 0], 0, True),         # zeros, balanced, sum=0
        ([1], 0, False),           # positive element, zero weight
        ([-1], 0, True),           # negative element, zero weight
    ])
    def test_zero_weight(self, q, w, expected):
        assert will_it_fly(q, w) is expected

    # --- Return type verification ---

    def test_returns_boolean(self):
        """Ensure the function always returns a boolean."""
        result = will_it_fly([1, 2, 1], 5)
        assert isinstance(result, bool)

    def test_returns_boolean_for_false_case(self):
        """Ensure the function returns False as a boolean, not some other falsy value."""
        result = will_it_fly([1, 2], 5)
        assert result is False
        assert type(result) is bool

    # --- Non-palindrome quick rejection ---

    @pytest.mark.parametrize("q,w", [
        ([1, 2, 3], 100),
        ([1, 2, 3, 4], 100),
        ([1, 2, 3, 2, 4], 100),
    ])
    def test_non_palindrome_rejected_even_with_high_weight(self, q, w):
        """Even with very high weight, non-palindromes should return False."""
        assert will_it_fly(q, w) is False
