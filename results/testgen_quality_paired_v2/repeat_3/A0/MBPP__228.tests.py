import pytest
from solution import all_Bits_Set_In_The_Given_Range


class TestAllBitsSetInRange:
    """Tests for all_Bits_Set_In_The_Given_Range(n, l, r).

    The function checks whether ALL bits in the 1-indexed range [l, r] of n are
    *unset* (i.e., equal to 0). Returns True if every bit in that range is 0,
    False otherwise.
    """

    # ------------------------------------------------------------------
    # Basic positive cases – all bits in range are 0
    # ------------------------------------------------------------------

    def test_all_unset_single_bit_l_equals_r(self):
        """n = 4 (100), range [2,2] -> bit 2 is 0 => True"""
        assert all_Bits_Set_In_The_Given_Range(4, 2, 2) is True

    def test_all_unset_range_at_lowest_bits(self):
        """n = 8 (1000), range [1,2] -> bits 1,2 are 0,0 => True"""
        assert all_Bits_Set_In_The_Given_Range(8, 1, 2) is True

    def test_all_unset_middle_range(self):
        """n = 9 (1001), range [2,3] -> bits 2,3 are 0,0 => True"""
        assert all_Bits_Set_In_The_Given_Range(9, 2, 3) is True

    def test_all_unset_full_range_small_number(self):
        """n = 0, any range -> all bits are 0 => True"""
        assert all_Bits_Set_In_The_Given_Range(0, 1, 5) is True

    def test_all_unset_large_range_with_zero(self):
        """n = 0, large range -> True"""
        assert all_Bits_Set_In_The_Given_Range(0, 1, 30) is True

    def test_all_unset_high_bits_only(self):
        """n = 3 (011), range [3,4] -> bits 3,4 are 0,0 => True"""
        assert all_Bits_Set_In_The_Given_Range(3, 3, 4) is True

    # ------------------------------------------------------------------
    # Negative cases – at least one bit in range is 1
    # ------------------------------------------------------------------

    def test_one_bit_set_in_range(self):
        """n = 6 (110), range [2,3] -> bit 2 is 1 => False"""
        assert all_Bits_Set_In_The_Given_Range(6, 2, 3) is False

    def test_multiple_bits_set_in_range(self):
        """n = 7 (111), range [1,3] -> all bits 1 => False"""
        assert all_Bits_Set_In_The_Given_Range(7, 1, 3) is False

    def test_lowest_bit_set(self):
        """n = 1 (001), range [1,1] -> bit 1 is 1 => False"""
        assert all_Bits_Set_In_The_Given_Range(1, 1, 1) is False

    def test_highest_bit_set(self):
        """n = 4 (100), range [3,3] -> bit 3 is 1 => False"""
        assert all_Bits_Set_In_The_Given_Range(4, 3, 3) is False

    def test_partial_overlap_with_set_bits(self):
        """n = 10 (1010), range [2,3] -> bit 2 is 1 => False"""
        assert all_Bits_Set_In_The_Given_Range(10, 2, 3) is False

    # ------------------------------------------------------------------
    # Edge cases – boundary conditions
    # ------------------------------------------------------------------

    def test_range_beyond_number_bits(self):
        """n = 1 (1), range [5,10] -> those bits don't exist => treated as 0 => True"""
        assert all_Bits_Set_In_The_Given_Range(1, 5, 10) is True

    def test_l_equals_r_single_bit_unset(self):
        """n = 16 (10000), range [5,5] -> bit 5 is 1 => False"""
        assert all_Bits_Set_In_The_Given_Range(16, 5, 5) is False

    def test_l_equals_r_single_bit_set(self):
        """n = 16 (10000), range [1,1] -> bit 1 is 0 => True"""
        assert all_Bits_Set_In_The_Given_Range(16, 1, 1) is True

    def test_range_starting_at_bit_1(self):
        """n = 12 (1100), range [1,2] -> bits 1,2 are 0,0 => True"""
        assert all_Bits_Set_In_The_Given_Range(12, 1, 2) is True

    def test_range_ending_at_high_bit(self):
        """n = 12 (1100), range [3,4] -> bits 3,4 are 1,1 => False"""
        assert all_Bits_Set_In_The_Given_Range(12, 3, 4) is False

    def test_n_is_max_positive_integer(self):
        """n = 2^31 - 1, range [1,31] -> all bits 1 => False"""
        assert all_Bits_Set_In_The_Given_Range((1 << 31) - 1, 1, 31) is False

    def test_n_is_power_of_two(self):
        """n = 32 (100000), range [1,5] -> all 0 => True"""
        assert all_Bits_Set_In_The_Given_Range(32, 1, 5) is True

    def test_n_is_power_of_two_bit_in_range(self):
        """n = 32 (100000), range [6,6] -> bit 6 is 1 => False"""
        assert all_Bits_Set_In_The_Given_Range(32, 6, 6) is False

    # ------------------------------------------------------------------
    # Larger numbers and wider ranges
    # ------------------------------------------------------------------

    def test_large_number_all_unset_high_range(self):
        """n = 255 (0b11111111), range [9,16] -> all 0 => True"""
        assert all_Bits_Set_In_The_Given_Range(255, 9, 16) is True

    def test_large_number_some_set_in_range(self):
        """n = 255, range [1,8] -> all 1 => False"""
        assert all_Bits_Set_In_The_Given_Range(255, 1, 8) is False

    def test_alternating_pattern(self):
        """n = 85 (01010101), range [2,3] -> bits 2,3 are 0,1 => False"""
        assert all_Bits_Set_In_The_Given_Range(85, 2, 3) is False

    def test_alternating_pattern_all_unset_even(self):
        """n = 85 (01010101), range [2,2] -> bit 2 is 0 => True"""
        assert all_Bits_Set_In_The_Given_Range(85, 2, 2) is True

    # ------------------------------------------------------------------
    # Invalid / unusual inputs – should still behave predictably
    # ------------------------------------------------------------------

    def test_l_greater_than_r(self):
        """When l > r, the mask becomes non-zero due to XOR of different-sized masks.
        For n=7 (111), l=5, r=2: mask = ((1<<2)-1) ^ ((1<<4)-1) = 3 ^ 15 = 12 (1100),
        new_num = 7 & 12 = 4 != 0 => False."""
        assert all_Bits_Set_In_The_Given_Range(7, 5, 2) is False

    def test_l_equals_1(self):
        """Range starts at bit 1."""
        assert all_Bits_Set_In_The_Given_Range(0, 1, 1) is True

    def test_r_equals_1(self):
        """Range ends at bit 1."""
        assert all_Bits_Set_In_The_Given_Range(0, 1, 1) is True

    def test_both_l_and_r_equal_1(self):
        """Single-bit range at position 1."""
        assert all_Bits_Set_In_The_Given_Range(0, 1, 1) is True
        assert all_Bits_Set_In_The_Given_Range(1, 1, 1) is False
