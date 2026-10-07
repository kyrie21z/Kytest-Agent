# Accepted by submit_tests; explanations in testgen_report.json.

"""Test comb_sort with an empty list."""
from solution import comb_sort as _case0_comb_sort

def test_empty_list():
    result = _case0_comb_sort([])
    assert result == []
    assert isinstance(result, list)

"""Test comb_sort with a single element."""
from solution import comb_sort as _case1_comb_sort

def test_single_element():
    result = _case1_comb_sort([42])
    assert result == [42]
    assert isinstance(result, list)

"""Test comb_sort swaps two out-of-order elements."""
from solution import comb_sort as _case2_comb_sort

def test_two_elements_swapped():
    result = _case2_comb_sort([2, 1])
    assert result == [1, 2]

"""Test comb_sort leaves an already-sorted list unchanged."""
from solution import comb_sort as _case3_comb_sort

def test_already_sorted():
    result = _case3_comb_sort([1, 2, 3, 4, 5])
    assert result == [1, 2, 3, 4, 5]

"""Test comb_sort handles duplicate values correctly."""
from solution import comb_sort as _case4_comb_sort

def test_with_duplicates():
    result = _case4_comb_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])
    assert result == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]

"""Test comb_sort modifies the input list in place and returns it."""
from solution import comb_sort as _case5_comb_sort

def test_in_place_modification():
    original = [8, 4, 1, 14, 7, 6, 2, 19, 3, 12]
    result = _case5_comb_sort(original)
    assert result is original
    assert result == [1, 2, 3, 4, 6, 7, 8, 12, 14, 19]

"""Test comb_sort handles negative numbers correctly."""
from solution import comb_sort as _case6_comb_sort

def test_negative_numbers():
    result = _case6_comb_sort([-3, -1, -4, -1, -5, 2, 0])
    assert result == [-5, -4, -3, -1, -1, 0, 2]

"""Test comb_sort fully reverses a descending list."""
from solution import comb_sort as _case7_comb_sort

def test_reverse_sorted():
    result = _case7_comb_sort([9, 7, 5, 3, 1])
    assert result == [1, 3, 5, 7, 9]

"""Test comb_sort with all identical elements."""
from solution import comb_sort as _case8_comb_sort

def test_all_same_elements():
    result = _case8_comb_sort([7, 7, 7, 7, 7])
    assert result == [7, 7, 7, 7, 7]

"""Test comb_sort when smallest element is at the last position."""
from solution import comb_sort as _case9_comb_sort

def test_smallest_at_end():
    result = _case9_comb_sort([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
    assert result == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

"""Test comb_sort always returns a list instance."""
from solution import comb_sort as _case10_comb_sort

def test_returns_list_type():
    result = _case10_comb_sort([5, 3, 1])
    assert isinstance(result, list)

"""Test comb_sort with two already-ordered elements."""
from solution import comb_sort as _case11_comb_sort

def test_two_elements_already_ordered():
    result = _case11_comb_sort([1, 2])
    assert result == [1, 2]
