"""Unit tests for solution.change_base."""

import pytest
from solution import change_base


class TestChangeBaseDoctests:
    """Tests from the docstring examples."""

    def test_change_base_8_to_3(self):
        assert change_base(8, 3) == "22"

    def test_change_base_8_to_2(self):
        assert change_base(8, 2) == "1000"

    def test_change_base_7_to_2(self):
        assert change_base(7, 2) == "111"


class TestChangeBaseZero:
    """Test cases where x is zero."""

    @pytest.mark.parametrize("base", [2, 3, 4, 5, 6, 7, 8, 9])
    def test_zero_various_bases(self, base):
        assert change_base(0, base) == "0"


class TestChangeBasePositiveNumbers:
    """Test cases for positive integer conversions."""

    # Powers of 2
    def test_power_of_2_base_2(self):
        assert change_base(1, 2) == "1"
        assert change_base(2, 2) == "10"
        assert change_base(4, 2) == "100"
        assert change_base(8, 2) == "1000"
        assert change_base(16, 2) == "10000"
        assert change_base(32, 2) == "100000"
        assert change_base(64, 2) == "1000000"
        assert change_base(128, 2) == "10000000"
        assert change_base(256, 2) == "100000000"

    # Powers of 10 converted to other bases
    def test_ten_in_various_bases(self):
        assert change_base(10, 2) == "1010"
        assert change_base(10, 3) == "101"
        assert change_base(10, 4) == "22"
        assert change_base(10, 5) == "20"
        assert change_base(10, 6) == "14"
        assert change_base(10, 7) == "13"
        assert change_base(10, 8) == "12"
        assert change_base(10, 9) == "11"

    # Larger numbers
    def test_larger_numbers(self):
        assert change_base(100, 2) == "1100100"
        assert change_base(100, 8) == "144"
        assert change_base(100, 10) == "100"
        assert change_base(255, 2) == "11111111"
        assert change_base(255, 16) == "ff"  # Note: base < 10 per docstring, so skip hex digits

    # Numbers equal to base
    def test_number_equal_to_base(self):
        assert change_base(3, 3) == "10"
        assert change_base(5, 5) == "10"
        assert change_base(9, 9) == "10"

    # Number one less than base
    def test_number_one_less_than_base(self):
        assert change_base(2, 3) == "2"
        assert change_base(4, 5) == "4"
        assert change_base(8, 9) == "8"

    # Single digit results
    def test_single_digit_results(self):
        assert change_base(1, 5) == "1"
        assert change_base(2, 5) == "2"
        assert change_base(3, 5) == "3"
        assert change_base(4, 5) == "4"

    # Consecutive numbers
    def test_consecutive_numbers_base_2(self):
        assert change_base(1, 2) == "1"
        assert change_base(2, 2) == "10"
        assert change_base(3, 2) == "11"
        assert change_base(4, 2) == "100"
        assert change_base(5, 2) == "101"
        assert change_base(6, 2) == "110"
        assert change_base(7, 2) == "111"
        assert change_base(8, 2) == "1000"

    # All valid bases for a given number
    @pytest.mark.parametrize("x", [1, 2, 3, 4, 5, 6, 7, 8, 9])
    @pytest.mark.parametrize("base", [2, 3, 4, 5, 6, 7, 8, 9])
    def test_all_valid_combinations(self, x, base):
        result = change_base(x, base)
        assert isinstance(result, str)
        assert all(c.isdigit() for c in result)


class TestChangeBaseEdgeCases:
    """Test edge cases and error conditions."""

    def test_base_1_raises_error(self):
        """Base 1 would cause an infinite loop; expect an error."""
        with pytest.raises(ZeroDivisionError):
            change_base(5, 1)

    def test_base_0_raises_error(self):
        """Base 0 causes division by zero."""
        with pytest.raises(ZeroDivisionError):
            change_base(5, 0)

    def test_negative_base_raises_error(self):
        """Negative base causes issues."""
        with pytest.raises(ZeroDivisionError):
            change_base(5, -1)

    def test_large_number(self):
        """Test with a large input number."""
        assert change_base(1024, 2) == "10000000000"
        assert change_base(1000, 10) == "1000"
        assert change_base(1000, 2) == "1111101000"

    def test_return_type_is_string(self):
        """Ensure the return value is always a string."""
        assert isinstance(change_base(0, 2), str)
        assert isinstance(change_base(1, 2), str)
        assert isinstance(change_base(100, 2), str)


class TestChangeBaseInverseVerification:
    """Verify conversions by converting back to base 10."""

    @pytest.mark.parametrize("x, base", [
        (8, 3), (8, 2), (7, 2),
        (10, 2), (10, 3), (10, 8),
        (100, 2), (100, 8), (100, 9),
        (255, 2), (255, 8),
        (1024, 2), (1024, 8),
    ])
    def test_inverse_conversion(self, x, base):
        """Convert to given base and back, should get original number."""
        if base <= 0 or base > 9:
            pytest.skip(f"Skipping invalid base {base}")
        result = change_base(x, base)
        reconstructed = sum(int(digit) * (base ** i) for i, digit in enumerate(reversed(result)))
        assert reconstructed == x
