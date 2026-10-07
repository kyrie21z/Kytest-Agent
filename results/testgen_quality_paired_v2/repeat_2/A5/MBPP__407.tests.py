# Accepted by submit_tests; explanations in testgen_report.json.

from solution import rearrange_bigger as _case0_rearrange_bigger

def test_basic_next_permutation():
    """Test basic next permutation: 123 -> 132."""
    assert _case0_rearrange_bigger(123) == 132

from solution import rearrange_bigger as _case1_rearrange_bigger

def test_descending_returns_false():
    """Test that descending-order digits return False."""
    assert _case1_rearrange_bigger(321) is False

from solution import rearrange_bigger as _case2_rearrange_bigger

def test_single_digit():
    """Test single-digit input returns False."""
    assert _case2_rearrange_bigger(5) is False

from solution import rearrange_bigger as _case3_rearrange_bigger

def test_duplicate_digits():
    """Test input with duplicate digits: 155 -> 515."""
    assert _case3_rearrange_bigger(155) == 515

from solution import rearrange_bigger as _case4_rearrange_bigger

def test_boundary_two_digits():
    """Test two-digit ascending: 12 -> 21."""
    assert _case4_rearrange_bigger(12) == 21
    assert _case4_rearrange_bigger(21) is False
