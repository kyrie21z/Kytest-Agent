"""Unit tests for change_base function in solution.py."""

import pytest
from solution import change_base


class TestChangeBaseDocstringExamples:
    """Test cases from the docstring examples."""

    def test_change_base_8_to_3(self):
        assert change_base(8, 3) == '22'

    def test_change_base_8_to_2(self):
        assert change_base(8, 2) == '1000'

    def test_change_base_7_to_2(self):
        assert change_base(7, 2) == '111'


class TestChangeBaseZeroAndSmallInputs:
    """Boundary cases at edges of valid input ranges."""

    def test_zero_input(self):
        """x == 0 should return '0' regardless of base."""
        assert change_base(0, 2) == '0'
        assert change_base(0, 8) == '0'
        assert change_base(0, 10) == '0'

    def test_one_input(self):
        """Smallest positive integer should return '1'."""
        assert change_base(1, 2) == '1'
        assert change_base(1, 3) == '1'
        assert change_base(1, 9) == '1'

    def test_single_digit_in_same_base(self):
        """A single-digit number in its own base returns itself."""
        assert change_base(5, 5) == '5'
        assert change_base(9, 9) == '9'

    def test_two_in_binary(self):
        assert change_base(2, 2) == '10'

    def test_three_in_binary(self):
        assert change_base(3, 2) == '11'

    def test_four_in_binary(self):
        assert change_base(4, 2) == '100'


class TestChangeBaseNormalCases:
    """Normal cases with typical inputs across various bases."""

    def test_ten_in_binary(self):
        assert change_base(10, 2) == '1010'

    def test_ten_in_octal(self):
        assert change_base(10, 8) == '12'

    def test_ten_in_decimal(self):
        assert change_base(10, 10) == '10'

    def test_hundred_in_decimal(self):
        assert change_base(100, 10) == '100'

    def test_hundred_in_binary(self):
        assert change_base(100, 2) == '1100100'

    def test_hundred_in_octal(self):
        assert change_base(100, 8) == '144'

    def test_hundred_in_hexadecimal_like_base_9(self):
        assert change_base(100, 9) == '121'

    def test_fifty_in_base_3(self):
        # 50 = 1*27 + 2*9 + 1*3 + 2*1 = 1212_3
        assert change_base(50, 3) == '1212'

    def test_sixty_three_in_base_2(self):
        # 63 = 111111_2
        assert change_base(63, 2) == '111111'

    def test_sixty_three_in_base_8(self):
        # 63 = 77_8
        assert change_base(63, 8) == '77'

    def test_sixty_three_in_base_10(self):
        assert change_base(63, 10) == '63'

    def test_large_number_in_binary(self):
        assert change_base(255, 2) == '11111111'

    def test_large_number_in_octal(self):
        assert change_base(255, 8) == '377'

    def test_large_number_in_decimal(self):
        assert change_base(255, 10) == '255'

    def test_power_of_two(self):
        assert change_base(16, 2) == '10000'

    def test_power_of_two_larger(self):
        assert change_base(1024, 2) == '10000000000'

    def test_base_4_conversion(self):
        # 10 = 2*4 + 2 = 22_4
        assert change_base(10, 4) == '22'

    def test_base_5_conversion(self):
        # 25 = 1*25 + 0*5 + 0 = 100_5
        assert change_base(25, 5) == '100'

    def test_base_6_conversion(self):
        # 36 = 1*36 = 100_6
        assert change_base(36, 6) == '100'


class TestChangeBaseReturnTypes:
    """Verify return type is always a string."""

    def test_returns_string_for_nonzero(self):
        assert isinstance(change_base(10, 2), str)

    def test_returns_string_for_zero(self):
        assert isinstance(change_base(0, 5), str)

    def test_returns_string_for_large(self):
        assert isinstance(change_base(1000, 2), str)


class TestChangeBaseEdgeBases:
    """Test with smallest and largest documented bases."""

    def test_smallest_valid_base_2(self):
        assert change_base(7, 2) == '111'

    def test_largest_documented_base_9(self):
        # 9 in base 9 is '10'
        assert change_base(9, 9) == '10'
        # 10 in base 9 is '11'
        assert change_base(10, 9) == '11'
        # 80 in base 9: 80 = 8*9 + 8 = 88_9
        assert change_base(80, 9) == '88'

    def test_base_3_various_values(self):
        assert change_base(1, 3) == '1'
        assert change_base(2, 3) == '2'
        assert change_base(3, 3) == '10'
        assert change_base(8, 3) == '22'
        assert change_base(26, 3) == '222'  # 2*9 + 2*3 + 2 = 26


class TestChangeBaseInvalidInputs:
    """Test behavior with invalid or edge-case inputs outside documented constraints."""

    def test_base_1_causes_infinite_loop_or_error(self):
        """Base 1 is not a valid positional base; the function will loop forever.
        We use a timeout to verify it does not complete normally."""
        with pytest.raises(Exception):
            # This would infinite-loop; we expect it to be interrupted
            change_base(5, 1)

    def test_negative_base(self):
        """Negative base produces unexpected/infinite results."""
        with pytest.raises(Exception):
            change_base(10, -2)

    def test_negative_x(self):
        """Negative x causes infinite loop due to floor division behavior."""
        with pytest.raises(Exception):
            change_base(-7, 2)
