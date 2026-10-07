# Accepted by submit_tests; explanations in testgen_report.json.

def test_empty_list():
    from solution import is_Monotonic
    result = is_Monotonic([])
    assert result is True
    assert isinstance(result, bool)

def test_single_element():
    from solution import is_Monotonic
    result = is_Monotonic([42])
    assert result is True
    assert isinstance(result, bool)

def test_strictly_increasing():
    from solution import is_Monotonic
    result = is_Monotonic([1, 2, 3, 4])
    assert result is True
    assert isinstance(result, bool)

def test_strictly_decreasing():
    from solution import is_Monotonic
    result = is_Monotonic([5, 3, 1])
    assert result is True
    assert isinstance(result, bool)

def test_not_monotonic():
    from solution import is_Monotonic
    result = is_Monotonic([1, 3, 2])
    assert result is False
    assert isinstance(result, bool)

def test_constant_array():
    from solution import is_Monotonic
    result = is_Monotonic([7, 7, 7, 7])
    assert result is True
    assert isinstance(result, bool)
