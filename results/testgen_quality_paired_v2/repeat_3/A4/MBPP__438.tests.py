# Accepted by submit_tests; explanations in testgen_report.json.

def test_empty_list():
    from solution import count_bidirectional
    result = count_bidirectional([])
    assert isinstance(result, int), 'return type must be int'
    assert result == 0, 'empty list has no pairs'

def test_single_tuple():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 2)])
    assert isinstance(result, int), 'return type must be int'
    assert result == 0, 'single tuple cannot form a pair'

def test_true_bidirectional_pair():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 2), (2, 1)])
    assert isinstance(result, int), 'return type must be int'
    assert result == 1, 'exactly one bidirectional pair exists'

def test_multiple_bidirectional_pairs():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 2), (2, 1), (3, 4), (4, 3), (5, 6), (6, 5)])
    assert isinstance(result, int), 'return type must be int'
    assert result == 3, 'three independent bidirectional pairs exist'

def test_mixed_valid_and_invalid():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 2), (2, 1), (3, 4), (4, 3)])
    assert isinstance(result, int), 'return type must be int'
    assert result == 2, 'two valid bidirectional pairs among mixed input'
