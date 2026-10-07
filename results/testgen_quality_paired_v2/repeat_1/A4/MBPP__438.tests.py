# Accepted by submit_tests; explanations in testgen_report.json.

def test_empty_list():
    from solution import count_bidirectional
    assert count_bidirectional([]) == 0

def test_single_tuple():
    from solution import count_bidirectional
    assert count_bidirectional([(1, 2)]) == 0

def test_true_bidirectional_pair():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 2), (2, 1)])
    assert result == 1

def test_asymmetric_nonpair():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 2), (3, 4)])
    assert result == 0

def test_multiple_pairs_count():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 2), (2, 1), (3, 4)])
    assert result == 1

def test_same_element_tuples():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 1), (1, 1)])
    assert result == 1

def test_return_type_int():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 2), (2, 1)])
    assert isinstance(result, int)
    assert not isinstance(result, bool)

def test_no_matching_elements():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 2), (3, 4), (5, 6)])
    assert result == 0

def test_three_bidirectional_pairs():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 2), (2, 1), (3, 4), (4, 3), (5, 6), (6, 5)])
    assert result == 3

def test_identical_tuples_not_counted():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 2), (1, 2)])
    assert result == 0

def test_duplicate_bidirectional_pairs():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 2), (2, 1), (3, 4), (4, 3)])
    assert result == 2

def test_self_reverse_tuple():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 1), (1, 1)])
    assert result == 1

def test_strings_as_elements():
    from solution import count_bidirectional
    result = count_bidirectional([('a', 'b'), ('b', 'a')])
    assert result == 1

def test_negative_numbers():
    from solution import count_bidirectional
    result = count_bidirectional([(-1, -2), (-2, -1)])
    assert result == 1

def test_mixed_positive_negative():
    from solution import count_bidirectional
    result = count_bidirectional([(1, -1), (-1, 1)])
    assert result == 1

def test_large_count():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 2), (2, 1), (3, 4), (4, 3), (5, 6), (6, 5)])
    assert result == 3

def test_zero_elements():
    from solution import count_bidirectional
    result = count_bidirectional([(0, 0), (0, 0)])
    assert result == 1
