"""Unit tests for specialFilter in solution.py."""

import pytest
from solution import specialFilter


# ── Normal cases ──────────────────────────────────────────────────────────────

class TestNormalCases:
    """Tests with typical inputs from the docstring and common scenarios."""

    def test_docstring_example_1(self):
        # [15 qualifies; -73 fails num>10; 14 last digit even; -15 fails num>10]
        assert specialFilter([15, -73, 14, -15]) == 1

    def test_docstring_example_2(self):
        # 33 qualifies; 45 first digit even; 21 first digit even; 109 qualifies
        assert specialFilter([33, -2, -3, 45, 21, 109]) == 2

    def test_all_qualify(self):
        # All numbers: >10, first odd, last odd
        assert specialFilter([11, 13, 31, 33, 55, 77, 99]) == 7

    def test_none_qualify(self):
        # No number satisfies all three conditions
        assert specialFilter([12, 34, 56, 78, 90]) == 0

    def test_mixed_positive_and_negative(self):
        # Only positive numbers >10 with odd first & last digits count
        assert specialFilter([11, -11, 33, -33, 55, -55]) == 3

    def test_single_element_qualifies(self):
        assert specialFilter([11]) == 1

    def test_single_element_does_not_qualify(self):
        assert specialFilter([5]) == 0

    def test_large_list(self):
        nums = list(range(1, 101))
        # Count manually: numbers >10 with odd first and last digits
        # 11,13,15,17,19, 31,33,35,37,39, 51,53,55,57,59, 71,73,75,77,79, 91,93,95,97,99
        assert specialFilter(nums) == 25


# ── Boundary cases ────────────────────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_exactly_10(self):
        # 10 is NOT > 10, so it should not count
        assert specialFilter([10]) == 0

    def test_just_above_10(self):
        # 11 is > 10, first='1' odd, last='1' odd → qualifies
        assert specialFilter([11]) == 1

    def test_two_digit_boundary_low(self):
        # 11 is the smallest qualifying number
        assert specialFilter([11]) == 1

    def test_two_digit_boundary_high(self):
        # 99: >10, first='9' odd, last='9' odd → qualifies
        assert specialFilter([99]) == 1

    def test_three_digit_qualifies(self):
        # 111: >10, first='1' odd, last='1' odd → qualifies
        assert specialFilter([111]) == 1

    def test_three_digit_first_even(self):
        # 211: first='2' even → does not qualify
        assert specialFilter([211]) == 0

    def test_three_digit_last_even(self):
        # 112: last='2' even → does not qualify
        assert specialFilter([112]) == 0

    def test_four_digit_qualifies(self):
        # 1001: >10, first='1' odd, last='1' odd → qualifies
        assert specialFilter([1001]) == 1

    def test_large_number(self):
        # 999999999: >10, first='9' odd, last='9' odd → qualifies
        assert specialFilter([999999999]) == 1

    def test_zero(self):
        # 0 is not > 10
        assert specialFilter([0]) == 0

    def test_one(self):
        # 1 is not > 10
        assert specialFilter([1]) == 0

    def test_ten(self):
        # 10 is not > 10
        assert specialFilter([10]) == 0

    def test_eleven(self):
        # 11 is > 10, first='1' odd, last='1' odd → qualifies
        assert specialFilter([11]) == 1


# ── Empty / zero-size inputs ─────────────────────────────────────────────────

class TestEmptyInputs:
    """Tests with empty lists and values that produce zero results."""

    def test_empty_list(self):
        assert specialFilter([]) == 0

    def test_list_of_zeros(self):
        assert specialFilter([0, 0, 0]) == 0

    def test_list_of_tens(self):
        # 10 is not > 10
        assert specialFilter([10, 10, 10]) == 0

    def test_list_of_negatives(self):
        # All negatives fail num > 10
        assert specialFilter([-1, -5, -10, -100]) == 0


# ── Invalid / unusual inputs ─────────────────────────────────────────────────

class TestUnusualInputs:
    """Tests with edge-case values that may behave unexpectedly."""

    def test_negative_numbers_with_odd_digits(self):
        # Negative numbers: str(-11) = "-11", first char is '-' not in odd list
        # Also -11 is not > 10
        assert specialFilter([-11, -13, -15, -17, -19]) == 0

    def test_mixed_sign_same_digits(self):
        # Positive 11 qualifies; negative -11 does not
        assert specialFilter([11, -11]) == 1

    def test_first_digit_even_last_digit_odd(self):
        # 21: first='2' even → no
        assert specialFilter([21]) == 0

    def test_first_digit_odd_last_digit_even(self):
        # 12: last='2' even → no
        assert specialFilter([12]) == 0

    def test_middle_digits_only_odd(self):
        # 101: first='1' odd, last='1' odd → qualifies despite middle being 0
        assert specialFilter([101]) == 1

    def test_all_same_digit(self):
        # 333: first='3' odd, last='3' odd → qualifies
        assert specialFilter([333]) == 1

    def test_duplicate_values(self):
        # Duplicates should each be counted independently
        assert specialFilter([11, 11, 11]) == 3

    def test_alternating_qualifying_and_not(self):
        # 11 qualifies, 12 doesn't, 13 qualifies, 14 doesn't
        assert specialFilter([11, 12, 13, 14]) == 2

    def test_numbers_with_zero_in_middle(self):
        # 101 qualifies (first='1', last='1'), 202 doesn't (first='2')
        assert specialFilter([101, 202, 303]) == 2

    def test_very_large_number(self):
        # 10000000000000000001: first='1' odd, last='1' odd → qualifies
        assert specialFilter([10000000000000000001]) == 1


# ── Exception cases ───────────────────────────────────────────────────────────

class TestExceptionCases:
    """Tests that the function handles unexpected input gracefully or raises."""

    def test_non_iterable_raises_type_error(self):
        # Passing a non-iterable should raise TypeError when iteration begins
        with pytest.raises(TypeError):
            specialFilter(42)

    def test_none_raises_type_error(self):
        # None is not iterable
        with pytest.raises(TypeError):
            specialFilter(None)

    def test_string_input_raises_type_error(self):
        # A string is iterable but yields characters (str type), which can't be
        # compared with > 10. Per the docstring, the function expects an array of
        # numbers, so passing a string is invalid input.
        with pytest.raises(TypeError):
            specialFilter("1135")
