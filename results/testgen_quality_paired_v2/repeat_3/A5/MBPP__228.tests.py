# Accepted by submit_tests; explanations in testgen_report.json.

def test_all_unset_basic():
    from solution import all_Bits_Set_In_The_Given_Range
    assert all_Bits_Set_In_The_Given_Range(5, 2, 2) is True
    assert all_Bits_Set_In_The_Given_Range(7, 1, 3) is False

def test_zero_n():
    from solution import all_Bits_Set_In_The_Given_Range
    assert all_Bits_Set_In_The_Given_Range(0, 1, 1) is True
    assert all_Bits_Set_In_The_Given_Range(0, 1, 32) is True
    assert all_Bits_Set_In_The_Given_Range(0, 5, 10) is True

def test_single_bit_set():
    from solution import all_Bits_Set_In_The_Given_Range
    assert all_Bits_Set_In_The_Given_Range(4, 3, 3) is False
    assert all_Bits_Set_In_The_Given_Range(4, 1, 1) is True
    assert all_Bits_Set_In_The_Given_Range(4, 2, 2) is True
    assert all_Bits_Set_In_The_Given_Range(4, 4, 4) is True

def test_range_beyond_bits():
    from solution import all_Bits_Set_In_The_Given_Range
    assert all_Bits_Set_In_The_Given_Range(1, 5, 10) is True
    assert all_Bits_Set_In_The_Given_Range(1, 2, 3) is True
    assert all_Bits_Set_In_The_Given_Range(1, 1, 1) is False

def test_full_range_all_ones():
    from solution import all_Bits_Set_In_The_Given_Range
    assert all_Bits_Set_In_The_Given_Range(255, 1, 8) is False
    assert all_Bits_Set_In_The_Given_Range(255, 1, 1) is False
    assert all_Bits_Set_In_The_Given_Range(255, 8, 8) is False
    assert all_Bits_Set_In_The_Given_Range(255, 9, 10) is True
