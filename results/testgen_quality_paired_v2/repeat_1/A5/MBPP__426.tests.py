# Accepted by submit_tests; explanations in testgen_report.json.

import solution as _case0_solution

def test_basic_mixed():
    """Test filtering a list with mixed even and odd numbers.
    Contract says "filter odd numbers" — given [1,2,3,4,5],
    odds are 1,3,5 in original order. Even numbers 2,4 removed."""
    result = _case0_solution.filter_oddnumbers([1, 2, 3, 4, 5])
    assert result == [1, 3, 5]

import solution as _case1_solution

def test_empty_input():
    """Test with empty list. An empty iterable has no odd numbers,
    so the result must be an empty list."""
    result = _case1_solution.filter_oddnumbers([])
    assert result == []
    assert isinstance(result, list)

import solution as _case2_solution

def test_all_even():
    """When every element is even, none satisfy x%2 != 0,
    so the output must be an empty list."""
    result = _case2_solution.filter_oddnumbers([2, 4, 6, 8, 10])
    assert result == []
    assert len(result) == 0

import solution as _case3_solution

def test_all_odd():
    """When every element is odd, all satisfy x%2 != 0,
    so the output must equal the input list."""
    result = _case3_solution.filter_oddnumbers([1, 3, 5, 7])
    assert result == [1, 3, 5, 7]
    assert len(result) == len([1, 3, 5, 7])

import solution as _case4_solution

def test_negative_numbers():
    """Negative odd numbers like -3, -1 also satisfy x%2 != 0.
    Negative evens like -2, -4 should be excluded."""
    result = _case4_solution.filter_oddnumbers([-3, -2, -1, 0, 1, 2])
    assert result == [-3, -1, 1]

import solution as _case5_solution

def test_single_elements_and_zero():
    """Boundary cases: single odd element returns itself;
    single even element returns []; zero is even."""
    assert _case5_solution.filter_oddnumbers([3]) == [3]
    assert _case5_solution.filter_oddnumbers([4]) == []
    assert _case5_solution.filter_oddnumbers([0]) == []
    assert isinstance(_case5_solution.filter_oddnumbers([3]), list)
