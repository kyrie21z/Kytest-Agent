# Accepted by submit_tests; explanations in testgen_report.json.

from solution import prod_signs as _case0_prod_signs

def test_empty_returns_none():
    """Verify that an empty array returns None as documented."""
    assert _case0_prod_signs([]) is None

from solution import prod_signs as _case1_prod_signs

def test_contains_zero_returns_zero():
    """Any array containing a zero element should return 0."""
    assert _case1_prod_signs([0, 1, 2, 3]) == 0
    assert _case1_prod_signs([5, 0, -3]) == 0
    assert _case1_prod_signs([0]) == 0

from solution import prod_signs as _case2_prod_signs

def test_all_positive():
    """All-positive arrays: product of signs is +1, so result equals sum of magnitudes."""
    assert _case2_prod_signs([1, 2, 2, -4]) == -9
    assert _case2_prod_signs([1, 2, 3]) == 6
    assert _case2_prod_signs([10]) == 10

from solution import prod_signs as _case3_prod_signs

def test_odd_negatives_yield_negative():
    """Odd number of negative elements: sign product is -1, result is negative."""
    assert _case3_prod_signs([-1, -2, -3]) == -6
    assert _case3_prod_signs([-5]) == -5
    assert _case3_prod_signs([1, -2, 3]) == -6

from solution import prod_signs as _case4_prod_signs

def test_even_negatives_yield_positive():
    """Even number of negative elements: sign product is +1, result is positive sum of magnitudes."""
    assert _case4_prod_signs([-1, -2]) == 3
    assert _case4_prod_signs([-3, 4, -5, 6]) == 18
    assert _case4_prod_signs([-1, -1, -1, -1]) == 4

from solution import prod_signs as _case5_prod_signs

def test_return_type_and_boundary():
    """Check return types: None for empty, int for non-empty integer arrays."""
    result_empty = _case5_prod_signs([])
    assert result_empty is None
    assert isinstance(result_empty, type(None))
    result_single = _case5_prod_signs([42])
    assert isinstance(result_single, int)
    assert result_single == 42
    result_mixed = _case5_prod_signs([1, 2, 2, -4])
    assert isinstance(result_mixed, int)
    assert result_mixed == -9
