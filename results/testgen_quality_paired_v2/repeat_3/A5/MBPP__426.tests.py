# Accepted by submit_tests; explanations in testgen_report.json.

from solution import filter_oddnumbers as _case0_filter_oddnumbers

def test_basic_mixed():
    """Test filtering a list with mixed odd and even numbers."""
    result = _case0_filter_oddnumbers([1, 2, 3, 4, 5])
    assert result == [1, 3, 5]

from solution import filter_oddnumbers as _case1_filter_oddnumbers

def test_all_even():
    """Test when all inputs are even numbers — result should be empty."""
    result = _case1_filter_oddnumbers([2, 4, 6, 8, 10])
    assert result == []

from solution import filter_oddnumbers as _case2_filter_oddnumbers

def test_empty_input():
    """Test with an empty list — should return an empty list."""
    result = _case2_filter_oddnumbers([])
    assert result == []

from solution import filter_oddnumbers as _case3_filter_oddnumbers

def test_negative_odds():
    """Test that negative odd numbers are correctly identified as odd."""
    result = _case3_filter_oddnumbers([-3, -2, -1, 0, 2, 5])
    assert result == [-3, -1, 5]

from solution import filter_oddnumbers as _case4_filter_oddnumbers

def test_return_type_and_order():
    """Verify the return value is a list and preserves original order of odd numbers."""
    result = _case4_filter_oddnumbers([10, 7, 4, 3, 8, 1])
    assert isinstance(result, list)
    assert result == [7, 3, 1]

from solution import filter_oddnumbers as _case5_filter_oddnumbers

def test_single_elements():
    """Test with single-element lists for both odd and even cases."""
    assert _case5_filter_oddnumbers([7]) == [7]
    assert _case5_filter_oddnumbers([8]) == []
