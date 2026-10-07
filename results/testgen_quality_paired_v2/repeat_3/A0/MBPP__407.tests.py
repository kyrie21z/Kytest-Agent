import pytest
from solution import rearrange_bigger


class TestRearrangeBiggerBasic:
    """Tests for basic functionality of rearrange_bigger."""

    def test_two_digits_simple(self):
        # 12 -> 21
        assert rearrange_bigger(12) == 21

    def test_two_digits_reversed(self):
        # 21 -> False (no bigger arrangement possible)
        assert rearrange_bigger(21) is False

    def test_three_digits_simple(self):
        # 123 -> 132
        assert rearrange_bigger(123) == 132

    def test_three_digits_middle_change(self):
        # 132 -> 213
        assert rearrange_bigger(132) == 213

    def test_three_digits_last_change(self):
        # 321 -> False (descending order)
        assert rearrange_bigger(321) is False

    def test_single_digit(self):
        # Single digit has no "next bigger" arrangement
        assert rearrange_bigger(5) is False


class TestRearrangeBiggerRepeatedDigits:
    """Tests for numbers with repeated digits."""

    def test_all_same_digits(self):
        # 111 -> False (all same, no bigger arrangement)
        assert rearrange_bigger(111) is False

    def test_two_same_digits(self):
        # 112 -> 121
        assert rearrange_bigger(112) == 121

    def test_two_same_digits_second(self):
        # 121 -> 211
        assert rearrange_bigger(121) == 211

    def test_repeated_with_larger_number(self):
        # 1999 -> 9199
        assert rearrange_bigger(1999) == 9199

    def test_repeated_in_middle(self):
        # 1223 -> 1232
        assert rearrange_bigger(1223) == 1232

    def test_repeated_at_end(self):
        # 3221 -> False (descending)
        assert rearrange_bigger(3221) is False


class TestRearrangeBiggerLargerNumbers:
    """Tests for larger numbers."""

    def test_four_digits(self):
        # 1234 -> 1243
        assert rearrange_bigger(1234) == 1243

    def test_five_digits(self):
        # 12345 -> 12354
        assert rearrange_bigger(12345) == 12354

    def test_descending_large(self):
        # 9876543210 -> False
        assert rearrange_bigger(9876543210) is False

    def test_ascending_large(self):
        # 123456789 -> 123456798
        assert rearrange_bigger(123456789) == 123456798

    def test_mixed_order(self):
        # 54876 -> 56478
        assert rearrange_bigger(54876) == 56478

    def test_swap_near_end(self):
        # 1999999999 -> 9199999999
        assert rearrange_bigger(1999999999) == 9199999999


class TestRearrangeBiggerEdgeCases:
    """Tests for edge cases."""

    def test_zero(self):
        # Single digit 0
        assert rearrange_bigger(0) is False

    def test_two_digit_same(self):
        # 22 -> False
        assert rearrange_bigger(22) is False

    def test_minimal_increase(self):
        # 12 -> 21 (smallest increase)
        assert rearrange_bigger(12) == 21

    def test_maximal_decrease(self):
        # 9876543210 -> False (maximal decrease, no bigger)
        assert rearrange_bigger(9876543210) is False

    def test_leading_digit_change(self):
        # 19 -> 91
        assert rearrange_bigger(19) == 91

    def test_complex_rearrangement(self):
        # 3548 -> 3584
        assert rearrange_bigger(3548) == 3584

    def test_multiple_swaps_needed(self):
        # 1584 -> 1845
        assert rearrange_bigger(1584) == 1845

    def test_result_has_more_digits_not_possible(self):
        # The function only rearranges, so result always has same number of digits
        # unless returning False
        result = rearrange_bigger(123)
        assert result is not False
        assert len(str(result)) == len(str(123))


class TestRearrangeBiggerReturnTypes:
    """Tests for return type correctness."""

    def test_returns_integer_on_success(self):
        result = rearrange_bigger(12)
        assert isinstance(result, int)

    def test_returns_false_on_failure(self):
        result = rearrange_bigger(21)
        assert result is False

    def test_returns_false_type_is_boolean(self):
        result = rearrange_bigger(321)
        assert isinstance(result, bool)
        assert result is False


class TestRearrangeBiggerNextBiggerProperty:
    """Tests verifying the 'next bigger' property."""

    def test_result_is_greater_than_input(self):
        # For inputs where a bigger number exists
        for n in [12, 123, 132, 1234, 54876]:
            result = rearrange_bigger(n)
            if result is not False:
                assert result > n

    def test_no_smaller_arrangement_between(self):
        # 123 -> 132, and 124, 125, ..., 131 are not valid rearrangements
        # This verifies we get the *next* biggest, not just any bigger
        assert rearrange_bigger(123) == 132
        assert rearrange_bigger(124) == 142
        assert rearrange_bigger(132) == 213

    def test_consecutive_numbers(self):
        # Verify consecutive next-bigger values
        assert rearrange_bigger(123) == 132
        assert rearrange_bigger(132) == 213
        assert rearrange_bigger(213) == 231
        assert rearrange_bigger(231) == 312
        assert rearrange_bigger(312) == 321
        assert rearrange_bigger(321) is False
