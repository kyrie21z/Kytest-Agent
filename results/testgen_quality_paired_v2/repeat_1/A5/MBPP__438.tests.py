# Accepted by submit_tests; explanations in testgen_report.json.

def test_empty_list():
    from solution import count_bidirectional
    assert count_bidirectional([]) == 0

def test_true_bidirectional_pair():
    from solution import count_bidirectional
    assert count_bidirectional([(1, 2), (2, 1)]) == 1

def test_no_match():
    from solution import count_bidirectional
    assert count_bidirectional([(1, 2), (3, 4)]) == 0

def test_multiple_pairs():
    from solution import count_bidirectional
    result = count_bidirectional([(1, 2), (2, 1), (3, 4), (4, 3)])
    assert result == 2

def test_duplicate_tuples():
    from solution import count_bidirectional
    assert count_bidirectional([(1, 1), (1, 1)]) == 1
