# Accepted by submit_tests; explanations in testgen_report.json.

from solution import search as _case0_search

def test_basic_example_1():
    """Test the first docstring example."""
    assert _case0_search([4, 1, 2, 2, 3, 1]) == 2

from solution import search as _case1_search

def test_basic_example_2():
    """Test the second docstring example."""
    assert _case1_search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3

from solution import search as _case2_search

def test_no_qualifying_element():
    """Test when no element satisfies the condition."""
    assert _case2_search([5, 5, 4, 4, 4]) == -1

from solution import search as _case3_search

def test_single_element_qualifies():
    """Test single-element list where the element qualifies."""
    assert _case3_search([1]) == 1

from solution import search as _case4_search

def test_single_element_does_not_qualify():
    """Test single-element list where the element does not qualify."""
    assert _case4_search([2]) == -1

from solution import search as _case5_search

def test_exact_boundary_frequency():
    """Test where frequency exactly equals the value (boundary condition)."""
    assert _case5_search([3, 3, 3]) == 3
