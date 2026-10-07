# Accepted by submit_tests; explanations in testgen_report.json.

def test_empty_list():
    """Empty input should return 0."""
    from solution import count_bidirectional
    assert count_bidirectional([]) == 0

def test_single_tuple():
    """A single tuple has no pairs, so result must be 0."""
    from solution import count_bidirectional
    assert count_bidirectional([(1, 2)]) == 0

def test_one_match_simple():
    """(1,2) and (2,1): first of second (2) == second of first (2) => match."""
    from solution import count_bidirectional
    assert count_bidirectional([(1, 2), (2, 1)]) == 1

def test_no_match():
    """(1,2) and (3,4): first of second (3) != second of first (2) => no match."""
    from solution import count_bidirectional
    assert count_bidirectional([(1, 2), (3, 4)]) == 0

def test_same_tuple_twice():
    """(1,2) and (1,2): first of second (1) != second of first (2) => no match."""
    from solution import count_bidirectional
    assert count_bidirectional([(1, 2), (1, 2)]) == 0

def test_two_independent_matches():
    """Two separate matching pairs each contribute 1."""
    from solution import count_bidirectional
    assert count_bidirectional([(1, 2), (2, 1), (3, 4), (4, 3)]) == 2

def test_self_equal_single():
    """A single self-equal tuple [(1,1)] has no distinct pairs; original code yields 0."""
    from solution import count_bidirectional
    assert count_bidirectional([(1, 1)]) == 0

def test_self_equal_in_list():
    """[(1,1),(2,3)]: no cross-pair matches; original returns 0."""
    from solution import count_bidirectional
    assert count_bidirectional([(1, 1), (2, 3)]) == 0

def test_all_self_equal_tuples():
    """[(1,1),(2,2),(3,3)]: no cross-pair matches; original returns 0."""
    from solution import count_bidirectional
    assert count_bidirectional([(1, 1), (2, 2), (3, 3)]) == 0

def test_chain_of_three():
    """(1,2),(2,3),(3,1): pairs (0,1) match (2==2), (1,2) match (3==3), (0,2) no => 2."""
    from solution import count_bidirectional
    assert count_bidirectional([(1, 2), (2, 3), (3, 1)]) == 2

def test_larger_list():
    """Five tuples in a cycle: (1,2),(2,3),(3,4),(4,5),(5,1). Exactly 4 matches."""
    from solution import count_bidirectional
    assert count_bidirectional([(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]) == 4
