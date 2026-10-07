# Accepted by submit_tests; explanations in testgen_report.json.

def test_basic_sort():
    from solution import pancake_sort
    result = pancake_sort([3, 1, 4, 1, 5, 9, 2, 6])
    assert result == [1, 1, 2, 3, 4, 5, 6, 9]

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

def test_two_elements():
    from solution import pancake_sort
    result = pancake_sort([2, 1])
    assert result == [1, 2]
