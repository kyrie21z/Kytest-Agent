# Accepted by submit_tests; explanations in testgen_report.json.

from solution import combinations_list as _case0_combinations_list

def test_empty_input():
    """Verify the base case: empty list returns a list containing one empty combination."""
    result = _case0_combinations_list([])
    assert isinstance(result, list), 'Return value must be a list'
    assert len(result) == 1, f'Expected 1 combination for empty input, got {len(result)}'
    assert result[0] == [], f'The single combination must be an empty list, got {result[0]}'

from solution import combinations_list as _case1_combinations_list

def test_single_element():
    """A single-element list should produce exactly two combinations: empty and itself."""
    result = _case1_combinations_list([42])
    assert isinstance(result, list), 'Return value must be a list'
    assert len(result) == 2, f'Expected 2 combinations, got {len(result)}'
    assert [] in result, 'Empty combination must be present'
    assert [42] in result, '[42] must be present'

from solution import combinations_list as _case2_combinations_list

def test_two_elements_count_and_completeness():
    """Two distinct elements yield 2^2 = 4 combinations covering all subsets."""
    result = _case2_combinations_list([1, 2])
    assert isinstance(result, list), 'Return value must be a list'
    assert len(result) == 4, f'Expected 4 combinations, got {len(result)}'
    assert [] in result, 'Empty combination missing'
    assert [1] in result, '[1] missing'
    assert [2] in result, '[2] missing'
    assert [2, 1] in result or [1, 2] in result, 'Full set combination missing'

from solution import combinations_list as _case3_combinations_list

def test_duplicates_preserved():
    """Duplicate values in input should produce duplicate-valued combinations."""
    result = _case3_combinations_list([1, 1])
    assert isinstance(result, list), 'Return value must be a list'
    assert len(result) == 4, f'Expected 4 combinations for [1,1], got {len(result)}'
    assert [] in result, 'Empty combination missing'
    assert [1] in result, '[1] missing'
    assert [1, 1] in result, '[1,1] missing'

from solution import combinations_list as _case4_combinations_list

def test_mixed_types_and_nested():
    """Function should handle mixed types and nested lists correctly."""
    inner = [9, 10]
    result = _case4_combinations_list(['x', 0, inner])
    assert isinstance(result, list), 'Return value must be a list'
    assert len(result) == 8, f'Expected 8 combinations, got {len(result)}'
    assert [] in result, 'Empty combination missing'
    assert ['x'] in result, "['x'] missing"
    assert [0] in result, '[0] missing'
    assert [inner] in result, f'[{inner}] missing'

from solution import combinations_list as _case5_combinations_list

def test_three_elements_power_of_two():
    """Three elements should produce 2^3 = 8 combinations."""
    result = _case5_combinations_list([1, 2, 3])
    assert isinstance(result, list), 'Return value must be a list'
    assert len(result) == 8, f'Expected 8 combinations, got {len(result)}'
    assert [1] in result, '[1] missing from power set'
    assert [2] in result, '[2] missing from power set'
    assert [3] in result, '[3] missing from power set'
