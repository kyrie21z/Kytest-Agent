# Accepted by submit_tests; explanations in testgen_report.json.

from solution import search as _case0_search

def test_basic_example():
    """Test the first example from the docstring."""
    assert _case0_search([4, 1, 2, 2, 3, 1]) == 2

from solution import search as _case1_search

def test_second_example():
    """Test the second example from the docstring."""
    assert _case1_search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3

from solution import search as _case2_search

def test_no_qualifying_element():
    """Test when no integer satisfies the condition."""
    assert _case2_search([5, 5, 4, 4, 4]) == -1

from solution import search as _case3_search

def test_single_qualifying():
    """Test single element that exactly meets the condition."""
    result = _case3_search([1])
    assert result == 1
    assert isinstance(result, int)

from solution import search as _case4_search

def test_single_non_qualifying():
    """Test single element that cannot satisfy the condition."""
    result = _case4_search([2])
    assert result == -1
    assert isinstance(result, int)

from solution import search as _case5_search

def test_multiple_candidates_picks_max():
    """Test that among multiple qualifying integers, the greatest is returned."""
    assert _case5_search([2, 2, 3, 3, 3]) == 3
