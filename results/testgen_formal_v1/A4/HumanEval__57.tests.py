# Accepted by submit_tests; explanations in testgen_report.json.

from solution import monotonic as _case0_monotonic

def test_monotonic_increasing():
    """Test that a strictly increasing list returns True."""
    result = _case0_monotonic([1, 2, 4, 20])
    assert result is True

from solution import monotonic as _case1_monotonic

def test_monotonic_decreasing():
    """Test that a strictly decreasing list returns True."""
    result = _case1_monotonic([4, 1, 0, -10])
    assert result is True

from solution import monotonic as _case2_monotonic

def test_non_monotonic():
    """Test that a non-monotonic list returns False."""
    result = _case2_monotonic([1, 20, 4, 10])
    assert result is False

from solution import monotonic as _case3_monotonic

def test_empty_list():
    """Test that an empty list returns True (trivially monotonic)."""
    result = _case3_monotonic([])
    assert result is True

from solution import monotonic as _case4_monotonic

def test_single_element():
    """Test that a single-element list returns True (trivially monotonic)."""
    result = _case4_monotonic([42])
    assert result is True

from solution import monotonic as _case5_monotonic

def test_all_equal_elements():
    """Test that a list of all equal elements returns True (both non-decreasing and non-increasing)."""
    result = _case5_monotonic([5, 5, 5, 5])
    assert result is True
