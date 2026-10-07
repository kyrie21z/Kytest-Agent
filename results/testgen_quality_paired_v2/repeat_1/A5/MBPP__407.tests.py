# Accepted by submit_tests; explanations in testgen_report.json.

from solution import rearrange_bigger as _case0_rearrange_bigger

def test_single_digit_returns_false():
    """A single-digit number has no other arrangement, so should return False."""
    assert _case0_rearrange_bigger(1) is False
    assert _case0_rearrange_bigger(5) is False
    assert _case0_rearrange_bigger(9) is False

from solution import rearrange_bigger as _case1_rearrange_bigger

def test_descending_digits_returns_false():
    """When digits are in strictly descending order, no bigger rearrangement exists."""
    assert _case1_rearrange_bigger(98765) is False
    assert _case1_rearrange_bigger(54321) is False
    assert _case1_rearrange_bigger(4321) is False

from solution import rearrange_bigger as _case2_rearrange_bigger

def test_identical_digits_returns_false():
    """All identical digits mean no distinct rearrangement is possible."""
    assert _case2_rearrange_bigger(111) is False
    assert _case2_rearrange_bigger(2222) is False
    assert _case2_rearrange_bigger(77777) is False

from solution import rearrange_bigger as _case3_rearrange_bigger

def test_simple_two_digit_swap():
    """For two-digit numbers, the next bigger is the reverse if ascending."""
    assert _case3_rearrange_bigger(12) == 21
    assert _case3_rearrange_bigger(23) == 32
    assert _case3_rearrange_bigger(45) == 54

from solution import rearrange_bigger as _case4_rearrange_bigger

def test_three_digit_next_permutation():
    """Test next permutation logic on three-digit numbers."""
    assert _case4_rearrange_bigger(132) == 213
    assert _case4_rearrange_bigger(231) == 312
    assert _case4_rearrange_bigger(123) == 132

from solution import rearrange_bigger as _case5_rearrange_bigger

def test_return_type_is_int_or_bool():
    """The function should return either an int (the next bigger number) or False (bool)."""
    result_with_solution = _case5_rearrange_bigger(12)
    assert isinstance(result_with_solution, int)
    assert result_with_solution > 12
    result_no_solution = _case5_rearrange_bigger(987)
    assert result_no_solution is False
