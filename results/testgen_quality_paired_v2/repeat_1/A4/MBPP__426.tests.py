# Accepted by submit_tests; explanations in testgen_report.json.

def test_basic_mixed():
    from solution import filter_oddnumbers
    result = filter_oddnumbers([1, 2, 3, 4, 5])
    assert result == [1, 3, 5]

def test_all_even():
    from solution import filter_oddnumbers
    result = filter_oddnumbers([2, 4, 6, 8])
    assert result == []

def test_empty_input():
    from solution import filter_oddnumbers
    result = filter_oddnumbers([])
    assert result == []

def test_negative_numbers():
    from solution import filter_oddnumbers
    result = filter_oddnumbers([-3, -2, -1, 0, 2])
    assert result == [-3, -1]

def test_return_type():
    from solution import filter_oddnumbers
    result = filter_oddnumbers([1, 2, 3])
    assert isinstance(result, list)

def test_single_elements():
    from solution import filter_oddnumbers
    assert filter_oddnumbers([7]) == [7]
    assert filter_oddnumbers([8]) == []
