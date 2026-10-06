# Accepted by submit_tests; explanations in testgen_report.json.

from solution import search as _case0_search

def test_basic_example_1():
    """Test first docstring example: mixed list with multiple candidates."""
    assert _case0_search([4, 1, 2, 2, 3, 1]) == 2

from solution import search as _case1_search

def test_basic_example_2():
    """Test second docstring example: ascending counts with boundary at 4."""
    assert _case1_search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3

from solution import search as _case2_search

def test_basic_example_3():
    """Test third docstring example: no valid candidate returns -1."""
    assert _case2_search([5, 5, 4, 4, 4]) == -1

from solution import search as _case3_search

def test_single_element_valid():
    """Test minimum valid input: single element equal to 1."""
    assert _case3_search([1]) == 1

from solution import search as _case4_search

def test_single_element_invalid():
    """Test single element that cannot satisfy the condition."""
    assert _case4_search([2]) == -1

from solution import search as _case5_search

def test_frequency_equals_value_boundary():
    """Test exact boundary: frequency equals value for multiple candidates."""
    assert _case5_search([1, 1, 1, 2, 2, 3]) == 2
