# Accepted by submit_tests; explanations in testgen_report.json.

import solution as _case0_solution

def test_basic_next_permutation():
    """Test that 12 becomes 21 - the simplest next permutation."""
    result = _case0_solution.rearrange_bigger(12)
    assert result == 21
    assert isinstance(result, int)

import solution as _case1_solution

def test_descending_order_returns_false():
    """Test that numbers with digits in descending order return False."""
    result = _case1_solution.rearrange_bigger(321)
    assert result is False

import solution as _case2_solution

def test_single_digit_returns_false():
    """Test that single-digit numbers return False since no rearrangement is possible."""
    result = _case2_solution.rearrange_bigger(5)
    assert result is False

import solution as _case3_solution

def test_repeated_digits():
    """Test next permutation with repeated digits: 1221 -> 2112."""
    result = _case3_solution.rearrange_bigger(1221)
    assert result == 2112
    assert isinstance(result, int)

import solution as _case4_solution

def test_consecutive_increasing_digits():
    """Test swapping last two digits: 1234 -> 1243."""
    result = _case4_solution.rearrange_bigger(1234)
    assert result == 1243
    assert isinstance(result, int)

import solution as _case5_solution

def test_all_same_digits_returns_false():
    """Test that numbers with all identical digits return False."""
    result = _case5_solution.rearrange_bigger(2222)
    assert result is False
