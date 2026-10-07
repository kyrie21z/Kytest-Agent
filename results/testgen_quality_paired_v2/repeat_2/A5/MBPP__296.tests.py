# Accepted by submit_tests; explanations in testgen_report.json.

def test_empty_array():
    from solution import get_Inv_Count
    result = get_Inv_Count([])
    assert result == 0
    assert isinstance(result, int), 'Return type should be int'

def test_single_element():
    from solution import get_Inv_Count
    result = get_Inv_Count([42])
    assert result == 0
    assert isinstance(result, int), 'Return type should be int'

def test_sorted_array():
    from solution import get_Inv_Count
    result = get_Inv_Count([1, 2, 3, 4, 5])
    assert result == 0
    assert isinstance(result, int), 'Return type should be int'

def test_reverse_sorted():
    from solution import get_Inv_Count
    arr = [5, 4, 3, 2, 1]
    n = len(arr)
    expected = n * (n - 1) // 2
    result = get_Inv_Count(arr)
    assert result == expected
    assert isinstance(result, int), 'Return type should be int'

def test_two_elements_inverted():
    from solution import get_Inv_Count
    result = get_Inv_Count([2, 1])
    assert result == 1
    assert isinstance(result, int), 'Return type should be int'

def test_with_duplicates():
    from solution import get_Inv_Count
    result = get_Inv_Count([1, 3, 2, 3, 1])
    assert result == 4
    assert isinstance(result, int), 'Return type should be int'
