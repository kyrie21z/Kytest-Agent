# Accepted by submit_tests; explanations in testgen_report.json.

from solution import rearrange_bigger as _case0_rearrange_bigger

def test_next_bigger_simple():
    """Test basic two-digit case where next bigger number exists."""
    assert _case0_rearrange_bigger(12) == 21
    assert isinstance(_case0_rearrange_bigger(12), int)

from solution import rearrange_bigger as _case1_rearrange_bigger

def test_no_bigger_returns_false():
    """Test that descending-order digits return False."""
    assert _case1_rearrange_bigger(21) is False
    assert _case1_rearrange_bigger(5) is False
    assert _case1_rearrange_bigger(321) is False

from solution import rearrange_bigger as _case2_rearrange_bigger

def test_three_digits_increasing():
    """Test three-digit number with strictly increasing digits."""
    assert _case2_rearrange_bigger(123) == 132
    assert isinstance(_case2_rearrange_bigger(123), int)
    assert _case2_rearrange_bigger(456) == 465

from solution import rearrange_bigger as _case3_rearrange_bigger

def test_repeated_digits():
    """Test numbers with repeated digits."""
    assert _case3_rearrange_bigger(199) == 919
    assert _case3_rearrange_bigger(991) is False
    assert _case3_rearrange_bigger(11) is False

from solution import rearrange_bigger as _case4_rearrange_bigger

def test_zeros_in_digits():
    """Test numbers containing zero digits."""
    assert _case4_rearrange_bigger(102) == 120
    assert _case4_rearrange_bigger(201) == 210
    assert _case4_rearrange_bigger(10) is False

from solution import rearrange_bigger as _case5_rearrange_bigger

def test_return_type_and_boundary():
    """Verify return types and boundary conditions."""
    assert isinstance(_case5_rearrange_bigger(12), int)
    assert isinstance(_case5_rearrange_bigger(123), int)
    assert _case5_rearrange_bigger(21) is False
    assert _case5_rearrange_bigger(5) is False
    assert _case5_rearrange_bigger(999) is False
    assert _case5_rearrange_bigger(10) is False
    assert _case5_rearrange_bigger(1234) == 1243
    assert _case5_rearrange_bigger(1999) == 9199
