# Accepted by submit_tests; explanations in testgen_report.json.

from solution import count_X as _case0_count_X

def test_count_basic():
    """Test basic counting with multiple occurrences."""
    result = _case0_count_X((1, 2, 3, 2, 2, 4), 2)
    assert result == 3
    assert isinstance(result, int)

from solution import count_X as _case1_count_X

def test_count_zero_occurrences():
    """Test when element is not present in the tuple."""
    result = _case1_count_X((1, 2, 3, 4, 5), 6)
    assert result == 0
    assert isinstance(result, int)

from solution import count_X as _case2_count_X

def test_count_empty_tuple():
    """Test with an empty tuple."""
    result = _case2_count_X((), 1)
    assert result == 0
    assert isinstance(result, int)

from solution import count_X as _case3_count_X

def test_count_single_match():
    """Test with a single-element tuple where the element matches."""
    result = _case3_count_X((42,), 42)
    assert result == 1
    assert isinstance(result, int)

from solution import count_X as _case4_count_X

def test_count_string_elements():
    """Test counting string elements in a tuple."""
    result = _case4_count_X(('a', 'b', 'a', 'c', 'a'), 'a')
    assert result == 3
    assert isinstance(result, int)

from solution import count_X as _case5_count_X

def test_count_first_last_element():
    """Test when the target element is at the first and last positions."""
    result = _case5_count_X('x', 'x')
    assert result == 1
    assert isinstance(result, int)
    result2 = _case5_count_X(('x', 1, 2, 3, 'x'), 'x')
    assert result2 == 2
