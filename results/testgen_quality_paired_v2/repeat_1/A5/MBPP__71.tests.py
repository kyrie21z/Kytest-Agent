# Accepted by submit_tests; explanations in testgen_report.json.

def test_comb_sort_basic():
    """Write a function to sort a list of elements."""
    from solution import comb_sort
    nums = [8, 4, 1, 56, 3, -44, 23, -6, 28, 0]
    expected = [-44, -6, 0, 1, 3, 4, 8, 23, 28, 56]
    result = comb_sort(nums)
    assert result == expected
    assert isinstance(result, list)

def test_comb_sort_empty():
    """Write a function to sort a list of elements."""
    from solution import comb_sort
    nums = []
    result = comb_sort(nums)
    assert result == []
    assert isinstance(result, list)

def test_comb_sort_single_element():
    """Write a function to sort a list of elements."""
    from solution import comb_sort
    nums = [42]
    result = comb_sort(nums)
    assert result == [42]
    assert isinstance(result, list)

def test_comb_sort_already_sorted():
    """Write a function to sort a list of elements."""
    from solution import comb_sort
    nums = [1, 2, 3, 4, 5]
    result = comb_sort(nums)
    assert result == [1, 2, 3, 4, 5]
    assert result is nums

def test_comb_sort_reverse_sorted():
    """Write a function to sort a list of elements."""
    from solution import comb_sort
    nums = [5, 4, 3, 2, 1]
    result = comb_sort(nums)
    assert result == [1, 2, 3, 4, 5]

def test_comb_sort_duplicates():
    """Write a function to sort a list of elements."""
    from solution import comb_sort
    nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    result = comb_sort(nums)
    assert result == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    assert len(result) == len(nums)

def test_comb_sort_all_identical():
    """Write a function to sort a list of elements."""
    from solution import comb_sort
    nums = [7, 7, 7, 7, 7]
    result = comb_sort(nums)
    assert result == [7, 7, 7, 7, 7]
    assert len(result) == len(nums)

def test_comb_sort_larger_list():
    """Write a function to sort a list of elements."""
    from solution import comb_sort
    nums = [99, 12, 88, 3, 67, 45, 21, 76, 54, 33, 11, 90, 5, 78, 29]
    expected = [3, 5, 11, 12, 21, 29, 33, 45, 54, 67, 76, 78, 88, 90, 99]
    result = comb_sort(nums)
    assert result == expected
    assert len(result) == len(nums)
