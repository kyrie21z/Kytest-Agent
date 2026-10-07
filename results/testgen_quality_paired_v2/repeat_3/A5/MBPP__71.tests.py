# Accepted by submit_tests; explanations in testgen_report.json.

def test_comb_sort_empty_list():
    from solution import comb_sort
    nums = []
    result = comb_sort(nums)
    assert result == []
    assert isinstance(result, list)

def test_comb_sort_single_element():
    from solution import comb_sort
    nums = [42]
    result = comb_sort(nums)
    assert result == [42]
    assert isinstance(result, list)

def test_comb_sort_already_sorted():
    from solution import comb_sort
    nums = [1, 2, 3, 4, 5]
    result = comb_sort(nums)
    assert result == [1, 2, 3, 4, 5]

def test_comb_sort_reverse_sorted():
    from solution import comb_sort
    nums = [5, 4, 3, 2, 1]
    result = comb_sort(nums)
    assert result == [1, 2, 3, 4, 5]

def test_comb_sort_with_duplicates():
    from solution import comb_sort
    nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    result = comb_sort(nums)
    expected = sorted([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])
    assert result == expected

def test_comb_sort_negative_numbers():
    from solution import comb_sort
    nums = [-3, -1, -4, -1, -5]
    result = comb_sort(nums)
    assert result == [-5, -4, -3, -1, -1]

def test_comb_sort_two_elements_unsorted():
    from solution import comb_sort
    nums = [2, 1]
    result = comb_sort(nums)
    assert result == [1, 2]

def test_comb_sort_all_same_elements():
    from solution import comb_sort
    nums = [7, 7, 7, 7]
    result = comb_sort(nums)
    assert result == [7, 7, 7, 7]

def test_comb_sort_mixed_positive_negative():
    from solution import comb_sort
    nums = [0, -1, 2, -3, 4]
    result = comb_sort(nums)
    assert result == [-3, -1, 0, 2, 4]

def test_comb_sort_larger_varied():
    from solution import comb_sort
    nums = [64, 34, 25, 12, 22, 11, 90, 1, 55, 43]
    result = comb_sort(nums)
    expected = sorted([64, 34, 25, 12, 22, 11, 90, 1, 55, 43])
    assert result == expected

def test_comb_sort_returns_list_type():
    from solution import comb_sort
    nums = [3, 1, 2]
    result = comb_sort(nums)
    assert isinstance(result, list)
