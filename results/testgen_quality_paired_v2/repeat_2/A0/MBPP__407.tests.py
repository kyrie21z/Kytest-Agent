import pytest
from solution import rearrange_bigger


class TestRearrangeBiggerBasic:
    """Tests for basic functionality."""

    def test_two_digits_ascending(self):
        assert rearrange_bigger(12) == 21

    def test_two_digits_descending(self):
        assert rearrange_bigger(21) is False

    def test_three_digits_simple(self):
        assert rearrange_bigger(513) == 531

    def test_three_digits_with_swap(self):
        assert rearrange_bigger(132) == 213

    def test_four_digits_simple(self):
        assert rearrange_bigger(1234) == 1243

    def test_four_digits_complex(self):
        assert rearrange_bigger(2071) == 2107

    def test_five_digits(self):
        assert rearrange_bigger(12345) == 12354


class TestRearrangeBiggerNoSolution:
    """Tests where no bigger number can be formed."""

    def test_single_digit(self):
        assert rearrange_bigger(5) is False

    def test_all_same_digits(self):
        assert rearrange_bigger(111) is False

    def test_descending_order(self):
        assert rearrange_bigger(4321) is False

    def test_descending_order_longer(self):
        assert rearrange_bigger(98765) is False

    def test_two_digits_descending(self):
        assert rearrange_bigger(21) is False

    def test_repeated_start_no_solution(self):
        # 331 -> digits are 3,3,1; no ascending pair from right, so False
        assert rearrange_bigger(331) is False

    def test_zero_at_end_no_solution(self):
        # 10 -> digits are 1,0; '1' > '0', no ascending pair, so False
        assert rearrange_bigger(10) is False


class TestRearrangeBiggerRepeatedDigits:
    """Tests with repeated digits."""

    def test_repeated_middle(self):
        assert rearrange_bigger(122) == 212

    def test_repeated_end(self):
        assert rearrange_bigger(1233) == 1323

    def test_many_repeats_has_solution(self):
        # 1999999999 -> '1' < '9' at index 0, swap 1 with smallest digit > 1 in suffix
        result = rearrange_bigger(1999999999)
        assert isinstance(result, int)
        assert result > 1999999999

    def test_repeats_with_solution(self):
        # 1999999998 -> has a valid next permutation
        result = rearrange_bigger(1999999998)
        assert isinstance(result, int)
        assert result > 1999999998


class TestRearrangeBiggerZeros:
    """Tests involving zero digits."""

    def test_zero_in_middle(self):
        assert rearrange_bigger(102) == 120

    def test_zero_at_end(self):
        assert rearrange_bigger(120) == 201

    def test_multiple_zeros(self):
        assert rearrange_bigger(1002) == 1020


class TestRearrangeBiggerEdgeCases:
    """Additional edge cases."""

    def test_larger_number(self):
        assert rearrange_bigger(123456789) == 123456798

    def test_adjacent_swap_needed(self):
        assert rearrange_bigger(123456798) == 123456879

    def test_negative_number(self):
        # Negative numbers converted to string include '-' sign
        result = rearrange_bigger(-12)
        assert isinstance(result, int)

    def test_return_type_is_int(self):
        assert isinstance(rearrange_bigger(12), int)

    def test_return_type_false(self):
        assert rearrange_bigger(4321) is False

    def test_float_input_raises_value_error(self):
        # Floats have '.' in their string representation, causing ValueError
        with pytest.raises(ValueError):
            rearrange_bigger(3.14)

    def test_string_input_works(self):
        # String input works because str("123") == "123"
        assert rearrange_bigger("123") == 132
