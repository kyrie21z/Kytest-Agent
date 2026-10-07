# Accepted by submit_tests; explanations in testgen_report.json.

from solution import all_Bits_Set_In_The_Given_Range as _case0_all_Bits_Set_In_The_Given_Range

def test_all_unset_zero_n():
    """When n is 0, no bits are set anywhere, so any range should return True."""
    assert _case0_all_Bits_Set_In_The_Given_Range(0, 1, 5) is True

from solution import all_Bits_Set_In_The_Given_Range as _case1_all_Bits_Set_In_The_Given_Range

def test_all_set_in_range():
    """When all bits in the range are 1, result must be False."""
    assert _case1_all_Bits_Set_In_The_Given_Range(7, 1, 3) is False

from solution import all_Bits_Set_In_The_Given_Range as _case2_all_Bits_Set_In_The_Given_Range

def test_partial_bits_set():
    """When some bits in range are set and others unset, result is False."""
    assert _case2_all_Bits_Set_In_The_Given_Range(5, 1, 3) is False

from solution import all_Bits_Set_In_The_Given_Range as _case3_all_Bits_Set_In_The_Given_Range

def test_range_outside_set_bits():
    """When the queried range falls entirely below the highest set bit, result is True."""
    assert _case3_all_Bits_Set_In_The_Given_Range(8, 1, 3) is True

from solution import all_Bits_Set_In_The_Given_Range as _case4_all_Bits_Set_In_The_Given_Range

def test_single_bit_unset():
    """Single-bit range where that bit is 0 should return True."""
    assert _case4_all_Bits_Set_In_The_Given_Range(4, 2, 2) is True

from solution import all_Bits_Set_In_The_Given_Range as _case5_all_Bits_Set_In_The_Given_Range

def test_single_bit_set():
    """Single-bit range where that bit is 1 should return False."""
    assert _case5_all_Bits_Set_In_The_Given_Range(4, 3, 3) is False
