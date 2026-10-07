# Accepted by submit_tests; explanations in testgen_report.json.

import solution as _case0_solution

def test_mixed_numbers():
    '''Verbatim docstring quote: "Write a function to filter odd numbers."'''
    result = _case0_solution.filter_oddnumbers([1, 2, 3, 4, 5, 6])
    assert result == [1, 3, 5]

import solution as _case1_solution

def test_all_even():
    '''Verbatim docstring quote: "Write a function to filter odd numbers."'''
    result = _case1_solution.filter_oddnumbers([2, 4, 6, 8, 10])
    assert result == []

import solution as _case2_solution

def test_empty_input():
    '''Verbatim docstring quote: "Write a function to filter odd numbers."'''
    result = _case2_solution.filter_oddnumbers([])
    assert result == []
    assert isinstance(result, list)

import solution as _case3_solution

def test_negative_odds():
    '''Verbatim docstring quote: "Write a function to filter odd numbers."'''
    result = _case3_solution.filter_oddnumbers([-3, -2, -1, 0, 1, 2, 3])
    assert result == [-3, -1, 1, 3]

import solution as _case4_solution

def test_return_type_check():
    '''Verbatim docstring quote: "Write a function to filter odd numbers."'''
    result = _case4_solution.filter_oddnumbers([1, 2, 3])
    assert isinstance(result, list)
    assert not isinstance(result, tuple)

import solution as _case5_solution

def test_single_elements():
    '''Verbatim docstring quote: "Write a function to filter odd numbers."'''
    assert _case5_solution.filter_oddnumbers([7]) == [7]
    assert _case5_solution.filter_oddnumbers([8]) == []
    assert _case5_solution.filter_oddnumbers([0]) == []
