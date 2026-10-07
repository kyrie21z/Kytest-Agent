# Accepted by submit_tests; explanations in testgen_report.json.

import solution as _case0_solution

def test_empty_list():
    nums = []
    result = _case0_solution.comb_sort(nums)
    assert result == []
    assert result is nums

import solution as _case1_solution

def test_single_element():
    nums = [42]
    result = _case1_solution.comb_sort(nums)
    assert result == [42]
    assert result is nums

import solution as _case2_solution

def test_already_sorted():
    nums = [1, 2, 3, 4, 5]
    result = _case2_solution.comb_sort(nums)
    assert result == [1, 2, 3, 4, 5]
    assert result is nums

import solution as _case3_solution

def test_unsorted_basic():
    nums = [5, 3, 1, 4, 2]
    result = _case3_solution.comb_sort(nums)
    assert result == [1, 2, 3, 4, 5]
    assert result is nums

import solution as _case4_solution

def test_with_duplicates():
    nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    result = _case4_solution.comb_sort(nums)
    assert result == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]
    assert len(result) == len(nums)
    assert result is nums

import solution as _case5_solution

def test_negative_numbers():
    nums = [-3, -1, -4, -1, -5]
    result = _case5_solution.comb_sort(nums)
    assert result == [-5, -4, -3, -1, -1]
    assert result is nums
