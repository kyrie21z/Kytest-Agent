# Accepted by submit_tests; explanations in testgen_report.json.

from solution import sorted_list_sum as _case0_sorted_list_sum

def test_empty_list():
    """An empty list should return an empty list since there are no elements to filter."""
    result = _case0_sorted_list_sum([])
    assert result == []
    assert isinstance(result, list)

from solution import sorted_list_sum as _case1_sorted_list_sum

def test_all_odd_lengths():
    """When every string has odd length, all are removed, yielding an empty list."""
    result = _case1_sorted_list_sum(['a', 'abc', 'hello'])
    assert result == []
    assert isinstance(result, list)

from solution import sorted_list_sum as _case2_sorted_list_sum

def test_basic_filter_and_sort_by_length():
    """Even-length strings are kept and sorted by ascending length.
    From the docstring example: sorted_list_sum(['aa', 'a', 'aaa']) => ['aa']"""
    result = _case2_sorted_list_sum(['aa', 'a', 'aaa'])
    assert result == ['aa']
    assert isinstance(result, list)

from solution import sorted_list_sum as _case3_sorted_list_sum

def test_alphabetical_tiebreak():
    """Strings of equal even length should be sorted alphabetically.
    Docstring example: sorted_list_sum(['ab', 'a', 'aaa', 'cd']) => ['ab', 'cd']"""
    result = _case3_sorted_list_sum(['ab', 'a', 'aaa', 'cd'])
    assert result == ['ab', 'cd']
    assert result.index('ab') < result.index('cd')

from solution import sorted_list_sum as _case4_sorted_list_sum

def test_mixed_lengths_with_duplicates():
    """Duplicates are preserved per the contract. Mixed lengths test: even-length items sorted by length then alphabetically."""
    result = _case4_sorted_list_sum(['bb', 'aa', 'cc', 'a', 'dddd', 'eee'])
    assert result == ['aa', 'bb', 'cc', 'dddd']
    assert isinstance(result, list)

from solution import sorted_list_sum as _case5_sorted_list_sum

def test_single_even_element():
    """A single even-length string should be returned as-is in a list."""
    result = _case5_sorted_list_sum(['ab'])
    assert result == ['ab']
    assert isinstance(result, list)
    assert len(result) == 1
