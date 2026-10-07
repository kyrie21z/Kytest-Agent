import pytest
from solution import all_Bits_Set_In_The_Given_Range


class TestAllBitsSetInRange:
    """Tests for the all_Bits_Set_In_The_Given_Range function."""

    # ------------------------------------------------------------------ #
    # Basic correctness – single-bit ranges
    # ------------------------------------------------------------------ #

    def test_single_unset_bit_at_position_1(self):
        """Bit at position 1 is 0 → should return True."""
        assert all_Bits_Set_In_The_Given_Range(0b0, 1, 1) is True

    def test_single_set_bit_at_position_1(self):
        """Bit at position 1 is 1 → should return False."""
        assert all_Bits_Set_In_The_Given_Range(0b1, 1, 1) is False

    def test_single_unset_bit_at_position_3(self):
        """Bit at position 3 is 0 (e.g. 0b011 = 3) → should return True."""
        assert all_Bits_Set_In_The_Given_Range(0b011, 3, 3) is True

    def test_single_set_bit_at_position_3(self):
        """Bit at position 3 is 1 (e.g. 0b101 = 5) → should return False."""
        assert all_Bits_Set_In_The_Given_Range(0b101, 3, 3) is False

    # ------------------------------------------------------------------ #
    # Multi-bit ranges where all bits are unset
    # ------------------------------------------------------------------ #

    def test_range_all_unset_l1_r2(self):
        """Bits 1-2 are both 0 → True."""
        assert all_Bits_Set_In_The_Given_Range(0b100, 1, 2) is True

    def test_range_all_unset_l2_r4(self):
        """Bits 2-4 are all 0 → True."""
        assert all_Bits_Set_In_The_Given_Range(0b10001, 2, 4) is True

    def test_full_range_all_unset(self):
        """All bits unset (n == 0) → True for any valid range."""
        assert all_Bits_Set_In_The_Given_Range(0, 1, 8) is True
        assert all_Bits_Set_In_The_Given_Range(0, 1, 32) is True

    # ------------------------------------------------------------------ #
    # Multi-bit ranges where at least one bit is set
    # ------------------------------------------------------------------ #

    def test_range_one_set_bit_l1_r2(self):
        """Bit 1 is set → False."""
        assert all_Bits_Set_In_The_Given_Range(0b11, 1, 2) is False

    def test_range_one_set_bit_l2_r3(self):
        """Bit 2 is set → False."""
        assert all_Bits_Set_In_The_Given_Range(0b101, 2, 3) is False

    def test_range_both_set_l1_r3(self):
        """Bits 1-3 all set → False."""
        assert all_Bits_Set_In_The_Given_Range(0b111, 1, 3) is False

    # ------------------------------------------------------------------ #
    # Edge cases – l == r (single bit)
    # ------------------------------------------------------------------ #

    @pytest.mark.parametrize("n,bit_pos", [
        (0b0, 1),
        (0b0, 5),
        (0b0, 16),
        (0b1, 1),
        (0b1, 5),
        (0b1, 16),
    ])
    def test_single_bit_edge_cases(self, n, bit_pos):
        """Single-bit range edge cases."""
        expected = False if (n >> (bit_pos - 1)) & 1 else True
        assert all_Bits_Set_In_The_Given_Range(n, bit_pos, bit_pos) == expected

    # ------------------------------------------------------------------ #
    # Large numbers
    # ------------------------------------------------------------------ #

    def test_large_number_unset_bits(self):
        """Large number with specific bits unset."""
        # 0b11110000 → bits 1-4 are 0
        assert all_Bits_Set_In_The_Given_Range(0b11110000, 1, 4) is True

    def test_large_number_set_bits(self):
        """Large number with some bits set in range."""
        # 0b11110000 → bits 5-8 are 1
        assert all_Bits_Set_In_The_Given_Range(0b11110000, 5, 8) is False

    def test_max_range(self):
        """Range covering entire width of the number."""
        assert all_Bits_Set_In_The_Given_Range(0b0000, 1, 4) is True
        assert all_Bits_Set_In_The_Given_Range(0b1111, 1, 4) is False

    # ------------------------------------------------------------------ #
    # Boundary / invalid input handling
    # ------------------------------------------------------------------ #

    @pytest.mark.parametrize("n,l,r", [
        (5, 1, 1),   # normal small case
        (10, 1, 4),  # normal medium case
        (255, 1, 8), # full byte
        (255, 4, 7), # sub-range of full byte
    ])
    def test_various_normal_inputs(self, n, l, r):
        """Sanity-check various normal inputs against manual computation."""
        mask = (((1 << r) - 1) ^ ((1 << (l - 1)) - 1))
        expected = (n & mask) == 0
        assert all_Bits_Set_In_The_Given_Range(n, l, r) == expected

    # ------------------------------------------------------------------ #
    # Property-based sanity check
    # ------------------------------------------------------------------ #

    def test_n_zero_always_true(self):
        """When n is 0, every range should return True."""
        for l in range(1, 10):
            for r in range(l, 10):
                assert all_Bits_Set_In_The_Given_Range(0, l, r) is True

    def test_n_all_ones_returns_false_for_valid_ranges(self):
        """When n has all bits set, every valid range should return False."""
        n = (1 << 16) - 1  # 16 ones
        for l in range(1, 16):
            for r in range(l, 16):
                assert all_Bits_Set_In_The_Given_Range(n, l, r) is False
