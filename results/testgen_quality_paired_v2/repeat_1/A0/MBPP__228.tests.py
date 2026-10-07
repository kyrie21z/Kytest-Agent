import pytest
from solution import all_Bits_Set_In_The_Given_Range


class TestAllBitsSetInRange:
    """Unit tests for all_Bits_Set_In_The_Given_Range."""

    # --- Basic cases: all bits unset in range (should return True) ---

    def test_all_unset_l1_r1(self):
        n = 0b1010  # bit 1 is 0
        assert all_Bits_Set_In_The_Given_Range(n, 1, 1) is True

    def test_all_unset_l1_r2(self):
        n = 0b1100  # bits 1-2 are 00
        assert all_Bits_Set_In_The_Given_Range(n, 1, 2) is True

    def test_all_unset_l2_r3(self):
        n = 0b1001  # bits 2-3 are 00
        assert all_Bits_Set_In_The_Given_Range(n, 2, 3) is True

    def test_all_unset_full_range(self):
        n = 0       # no bits set at all
        assert all_Bits_Set_In_The_Given_Range(n, 1, 8) is True

    def test_all_unset_single_bit_zero(self):
        n = 0b101   # bit 2 is 0
        assert all_Bits_Set_In_The_Given_Range(n, 2, 2) is True

    # --- Cases where some bits are set in range (should return False) ---

    def test_one_bit_set_l1_r1(self):
        n = 0b1011  # bit 1 is 1
        assert all_Bits_Set_In_The_Given_Range(n, 1, 1) is False

    def test_one_bit_set_l2_r2(self):
        n = 0b1010  # bit 2 is 1
        assert all_Bits_Set_In_The_Given_Range(n, 2, 2) is False

    def test_multiple_bits_set_in_range(self):
        n = 0b1110  # bits 1-3 are 111
        assert all_Bits_Set_In_The_Given_Range(n, 1, 3) is False

    def test_mixed_bits_in_range(self):
        n = 0b1101  # bits 1-3 are 101 (bit 2 is 0 but bit 1 and 3 are 1)
        assert all_Bits_Set_In_The_Given_Range(n, 1, 3) is False

    # --- Edge cases ---

    def test_l_equals_r(self):
        n = 0b1000  # bit 4 is 1
        assert all_Bits_Set_In_The_Given_Range(n, 4, 4) is False

    def test_l_equals_r_unset(self):
        n = 0b1000  # bit 3 is 0
        assert all_Bits_Set_In_The_Given_Range(n, 3, 3) is True

    def test_large_range(self):
        n = 0       # all bits unset
        assert all_Bits_Set_In_The_Given_Range(n, 1, 64) is True

    def test_range_beyond_set_bits(self):
        n = 0b1     # only bit 1 is set; range 5-10 should be all unset
        assert all_Bits_Set_In_The_Given_Range(n, 5, 10) is True

    def test_n_is_max_int(self):
        n = (1 << 32) - 1  # all 32 bits set
        assert all_Bits_Set_In_The_Given_Range(n, 1, 32) is False

    # --- Parametrized comprehensive tests ---
    # For 0b10101010 (= 170), bit positions (1-indexed from LSB):
    #   bit 1: 0, bit 2: 1, bit 3: 0, bit 4: 1, bit 5: 0, bit 6: 1, bit 7: 0, bit 8: 1

    @pytest.mark.parametrize(
        "n,l,r,expected",
        [
            # All bits unset in range -> True
            (0, 1, 1, True),
            (0, 1, 10, True),
            (0, 5, 20, True),
            (0b1010, 1, 1, True),   # bit 1 = 0
            (0b1010, 3, 3, True),   # bit 3 = 0
            (0b1100, 1, 2, True),   # bits 1-2 = 00
            (0b1001, 2, 3, True),   # bits 2-3 = 00
            (0b10101, 2, 2, True),  # bit 2 = 0
            (0b10101, 4, 4, True),  # bit 4 = 0
            (0b11110000, 1, 4, True),  # lower 4 bits all 0
            (0b11110000, 5, 8, False), # upper 4 bits all 1
            (0b00001111, 1, 4, False), # lower 4 bits all 1
            (0b00001111, 5, 8, True),  # upper 4 bits all 0
            # 0b10101010 = 170: bits 1=0,2=1,3=0,4=1,5=0,6=1,7=0,8=1
            (170, 1, 1, True),   # bit 1 = 0
            (170, 2, 2, False),  # bit 2 = 1
            (170, 3, 3, True),   # bit 3 = 0
            (170, 4, 4, False),  # bit 4 = 1
            (170, 5, 5, True),   # bit 5 = 0
            (170, 6, 6, False),  # bit 6 = 1
            (170, 7, 7, True),   # bit 7 = 0
            (170, 8, 8, False),  # bit 8 = 1
            (170, 1, 8, False),  # not all unset
            (170, 1, 3, False),  # bits 1-3 = 010 -> bit 2 is 1
            (170, 3, 5, False),  # bits 3-5 = 010 -> bit 4 is 1
            (170, 7, 9, False),  # bits 7-9: bit7=0, bit8=1 -> has a set bit
            (170, 1, 1, True),   # already covered
            (170, 3, 3, True),   # already covered
            (170, 5, 5, True),   # already covered
            (170, 7, 7, True),   # already covered
            # Range entirely beyond highest set bit
            (0b111, 4, 10, True),
            (0b1, 2, 100, True),
        ],
    )
    def test_parametrized(self, n, l, r, expected):
        assert all_Bits_Set_In_The_Given_Range(n, l, r) is expected

    # --- Invalid / boundary input handling ---

    def test_l_greater_than_r(self):
        """When l > r, the mask becomes 0, new_num = 0, returns True."""
        n = 0b1111
        assert all_Bits_Set_In_The_Given_Range(n, 5, 2) is True

    def test_l_and_r_equal_to_1(self):
        n = 0b1
        assert all_Bits_Set_In_The_Given_Range(n, 1, 1) is False

    def test_l_and_r_equal_to_1_unset(self):
        n = 0b0
        assert all_Bits_Set_In_The_Given_Range(n, 1, 1) is True
