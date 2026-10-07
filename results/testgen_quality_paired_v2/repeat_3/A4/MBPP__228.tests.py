# Accepted by submit_tests; explanations in testgen_report.json.

"""Test that zero returns True for any range."""
from solution import all_Bits_Set_In_The_Given_Range as _case0_all_Bits_Set_In_The_Given_Range

def test_zero_all_unset():
    """Zero has no bits set, so any range should return True.

    Contract quote: 'Write a python function to check whether all the bits
    are unset in the given range or not.'

    Input domain: n=0, l=1, r=8 — zero with an 8-bit range.
    Expected result: True, since 0 & mask == 0 for any mask.
    Fault hypothesis: Implementation might mishandle n=0 edge case.
    """
    assert _case0_all_Bits_Set_In_The_Given_Range(0, 1, 8) is True

"""Test that a set bit in range yields False."""
from solution import all_Bits_Set_In_The_Given_Range as _case1_all_Bits_Set_In_The_Given_Range

def test_single_bit_set_in_range():
    """Bit at position 1 (LSB) is set in n=1, so range [1,1] should be False.

    Contract quote: 'Write a python function to check whether all the bits
    are unset in the given range or not.'

    Input domain: n=1 (0b1), l=1, r=1 — single-bit range covering LSB.
    Expected result: False, because bit 0 of 1 is 1 (set).
    Fault hypothesis: Function might always return True regardless of bit values.
    """
    assert _case1_all_Bits_Set_In_The_Given_Range(1, 1, 1) is False

"""Test that any single set bit in range causes False."""
from solution import all_Bits_Set_In_The_Given_Range as _case2_all_Bits_Set_In_The_Given_Range

def test_one_bit_set_among_unset():
    """n=0b101010 (42): bits 1,3,5 are 1; bits 2,4 are 0.
    Range [2,4] covers bits 1-3 (0-indexed): bit 1=0, bit 2=1, bit 3=0.

    Contract quote: 'Write a python function to check whether all the bits
    are unset in the given range or not.'

    Input domain: n=42 (0b101010), l=2, r=4.
    Expected result: False, because bit 2 (0-indexed) of 42 is 1.
    Fault hypothesis: Only checks first/last bit instead of entire range.
    """
    assert _case2_all_Bits_Set_In_The_Given_Range(42, 2, 4) is False

"""Test that return value is strictly a Python bool."""
from solution import all_Bits_Set_In_The_Given_Range as _case3_all_Bits_Set_In_The_Given_Range

def test_return_type_bool():
    """Verify the function returns a bool, not int.

    Contract quote: 'Write a python function to check whether all the bits
    are unset in the given range or not.'

    Input domain: n=0, l=1, r=1 — simple query guaranteed to return True.
    Expected result: isinstance(result, bool) is True and result is True.
    Fault hypothesis: Returns 0/1 integers instead of True/False booleans.
    """
    result = _case3_all_Bits_Set_In_The_Given_Range(0, 1, 1)
    assert isinstance(result, bool)
    assert result is True

"""Test unset high-order bits in range."""
from solution import all_Bits_Set_In_The_Given_Range as _case4_all_Bits_Set_In_The_Given_Range

def test_high_bits_unset():
    """n=0b111 (7): only bits 0,1,2 are set. Bits 3-6 are 0.
    Range [4,6] checks bits 3-5 (0-indexed), all should be 0.

    Contract quote: 'Write a python function to check whether all the bits
    are unset in the given range or not.'

    Input domain: n=7 (0b111), l=4, r=6.
    Expected result: True, bits 3-5 of 7 are all 0.
    Fault hypothesis: Mask might overflow or miscalculate for higher positions.
    """
    assert _case4_all_Bits_Set_In_The_Given_Range(7, 4, 6) is True

"""Test consecutive unset bits in a wider range."""
from solution import all_Bits_Set_In_The_Given_Range as _case5_all_Bits_Set_In_The_Given_Range

def test_multiple_bits_unset_consecutive():
    """Bits 1-4 of n=0b11110000 (240) are all 0.

    Contract quote: 'Write a python function to check whether all the bits
    are unset in the given range or not.'

    Input domain: n=240 (0b11110000), l=1, r=4 — four consecutive low bits.
    Expected result: True, bits 0-3 of 240 are all 0.
    Fault hypothesis: Mask computation off-by-one, checking wrong bit positions.
    """
    assert _case5_all_Bits_Set_In_The_Given_Range(240, 1, 4) is True
