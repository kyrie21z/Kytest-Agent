# Accepted by submit_tests; explanations in testgen_report.json.

import pytest as _case0_pytest
from solution import comb_sort as _case0_comb_sort

def test_empty_list():
    """comb_sort on an empty list should return an empty list."""
    nums = []
    result = _case0_comb_sort(nums)
    assert result == []
    assert isinstance(result, list)

import pytest as _case1_pytest
from solution import comb_sort as _case1_comb_sort

def test_single_element():
    """comb_sort on a single-element list should return that element unchanged."""
    nums = [42]
    result = _case1_comb_sort(nums)
    assert result == [42]
    assert len(result) == 1

import pytest as _case2_pytest
from solution import comb_sort as _case2_comb_sort

def test_already_sorted():
    """comb_sort on an already-sorted list should return the same sorted order."""
    nums = [1, 2, 3, 4, 5]
    result = _case2_comb_sort(nums)
    assert result == [1, 2, 3, 4, 5]

import pytest as _case3_pytest
from solution import comb_sort as _case3_comb_sort

def test_reverse_sorted():
    """comb_sort on a reverse-sorted list should produce ascending order."""
    nums = [5, 4, 3, 2, 1]
    result = _case3_comb_sort(nums)
    assert result == [1, 2, 3, 4, 5]

import pytest as _case4_pytest
from solution import comb_sort as _case4_comb_sort

def test_with_duplicates():
    """comb_sort should preserve all duplicate values in sorted order."""
    nums = [3, 1, 3, 2, 1]
    result = _case4_comb_sort(nums)
    assert result == [1, 1, 2, 3, 3]

import pytest as _case5_pytest
from solution import comb_sort as _case5_comb_sort

def test_in_place_modification():
    """comb_sort must modify the original list in-place (same object reference)."""
    nums = [3, 1, 2]
    result = _case5_comb_sort(nums)
    assert result is nums

import pytest as _case6_pytest
from solution import comb_sort as _case6_comb_sort

def test_negative_numbers():
    """comb_sort should correctly sort lists containing negative numbers."""
    nums = [-5, 3, -1, 0, 2]
    result = _case6_comb_sort(nums)
    assert result == [-5, -1, 0, 2, 3]

import pytest as _case7_pytest
from solution import comb_sort as _case7_comb_sort

def test_two_elements_unsorted():
    """comb_sort on two unsorted elements should swap them into order."""
    nums = [2, 1]
    result = _case7_comb_sort(nums)
    assert result == [1, 2]

import pytest as _case8_pytest
from solution import comb_sort as _case8_comb_sort

def test_all_same_elements():
    """comb_sort on a list of identical elements should return unchanged list."""
    nums = [7, 7, 7, 7]
    result = _case8_comb_sort(nums)
    assert result == [7, 7, 7, 7]

import pytest as _case9_pytest
from solution import comb_sort as _case9_comb_sort

def test_larger_random_input():
    """comb_sort should correctly sort a moderately sized list with varied values."""
    nums = [42, 17, 99, 3, 55, 8, 71, 23, 66, 1, 88, 34, 5, 47, 91, 12, 60, 29, 78, 44]
    result = _case9_comb_sort(nums)
    expected = sorted([42, 17, 99, 3, 55, 8, 71, 23, 66, 1, 88, 34, 5, 47, 91, 12, 60, 29, 78, 44])
    assert result == expected
