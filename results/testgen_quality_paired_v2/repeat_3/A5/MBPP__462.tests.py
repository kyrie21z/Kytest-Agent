# Accepted by submit_tests; explanations in testgen_report.json.

from solution import combinations_list as _case0_combinations_list

def test_empty_input():
    '''Docstring quote: "Write a function to find all possible combinations of the elements of a given list."'''
    result = _case0_combinations_list([])
    assert isinstance(result, list), 'Return value must be a list'
    assert len(result) == 1, 'Empty input should yield exactly 1 combination'
    assert result == [[]], 'The sole combination of an empty list is the empty list'

from solution import combinations_list as _case1_combinations_list

def test_single_element():
    '''Docstring quote: "Write a function to find all possible combinations of the elements of a given list."'''
    result = _case1_combinations_list([42])
    assert isinstance(result, list), 'Return value must be a list'
    assert len(result) == 2, 'Single element yields 2 combinations'
    assert [] in result, 'Empty subset must be present'
    assert [42] in result, 'Singleton subset must be present'

from solution import combinations_list as _case2_combinations_list

def test_duplicate_elements_treated_as_distinct_positions():
    '''Docstring quote: "Write a function to find all possible combinations of the elements of a given list."'''
    result = _case2_combinations_list([1, 1])
    assert len(result) == 4, 'Two positions yield 4 combinations even if values are equal'
    tuples = sorted((tuple(c) for c in result))
    assert tuples.count((1,)) == 2, 'Duplicate-value subsets from different positions should both appear'
    assert tuples.count(()) == 1, 'Empty subset appears once'
    assert tuples.count((1, 1)) == 1, 'Full subset appears once'

from solution import combinations_list as _case3_combinations_list

def test_mutation_M1_base_case_single_element():
    '''Docstring quote: "Write a function to find all possible combinations of the elements of a given list."'''
    result = _case3_combinations_list([99])
    assert len(result) == 2, 'Single element must produce 2 subsets, not 1 (catches M1: base case shift)'
    assert [] in result and [99] in result, 'Both empty and singleton subsets must be present'
