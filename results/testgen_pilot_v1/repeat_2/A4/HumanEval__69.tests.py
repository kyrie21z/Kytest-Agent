# Accepted by submit_tests; explanations in testgen_report.json.

from solution import search as _case0_search

def test_docstring_example_1():
    """Test first example from docstring: search([4, 1, 2, 2, 3, 1]) == 2"""
    result = _case0_search([4, 1, 2, 2, 3, 1])
    assert result == 2

from solution import search as _case1_search

def test_docstring_example_2():
    """Test second example from docstring: search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3"""
    result = _case1_search([1, 2, 2, 3, 3, 3, 4, 4, 4])
    assert result == 3

from solution import search as _case2_search

def test_docstring_example_3():
    """Test third example from docstring: search([5, 5, 4, 4, 4]) == -1"""
    result = _case2_search([5, 5, 4, 4, 4])
    assert result == -1

from solution import search as _case3_search

def test_single_element_one():
    """A single [1]: freq of 1 is 1, 1>=1, so answer is 1."""
    result = _case3_search([1])
    assert result == 1
    assert isinstance(result, int)

from solution import search as _case4_search

def test_single_element_two():
    """A single [2]: freq of 2 is 1, 1<2, so answer is -1."""
    result = _case4_search([2])
    assert result == -1
    assert isinstance(result, int)

from solution import search as _case5_search

def test_boundary_equal_freq():
    """Exact equality boundary: [3, 3, 3] -> freq=3, value=3, 3>=3 qualifies, answer=3.
     [3, 3] -> freq=2, value=3, 2<3 fails, answer=-1."""
    assert _case5_search([3, 3, 3]) == 3
    assert _case5_search([3, 3]) == -1
