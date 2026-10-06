# Accepted by submit_tests; explanations in testgen_report.json.

from solution import search as _case0_search

def test_docstring_example_1():
    """search([4, 1, 2, 2, 3, 1]) == 2"""
    assert _case0_search([4, 1, 2, 2, 3, 1]) == 2

from solution import search as _case1_search

def test_docstring_example_2():
    """search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3"""
    assert _case1_search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3

from solution import search as _case2_search

def test_docstring_example_3():
    """search([5, 5, 4, 4, 4]) == -1"""
    assert _case2_search([5, 5, 4, 4, 4]) == -1

from solution import search as _case3_search

def test_single_element_qualifies():
    """search([1]) == 1"""
    assert _case3_search([1]) == 1

from solution import search as _case4_search

def test_exact_frequency_boundary():
    """search([3, 3, 3]) == 3"""
    assert _case4_search([3, 3, 3]) == 3

from solution import search as _case5_search

def test_multiple_candidates_picks_largest():
    """search([1, 1, 2, 2, 3, 3, 3]) == 3"""
    assert _case5_search([1, 1, 2, 2, 3, 3, 3]) == 3
