# Accepted by submit_tests; explanations in testgen_report.json.

from solution import max_product as _case0_max_product

def test_basic_increasing():
    """Test that max_product correctly computes the product of the full increasing array."""
    result = _case0_max_product([1, 2, 3])
    assert result == 6

from solution import max_product as _case1_max_product

def test_single_element():
    """A single-element array should return that element itself."""
    result = _case1_max_product([7])
    assert result == 7

from solution import max_product as _case2_max_product

def test_strictly_decreasing():
    """For a strictly decreasing array, no two consecutive elements form an increasing pair,
    so the answer is the maximum single element."""
    result = _case2_max_product([5, 4, 3, 2, 1])
    assert result == 5

from solution import max_product as _case3_max_product

def test_mixed_with_peak():
    """Test an array with an increasing run followed by a drop and another increase."""
    result = _case3_max_product([2, 3, 5, 4, 6])
    assert result == 30

from solution import max_product as _case4_max_product

def test_equal_elements():
    """When all elements are equal, the code treats them as non-decreasing (no strict inequality).
    The product of all elements should be returned."""
    result = _case4_max_product([3, 3, 3])
    assert result == 27

from solution import max_product as _case5_max_product

def test_return_type_int():
    """Verify the return value is an integer for integer inputs."""
    result = _case5_max_product([2, 3, 4])
    assert isinstance(result, int)
    assert result == 24
