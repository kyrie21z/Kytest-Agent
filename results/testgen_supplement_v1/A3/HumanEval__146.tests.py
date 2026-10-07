import pytest
from solution import specialFilter


# ──────────────────────────────────────────────
# Normal cases (typical inputs from docstring + extras)
# ──────────────────────────────────────────────

class TestNormalCases:
    """Tests using typical inputs, including documented examples."""

    def test_docstring_example_1(self):
        # [15, -73, 14, -15] => 1
        # 15: >10, first='1', last='5' → qualifies
        # -73: not >10 → no
        # 14: >10, first='1', last='4'(even) → no
        # -15: not >10 → no
        assert specialFilter([15, -73, 14, -15]) == 1

    def test_docstring_example_2(self):
        # [33, -2, -3, 45, 21, 109] => 2
        # 33: >10, '3','3' → qualifies
        # -2: not >10 → no
        # -3: not >10 → no
        # 45: >10, '4'(even) → no
        # 21: >10, '2'(even) → no
        # 109: >10, '1','9' → qualifies
        assert specialFilter([33, -2, -3, 45, 21, 109]) == 2

    def test_all_qualify(self):
        # Every number is >10 and has odd first & last digits
        assert specialFilter([11, 33, 55, 77, 99]) == 5

    def test_none_qualify(self):
        # All numbers are <= 10
        assert specialFilter([1, 2, 3, 4, 5]) == 0

    def test_mixed_first_digit_odd_last_even(self):
        # Numbers with odd first digit but even last digit
        # 12: '1' odd, '2' even → no
        # 14: '1' odd, '4' even → no
        # 16: '1' odd, '6' even → no
        assert specialFilter([12, 14, 16, 18]) == 0

    def test_mixed_first_digit_even_last_odd(self):
        # Numbers with even first digit but odd last digit
        # 21: '2' even → no
        # 31: '3' odd, '1' odd → YES
        # 41: '4' even → no
        assert specialFilter([21, 31, 41, 51]) == 2  # 31 and 51 qualify

    def test_three_digit_numbers(self):
        # 101: >10, '1','1' → YES
        # 103: >10, '1','3' → YES
        # 100: >10, '1','0'(even) → NO
        assert specialFilter([101, 103, 100]) == 2

    def test_large_number(self):
        # 99999999999999999999: >10, '9','9' → YES
        assert specialFilter([99999999999999999999]) == 1

    def test_single_qualifying_element(self):
        assert specialFilter([11]) == 1

    def test_single_non_qualifying_element(self):
        assert specialFilter([10]) == 0


# ──────────────────────────────────────────────
# Boundary cases (edges of valid input ranges)
# ──────────────────────────────────────────────

class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_exactly_10_not_greater(self):
        # 10 is NOT > 10, so it should not qualify
        assert specialFilter([10]) == 0

    def test_exactly_11_qualifies(self):
        # 11: >10, '1','1' → YES
        assert specialFilter([11]) == 1

    def test_boundary_between_qualify_and_not(self):
        # 10 does not qualify, 11 does
        assert specialFilter([10, 11]) == 1

    def test_negative_boundary(self):
        # -10: not >10 → no
        # -11: not >10 → no
        assert specialFilter([-10, -11]) == 0

    def test_zero(self):
        # 0: not >10 → no
        assert specialFilter([0]) == 0

    def test_one_digit_numbers(self):
        # All single-digit numbers are <= 10
        assert specialFilter([1, 3, 5, 7, 9]) == 0

    def test_two_digit_all_odd_digits(self):
        # All two-digit numbers with both digits odd
        # 11, 13, 15, 17, 19, 31, 33, 35, 37, 39, ...
        nums = [11, 13, 15, 17, 19, 31, 33, 35, 37, 39, 51, 53, 55, 57, 59,
                71, 73, 75, 77, 79, 91, 93, 95, 97, 99]
        assert specialFilter(nums) == 25

    def test_two_digit_with_even_first(self):
        # Even first digit: 2x, 4x, 6x, 8x — none qualify regardless of last
        assert specialFilter([21, 23, 45, 47, 61, 63, 81, 83]) == 0

    def test_two_digit_with_even_last(self):
        # Even last digit: x0, x2, x4, x6, x8 — none qualify regardless of first
        assert specialFilter([10, 12, 14, 16, 18, 30, 32, 34, 36, 38]) == 0

    def test_just_above_threshold(self):
        # 11 is the smallest integer > 10 with odd first and last digit
        assert specialFilter([11, 12, 13, 14, 15, 16, 17, 18, 19]) == 5  # 11,13,15,17,19


# ──────────────────────────────────────────────
# Empty, null, or zero-size inputs
# ──────────────────────────────────────────────

class TestEmptyAndZeroSizeInputs:
    """Tests with empty or zero-size inputs."""

    def test_empty_list(self):
        assert specialFilter([]) == 0

    def test_list_with_only_zeros(self):
        assert specialFilter([0, 0, 0]) == 0

    def test_list_with_only_negatives(self):
        # All negative numbers fail the >10 check
        assert specialFilter([-1, -2, -3, -10, -11]) == 0

    def test_list_with_only_tens(self):
        # 10 is not > 10
        assert specialFilter([10, 10, 10]) == 0


# ──────────────────────────────────────────────
# Invalid inputs (if constraints are implied)
# ──────────────────────────────────────────────

class TestInvalidInputs:
    """Tests with inputs outside expected types."""

    def test_none_input_raises_type_error(self):
        # Passing None causes iteration to fail
        with pytest.raises(TypeError):
            specialFilter(None)

    def test_string_input_raises_type_error(self):
        # Passing a string instead of a list
        with pytest.raises(TypeError):
            specialFilter("hello")

    def test_integer_input_raises_type_error(self):
        # Passing an int instead of a list
        with pytest.raises(TypeError):
            specialFilter(42)


# ──────────────────────────────────────────────
# Exception cases
# ──────────────────────────────────────────────

class TestExceptionCases:
    """Tests that exercise potential exception paths."""

    def test_empty_list_no_exception(self):
        # Empty list should return 0 without raising
        result = specialFilter([])
        assert isinstance(result, int)
        assert result == 0

    def test_single_element_no_exception(self):
        # Single element should work fine
        assert specialFilter([11]) == 1
        assert specialFilter([10]) == 0
        assert specialFilter([-5]) == 0

    def test_duplicate_values(self):
        # Duplicates should each be counted independently
        assert specialFilter([11, 11, 11]) == 3
        assert specialFilter([10, 10, 10]) == 0

    def test_unsorted_list(self):
        # Order should not matter
        assert specialFilter([109, 33, 21, 45, -3, -2]) == 2

    def test_float_inputs(self):
        # Floats: str(11.5) = "11.5", first='1', last='5' → qualifies
        assert specialFilter([11.5]) == 1
        # 10.5: >10, '1'✓, '5'✓ → qualifies
        assert specialFilter([10.5]) == 1
        # 10.0: >10? No (10.0 == 10, not > 10) → no
        assert specialFilter([10.0]) == 0
        # 12.0: >10, '1'✓, '0'✗ → no
        assert specialFilter([12.0]) == 0

    def test_very_large_list(self):
        # A large list with known composition
        # Generate all numbers from 1 to 200
        nums = list(range(1, 201))
        # Count manually: numbers > 10 with odd first and last digit
        count = 0
        for n in nums:
            if n > 10:
                s = str(n)
                if s[0] in ["1", "3", "5", "7", "9"] and s[-1] in ["1", "3", "5", "7", "9"]:
                    count += 1
        assert specialFilter(nums) == count
