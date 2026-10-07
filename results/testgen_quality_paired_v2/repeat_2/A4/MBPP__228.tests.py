# Accepted by submit_tests; explanations in testgen_report.json.

from solution import all_Bits_Set_In_The_Given_Range as _case0_all_Bits_Set_In_The_Given_Range

def test_all_unset_range():
    """n=5 (101 binary), range [2,2]: bit 2 is 0, so all bits in range are unset."""
    assert _case0_all_Bits_Set_In_The_Given_Range(5, 2, 2) is True

from solution import all_Bits_Set_In_The_Given_Range as _case1_all_Bits_Set_In_The_Given_Range

def test_some_set_in_range():
    """n=5 (101 binary), range [1,3]: bits include both 0s and 1s, not all unset."""
    assert _case1_all_Bits_Set_In_The_Given_Range(5, 1, 3) is False

from solution import all_Bits_Set_In_The_Given_Range as _case2_all_Bits_Set_In_The_Given_Range

def test_n_zero_all_unset():
    """n=0 has no bits set anywhere, so any range should return True."""
    assert _case2_all_Bits_Set_In_The_Given_Range(0, 1, 5) is True
    assert _case2_all_Bits_Set_In_The_Given_Range(0, 10, 20) is True

from solution import all_Bits_Set_In_The_Given_Range as _case3_all_Bits_Set_In_The_Given_Range

def test_all_bits_set_in_range():
    """n=7 (111 binary), range [1,3]: all three bits are 1, so not all unset."""
    assert _case3_all_Bits_Set_In_The_Given_Range(7, 1, 3) is False

from solution import all_Bits_Set_In_The_Given_Range as _case4_all_Bits_Set_In_The_Given_Range

def test_single_bit_unset():
    """n=4 (100 binary), range [1,1]: bit 1 is 0, so all bits in range are unset."""
    assert _case4_all_Bits_Set_In_The_Given_Range(4, 1, 1) is True

from solution import all_Bits_Set_In_The_Given_Range as _case5_all_Bits_Set_In_The_Given_Range

def test_return_type_check():
    """Verify the function always returns a boolean value."""
    result_true = _case5_all_Bits_Set_In_The_Given_Range(0, 1, 1)
    result_false = _case5_all_Bits_Set_In_The_Given_Range(1, 1, 1)
    assert isinstance(result_true, bool)
    assert isinstance(result_false, bool)
    assert result_true is True
    assert result_false is False
