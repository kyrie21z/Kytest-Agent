# Accepted by submit_tests; explanations in testgen_report.json.

from solution import filter_oddnumbers as _case0_filter_oddnumbers

def test_filter_odd_basic():
    """Test basic filtering of odd numbers from a mixed list."""
    result = _case0_filter_oddnumbers([1, 2, 3, 4, 5])
    assert result == [1, 3, 5]

from solution import filter_oddnumbers as _case1_filter_oddnumbers

def test_filter_odd_empty():
    """Test that an empty list returns an empty list."""
    result = _case1_filter_oddnumbers([])
    assert result == []

from solution import filter_oddnumbers as _case2_filter_oddnumbers

def test_filter_odd_all_even():
    """Test when all elements are even — result should be empty."""
    result = _case2_filter_oddnumbers([2, 4, 6, 8, 10])
    assert result == []

from solution import filter_oddnumbers as _case3_filter_oddnumbers

def test_filter_odd_all_odd():
    """Test when all elements are odd — result should equal the input."""
    result = _case3_filter_oddnumbers([1, 3, 5, 7])
    assert result == [1, 3, 5, 7]

from solution import filter_oddnumbers as _case4_filter_oddnumbers

def test_filter_odd_negative():
    """Test filtering with negative numbers — negatives can also be odd."""
    result = _case4_filter_oddnumbers([-3, -2, -1, 0, 1, 2])
    assert result == [-3, -1, 1]

from solution import filter_oddnumbers as _case5_filter_oddnumbers

def test_filter_odd_return_type():
    """Verify the return value is always a list, not a filter object."""
    result = _case5_filter_oddnumbers([1, 2, 3])
    assert isinstance(result, list)
    assert isinstance(_case5_filter_oddnumbers([2]), list)
    assert isinstance(_case5_filter_oddnumbers([1]), list)
