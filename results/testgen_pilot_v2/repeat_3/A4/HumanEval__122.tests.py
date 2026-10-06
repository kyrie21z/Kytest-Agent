# Accepted by submit_tests; explanations in testgen_report.json.

from solution import add_elements as _case0_add_elements

def test_docstring_example():
    """Test the exact example from the docstring."""
    result = _case0_add_elements([111, 21, 3, 4000, 5, 6, 7, 8, 9], 4)
    assert result == 24

from solution import add_elements as _case1_add_elements

def test_all_qualify():
    """Test when all first-k elements have at most two digits."""
    result = _case1_add_elements([1, 2, 3], 3)
    assert result == 6

from solution import add_elements as _case2_add_elements

def test_none_qualify():
    """Test when no first-k elements have at most two digits."""
    result = _case2_add_elements([100, 200, 300], 3)
    assert result == 0

from solution import add_elements as _case3_add_elements

def test_negative_two_digit():
    """Test negative numbers with at most two digits."""
    result = _case3_add_elements([-5, -42, 100], 3)
    assert result == -47

from solution import add_elements as _case4_add_elements

def test_boundary_two_digits():
    """Test boundary values: 99 (max 2-digit) and 100 (min 3-digit)."""
    result = _case4_add_elements([99, 100, -99, -100], 4)
    assert result == 0

from solution import add_elements as _case5_add_elements

def test_return_type_and_single_element():
    """Test return type is int and single-element case."""
    result = _case5_add_elements([42], 1)
    assert isinstance(result, int)
    assert result == 42
