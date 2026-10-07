# Accepted by submit_tests; explanations in testgen_report.json.

from solution import count_X as _case0_count_X

def test_empty_tuple():
    """Test that counting in an empty tuple returns 0."""
    result = _case0_count_X((), 5)
    assert result == 0

from solution import count_X as _case1_count_X

def test_element_not_present():
    """Test that counting a missing element returns 0."""
    result = _case1_count_X((1, 2, 3), 4)
    assert result == 0

from solution import count_X as _case2_count_X

def test_single_occurrence():
    """Test counting an element that appears exactly once."""
    result = _case2_count_X((1, 2, 3, 2, 5), 3)
    assert result == 1

from solution import count_X as _case3_count_X

def test_multiple_occurrences():
    """Test counting an element that appears multiple times."""
    result = _case3_count_X((1, 2, 3, 2, 5, 2), 2)
    assert result == 3

from solution import count_X as _case4_count_X

def test_all_elements_match():
    """Test when every element in the tuple matches x."""
    result = _case4_count_X(('a', 'a', 'a'), 'a')
    assert result == 3

from solution import count_X as _case5_count_X

def test_type_preservation():
    """Test that the return value is always an integer."""
    result = _case5_count_X((1, 2, 1), 1)
    assert isinstance(result, int)
