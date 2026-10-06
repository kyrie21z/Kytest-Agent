import pytest
from solution import specialFilter


# ──────────────────────────────────────────────
# Normal / typical-input cases
# ──────────────────────────────────────────────

class TestNormalCases:
    """Tests with typical, representative inputs."""

    def test_example_1(self):
        # From docstring: [15, -73, 14, -15] => 1
        assert specialFilter([15, -73, 14, -15]) == 1

    def test_example_2(self):
        # From docstring: [33, -2, -3, 45, 21, 109] => 2
        assert specialFilter([33, -2, -3, 45, 21, 109]) == 2

    def test_all_match(self):
        # Every element satisfies all three conditions
        assert specialFilter([11, 33, 55, 77, 99]) == 5

    def test_mixed_odd_first_last(self):
        # Different odd first/last digits — all still qualify
        assert specialFilter([13, 35, 57, 79, 91]) == 5

    def test_some_match_some_not(self):
        # Only 11 and 99 qualify; others fail one condition
        assert specialFilter([11, 12, 21, 22, 99]) == 2

    def test_single_matching_element(self):
        assert specialFilter([33]) == 1

    def test_single_non_matching_element(self):
        assert specialFilter([44]) == 0

    def test_large_numbers(self):
        # Multi-digit numbers with odd first & last digits
        assert specialFilter([111, 333, 555, 777, 999]) == 5

    def test_huge_number(self):
        assert specialFilter([99999999999999999999]) == 1


# ──────────────────────────────────────────────
# Boundary cases at edges of valid input ranges
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at the boundaries of the "> 10" threshold and digit checks."""

    def test_exactly_10(self):
        # 10 is NOT > 10, so it does not qualify
        assert specialFilter([10]) == 0

    def test_exactly_11(self):
        # 11 > 10, first="1", last="1" — qualifies
        assert specialFilter([11]) == 1

    def test_exactly_12(self):
        # 12 > 10 but last digit "2" is even
        assert specialFilter([12]) == 0

    def test_exactly_13(self):
        # 13 > 10, first="1", last="3" — qualifies
        assert specialFilter([13]) == 1

    def test_negative_boundary(self):
        # -11 is NOT > 10
        assert specialFilter([-11]) == 0

    def test_zero(self):
        assert specialFilter([0]) == 0

    def test_one_digit_odd(self):
        # Single-digit odd numbers are not > 10
        assert specialFilter([1, 3, 5, 7, 9]) == 0

    def test_two_digit_even_first(self):
        # First digit even → no match
        assert specialFilter([21, 23, 25, 27, 29]) == 0

    def test_two_digit_even_last(self):
        # Last digit even → no match
        assert specialFilter([12, 32, 52, 72, 92]) == 0

    def test_three_digit_middle_even(self):
        # Middle digit can be anything; only first & last matter
        assert specialFilter([121, 323, 525]) == 3


# ──────────────────────────────────────────────
# Empty / zero-size inputs
# ──────────────────────────────────────────────

class TestEmptyInputs:
    """Tests with empty or degenerate collections."""

    def test_empty_list(self):
        assert specialFilter([]) == 0


# ──────────────────────────────────────────────
# Negative-number behaviour
# ──────────────────────────────────────────────

class TestNegativeNumbers:
    """Negative numbers always fail because str(num)[0] == '-'."""

    def test_all_negative(self):
        assert specialFilter([-11, -33, -55, -77, -99]) == 0

    def test_mixed_positive_negative(self):
        # Only positive ones can qualify
        assert specialFilter([11, -11, 13, -13, 15, -15]) == 3

    def test_negative_with_odd_digits(self):
        # Even though digits are odd, sign prevents match
        assert specialFilter([-13579]) == 0


# ──────────────────────────────────────────────
# Float inputs
# ──────────────────────────────────────────────

class TestFloatInputs:
    """Verify behaviour when floats are passed (they are numbers)."""

    def test_float_qualifies(self):
        # str(11.5) == "11.5"; first="1", last="5"
        assert specialFilter([11.5]) == 1

    def test_float_does_not_qualify(self):
        # str(12.5) == "12.5"; last="5" but first="1" ok, wait...
        # Actually first="1" ✓, last="5" ✓, 12.5 > 10 ✓ → qualifies!
        assert specialFilter([12.5]) == 1

    def test_float_small(self):
        # 5.5 is not > 10
        assert specialFilter([5.5]) == 0

    def test_float_negative(self):
        # Negative float: str(-11.5) starts with "-"
        assert specialFilter([-11.5]) == 0


# ──────────────────────────────────────────────
# Edge-case combinations
# ──────────────────────────────────────────────

class TestEdgeCombinations:
    """Tricky combinations that exercise multiple conditions simultaneously."""

    def test_duplicate_values(self):
        assert specialFilter([11, 11, 11]) == 3

    def test_all_same_non_matching(self):
        assert specialFilter([22, 22, 22]) == 0

    def test_alternating_match_no_match(self):
        assert specialFilter([11, 12, 13, 14, 15]) == 3  # 11, 13, 15

    def test_only_threshold_value(self):
        # 10 is the boundary; nothing above it yet
        assert specialFilter([10, 10, 10]) == 0

    def test_many_elements_all_fail(self):
        nums = list(range(1, 100))  # 1..99
        # Only numbers > 10 with odd first & last digits qualify
        # Those are: 11, 13, 15, 17, 19, 31, 33, 35, 37, 39,
        #            51, 53, 55, 57, 59, 71, 73, 75, 77, 79, 91, 93, 95, 97, 99
        expected = 25
        assert specialFilter(nums) == expected

    def test_numbers_with_same_first_and_last(self):
        # Palindromic-like single-digit repeats
        assert specialFilter([11, 33, 55, 77, 99]) == 5

    def test_four_digit_numbers(self):
        assert specialFilter([1111, 3333, 5555, 7777, 9999]) == 5

    def test_four_digit_partial_match(self):
        # 1231: first="1"✓, last="1"✓, >10✓ → match
        # 1232: last="2"✗ → no match
        assert specialFilter([1231, 1232, 1233]) == 2
