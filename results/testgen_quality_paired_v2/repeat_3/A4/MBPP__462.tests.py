# Accepted by submit_tests; explanations in testgen_report.json.

from solution import combinations_list as _case0_combinations_list

def test_empty_list():
    """Verify that an empty input list returns a list containing one empty subset."""
    result = _case0_combinations_list([])
    assert result == [[]]
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == []

from solution import combinations_list as _case1_combinations_list

def test_single_element():
    """Verify that a single-element list returns exactly two subsets: empty and the element itself."""
    result = _case1_combinations_list([42])
    assert isinstance(result, list)
    assert len(result) == 2
    assert [] in result
    assert [42] in result
    assert result == [[], [42]]

from solution import combinations_list as _case2_combinations_list

def test_duplicate_elements():
    """Verify behavior when the input contains duplicate values."""
    result = _case2_combinations_list([1, 1])
    assert isinstance(result, list)
    assert len(result) == 4
    expected = [[], [1], [1], [1, 1]]
    assert result == expected
    assert [1, 1] in result

from solution import combinations_list as _case3_combinations_list

def test_two_elements_exact():
    """Verify the exact output for [1, 2] matches the recursive construction."""
    result = _case3_combinations_list([1, 2])
    assert result == [[], [1], [2], [2, 1]]

from solution import combinations_list as _case4_combinations_list

def test_three_elements_exact():
    """Verify the exact output for [1, 2, 3] matches the recursive construction."""
    result = _case4_combinations_list([1, 2, 3])
    expected = [[], [1], [2], [2, 1], [3], [3, 1], [3, 2], [3, 2, 1]]
    assert result == expected

from solution import combinations_list as _case5_combinations_list

def test_mixed_types_exact():
    """Verify exact output for a mixed-type single-element list preserves types."""
    result = _case5_combinations_list(['a'])
    assert result == [[], ['a']]
    assert isinstance(result[0], list)
    assert isinstance(result[1], list)
    assert result[1][0] == 'a'
    assert isinstance(result[1][0], str)
