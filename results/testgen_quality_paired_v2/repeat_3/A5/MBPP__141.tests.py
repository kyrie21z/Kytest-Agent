# Accepted by submit_tests; explanations in testgen_report.json.

def test_basic_unsorted():
    from solution import pancake_sort
    result = pancake_sort([3, 1, 2])
    assert result == [1, 2, 3]

def test_empty_list():
    from solution import pancake_sort
    result = pancake_sort([])
    assert result == []

def test_single_element():
    from solution import pancake_sort
    result = pancake_sort([42])
    assert result == [42]

def test_already_sorted():
    from solution import pancake_sort
    result = pancake_sort([1, 2, 3, 4, 5])
    assert result == [1, 2, 3, 4, 5]

def test_reverse_sorted():
    from solution import pancake_sort
    result = pancake_sort([5, 4, 3, 2, 1])
    assert result == [1, 2, 3, 4, 5]

def test_with_duplicates():
    from solution import pancake_sort
    result = pancake_sort([3, 1, 2, 1, 3])
    assert result == [1, 1, 2, 3, 3]

def test_negative_numbers():
    from solution import pancake_sort
    result = pancake_sort([-3, 5, -1, 0, 2])
    assert result == [-3, -1, 0, 2, 5]

def test_two_elements_swapped():
    from solution import pancake_sort
    result = pancake_sort([2, 1])
    assert result == [1, 2]

def test_all_same_elements():
    from solution import pancake_sort
    result = pancake_sort([7, 7, 7, 7])
    assert result == [7, 7, 7, 7]

def test_return_type_is_list():
    from solution import pancake_sort
    result = pancake_sort([3, 1, 2])
    assert isinstance(result, list)

def test_larger_reverse_sorted():
    from solution import pancake_sort
    result = pancake_sort([9, 8, 7, 6, 5, 4, 3, 2, 1])
    assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9]
