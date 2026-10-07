# Accepted by submit_tests; explanations in testgen_report.json.

"""Test empty input returns [[]]."""
from solution import combinations_list as _case0_combinations_list

def test_empty_list_returns_singleton_empty():
    """Verify the base-case contract: empty input yields [[]].
    Contract quote: "Write a function to find all possible combinations of the elements of a given list."
    Input domain: list1 = [] (empty list)
    Oracle: The only valid combination of zero elements is the empty set itself,
            represented as a list containing one empty list.
    Fault hypothesis: A buggy implementation might return [] (no combinations at all)
                      or [[[]]] (wrong nesting).
    """
    result = _case0_combinations_list([])
    assert isinstance(result, list), 'Result must be a list'
    assert len(result) == 1, f'Expected 1 combination for empty input, got {len(result)}'
    assert result[0] == [], f'Expected [[]], got {result}'

"""Test single-element input produces exactly two combinations."""
from solution import combinations_list as _case1_combinations_list

def test_single_element_two_combinations():
    """Verify single-element input produces exactly two combinations.
    Contract quote: "Write a function to find all possible combinations of the elements of a given list."
    Input domain: list1 = [42] (single element)
    Oracle: With one element there are 2^1 = 2 subsets: the empty set and the set
            containing that element.
    Fault hypothesis: Off-by-one returning only 1 or 3 items; wrong nesting.
    """
    result = _case1_combinations_list([42])
    assert isinstance(result, list), 'Result must be a list'
    assert len(result) == 2, f'Expected 2 combinations, got {len(result)}'
    assert result[0] == [], f'First combination should be [], got {result[0]}'
    assert result[1] == [42], f'Second combination should be [42], got {result[1]}'

"""Test three-element input yields 2^3 = 8 combinations."""
from solution import combinations_list as _case2_combinations_list

def test_three_elements_power_of_two():
    """Verify three-element input yields 2^3 = 8 combinations.
    Contract quote: "Write a function to find all possible combinations of the elements of a given list."
    Input domain: list1 = [1, 2, 3] (three distinct integers)
    Oracle: The power set of a 3-element set has size 2^3 = 8.
    Fault hypothesis: Missing branches in recursion yielding fewer than 8 results.
    """
    result = _case2_combinations_list([1, 2, 3])
    assert len(result) == 8, f'Expected 8 combinations for 3 elements, got {len(result)}'
