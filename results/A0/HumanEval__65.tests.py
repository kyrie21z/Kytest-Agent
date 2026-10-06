import pytest
from solution import circular_shift


class TestCircularShiftBasic:
    """Tests for basic circular shift behavior."""

    def test_shift_right_by_one(self):
        """Shift right by 1 moves last digit to front."""
        assert circular_shift(12, 1) == "21"

    def test_shift_right_by_two_equal_to_length(self):
        """Shift right by number of digits returns original."""
        assert circular_shift(12, 2) == "12"

    def test_shift_right_by_zero(self):
        """Shift by 0 returns the original string."""
        assert circular_shift(12, 0) == "12"

    def test_shift_single_digit(self):
        """Shifting a single-digit number returns itself."""
        assert circular_shift(5, 1) == "5"

    def test_shift_single_digit_nonzero(self):
        """Any shift on single digit returns itself (since shift >= len)."""
        assert circular_shift(7, 3) == "7"


class TestCircularShiftGreaterThanLength:
    """Tests when shift exceeds the number of digits - returns reversed."""

    def test_shift_greater_than_length_reverses(self):
        """If shift > number of digits, return reversed digits."""
        assert circular_shift(123, 4) == "321"

    def test_shift_exactly_one_more_than_length(self):
        assert circular_shift(123, 4) == "321"

    def test_shift_very_large(self):
        """Very large shift should still reverse."""
        assert circular_shift(1234, 100) == "4321"

    def test_shift_greater_than_length_for_two_digits(self):
        assert circular_shift(45, 3) == "54"

    def test_shift_double_length_reverses(self):
        """When shift > length, it reverses regardless of multiples."""
        assert circular_shift(123, 6) == "321"

    def test_shift_three_times_length_reverses(self):
        """Even 3x length reverses because shift > len."""
        assert circular_shift(123, 9) == "321"


class TestCircularShiftModuloBehavior:
    """Tests for shift values that are within length (modulo applied)."""

    def test_shift_equals_length(self):
        """Shift equal to length returns original."""
        assert circular_shift(123, 3) == "123"

    def test_shift_modulo_wraps_correctly(self):
        """When shift <= length, modulo is applied for right shift."""
        # shift=5 > len=4, so this triggers reversal
        assert circular_shift(1234, 5) == "4321"

    def test_shift_within_length_applies_modulo(self):
        """shift < length: normal circular right shift."""
        # shift=1, len=4: right shift by 1 -> last digit comes to front
        assert circular_shift(1234, 1) == "4123"

    def test_shift_half_length(self):
        """shift = half of length."""
        # shift=2, len=4: right shift by 2 -> "3412"
        assert circular_shift(1234, 2) == "3412"

    def test_shift_three_of_four(self):
        """shift=3, len=4: right shift by 3 -> '2341'"""
        assert circular_shift(1234, 3) == "2341"


class TestCircularShiftEdgeCases:
    """Edge case tests."""

    def test_zero_input(self):
        """Input of 0 should work correctly."""
        assert circular_shift(0, 0) == "0"
        assert circular_shift(0, 1) == "0"

    def test_negative_shift_not_applicable(self):
        """The function doesn't handle negative shifts; test with 0."""
        assert circular_shift(123, 0) == "123"

    def test_larger_number(self):
        """Test with a larger number."""
        assert circular_shift(12345, 2) == "45123"

    def test_larger_number_shift_equals_length(self):
        assert circular_shift(12345, 5) == "12345"

    def test_larger_number_shift_exceeds_length(self):
        assert circular_shift(12345, 6) == "54321"

    def test_three_digit_shift_one(self):
        assert circular_shift(123, 1) == "312"

    def test_three_digit_shift_two(self):
        assert circular_shift(123, 2) == "231"

    def test_four_digit_shift_three(self):
        assert circular_shift(1234, 3) == "2341"

    def test_four_digit_shift_five_exceeds(self):
        assert circular_shift(1234, 5) == "4321"


class TestCircularShiftReturnTypes:
    """Tests to ensure correct return type."""

    def test_returns_string(self):
        """The function should always return a string."""
        result = circular_shift(12, 1)
        assert isinstance(result, str)

    def test_returns_string_for_zero(self):
        result = circular_shift(0, 0)
        assert isinstance(result, str)

    def test_returns_string_for_large_shift(self):
        result = circular_shift(12345, 100)
        assert isinstance(result, str)


class TestCircularShiftDocstringExamples:
    """Verify the examples from the docstring pass."""

    def test_docstring_example_1(self):
        """>>> circular_shift(12, 1) -> '21'"""
        assert circular_shift(12, 1) == "21"

    def test_docstring_example_2(self):
        """>>> circular_shift(12, 2) -> '12'"""
        assert circular_shift(12, 2) == "12"
