# Accepted by submit_tests; explanations in testgen_report.json.

from solution import count_X as _case0_count_X

def test_count_basic():
    """Test basic counting of an element appearing multiple times."""
    result = _case0_count_X((1, 2, 3, 2, 4, 2), 2)
    assert result == 3

from solution import count_X as _case1_count_X

def test_count_zero():
    """Test counting an element that does not appear in the tuple."""
    result = _case1_count_X((1, 2, 3, 4, 5), 6)
    assert result == 0

from solution import count_X as _case2_count_X

def test_count_empty_tuple():
    """Test counting in an empty tuple returns 0."""
    result = _case2_count_X((), 1)
    assert result == 0

from solution import count_X as _case3_count_X

def test_count_single_match():
    """Test counting when the tuple has exactly one matching element."""
    result = _case3_count_X(('a', 'b', 'c'), 'b')
    assert result == 1

from solution import count_X as _case4_count_X

def test_count_all_same():
    """Test counting when all elements in the tuple match the target."""
    result = _case4_count_X((5, 5, 5, 5), 5)
    assert result == 4

from solution import count_X as _case5_count_X

def test_count_return_type():
    """Test that the return value is an integer."""
    result = _case5_count_X((1, 2, 1), 1)
    assert isinstance(result, int)
    assert not isinstance(result, bool)
