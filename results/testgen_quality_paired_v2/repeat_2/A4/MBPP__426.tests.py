# Accepted by submit_tests; explanations in testgen_report.json.

def test_basic_odd_filtering():
    from solution import filter_oddnumbers
    result = filter_oddnumbers([1, 2, 3, 4, 5, 6])
    assert result == [1, 3, 5]

def test_all_even_numbers():
    from solution import filter_oddnumbers
    result = filter_oddnumbers([2, 4, 6, 8, 10])
    assert result == []

def test_all_odd_numbers():
    from solution import filter_oddnumbers
    result = filter_oddnumbers([1, 3, 5, 7, 9])
    assert result == [1, 3, 5, 7, 9]

def test_empty_list():
    from solution import filter_oddnumbers
    result = filter_oddnumbers([])
    assert result == []

def test_negative_numbers():
    from solution import filter_oddnumbers
    result = filter_oddnumbers([-3, -2, -1, 0, 1, 2])
    assert result == [-3, -1, 1]

def test_return_type_is_list():
    from solution import filter_oddnumbers
    result = filter_oddnumbers([1, 2, 3])
    assert isinstance(result, list)
