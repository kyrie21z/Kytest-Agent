import pytest
from solution import validate


class TestValidateBasic:
    """Tests for basic valid inputs."""

    def test_single_digit_valid(self):
        """Single digit numbers are always valid (frequency 1 <= digit)."""
        assert validate(1) is True
        assert validate(2) is True
        assert validate(3) is True
        assert validate(4) is True
        assert validate(5) is True
        assert validate(6) is True
        assert validate(7) is True
        assert validate(8) is True
        assert validate(9) is True

    def test_all_different_digits(self):
        """Numbers with all distinct non-zero digits should be valid."""
        assert validate(123456789) is True
        assert validate(987654321) is True
        assert validate(12) is True
        assert validate(345) is True

    def test_digit_2_appears_twice(self):
        """Digit 2 appearing exactly twice is valid (2 <= 2)."""
        assert validate(22) is True
        assert validate(122) is True
        assert validate(221) is True
        assert validate(3224) is True

    def test_digit_3_appears_thrice(self):
        """Digit 3 appearing exactly 3 times is valid (3 <= 3)."""
        assert validate(333) is True
        assert validate(1333) is True
        assert validate(3334) is True

    def test_mixed_valid_digits(self):
        """Various valid combinations where no digit exceeds its limit."""
        assert validate(122333) is True   # 1x1, 2x2, 3x3 — all within limits
        assert validate(123456789) is True  # each digit once
        assert validate(55555) is True      # 5x5 — valid (5 <= 5)


class TestValidateInvalid:
    """Tests for inputs that should return False."""

    def test_digit_0_anywhere_invalid(self):
        """Digit 0 appearing anywhere makes count > 0, so invalid."""
        assert validate(10) is False
        assert validate(101) is False
        assert validate(100) is False
        assert validate(1000) is False
        assert validate(102030) is False

    def test_digit_1_appears_more_than_once(self):
        """Digit 1 appearing more than once is invalid."""
        assert validate(11) is False
        assert validate(111) is False
        assert validate(112) is False
        assert validate(211) is False
        assert validate(1111) is False
        assert validate(123123) is False  # 1 appears twice

    def test_digit_2_appears_more_than_twice(self):
        """Digit 2 appearing more than twice is invalid."""
        assert validate(222) is False
        assert validate(2222) is False
        assert validate(1222) is False
        assert validate(2221) is False

    def test_digit_3_appears_more_than_thrice(self):
        """Digit 3 appearing more than 3 times is invalid."""
        assert validate(3333) is False
        assert validate(33333) is False

    def test_multiple_violations(self):
        """Numbers with multiple digit frequency violations."""
        assert validate(11222) is False  # 1 appears twice, 2 appears thrice
        assert validate(110) is False    # 1 appears twice AND 0 appears
        assert validate(2223333) is False  # both exceed limits


class TestValidateEdgeCases:
    """Tests for edge cases."""

    def test_zero(self):
        """Zero: the while(temp) loop never runs, so function returns True.
        Note: this is a bug in the original implementation — 0 contains
        digit 0 with frequency 1 > 0, but the code skips the loop entirely."""
        assert validate(0) is True

    def test_large_number_with_valid_digits(self):
        """Large numbers with valid digit frequencies (each digit appears
        at most once)."""
        assert validate(123456789) is True
        assert validate(987654321) is True

    def test_largest_valid_single_digit_repetition(self):
        """Digit 9 can appear up to 9 times."""
        assert validate(999999999) is True  # 9 nines — valid
        assert validate(9999999999) is False  # 10 nines — invalid

    def test_boundary_for_each_digit(self):
        """Test exact boundary counts for each digit."""
        # Digit 1: max 1 occurrence
        assert validate(1) is True
        assert validate(11) is False

        # Digit 2: max 2 occurrences
        assert validate(22) is True
        assert validate(222) is False

        # Digit 3: max 3 occurrences
        assert validate(333) is True
        assert validate(3333) is False

        # Digit 4: max 4 occurrences
        assert validate(4444) is True
        assert validate(44444) is False

        # Digit 5: max 5 occurrences
        assert validate(55555) is True
        assert validate(555555) is False

        # Digit 6: max 6 occurrences
        assert validate(666666) is True
        assert validate(6666666) is False

        # Digit 7: max 7 occurrences
        assert validate(7777777) is True
        assert validate(77777777) is False

        # Digit 8: max 8 occurrences
        assert validate(88888888) is True
        assert validate(888888888) is False

        # Digit 9: max 9 occurrences
        assert validate(999999999) is True
        assert validate(9999999999) is False

    def test_no_zeros_valid(self):
        """Numbers without digit 0 and with valid frequencies."""
        assert validate(123456789) is True
        assert validate(1122334455667788) is True  # 1-8 each appear twice


class TestValidateNegativeNumbers:
    """Tests for negative number handling."""

    def test_negative_single_digit(self):
        """Negative single-digit numbers."""
        result = validate(-1)
        # Behavior depends on implementation; just record it
        assert isinstance(result, bool)

    def test_negative_with_zeros(self):
        """Negative numbers containing digit 0."""
        result = validate(-10)
        assert isinstance(result, bool)

    def test_negative_no_zeros(self):
        """Negative numbers without digit 0."""
        result = validate(-123)
        assert isinstance(result, bool)


class TestValidateTypeHandling:
    """Tests for type-related edge cases."""

    def test_string_input(self):
        """Passing a string should raise an error or handle gracefully."""
        with pytest.raises((TypeError, ValueError)):
            validate("123")

    def test_float_input(self):
        """Passing a float should raise an error or handle gracefully."""
        with pytest.raises((TypeError, ValueError)):
            validate(1.5)

    def test_none_input(self):
        """Passing None should raise an error."""
        with pytest.raises((TypeError, AttributeError)):
            validate(None)

    def test_list_input(self):
        """Passing a list should raise an error."""
        with pytest.raises((TypeError, AttributeError)):
            validate([1, 2, 3])
