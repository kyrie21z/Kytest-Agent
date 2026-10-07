# Accepted by submit_tests; explanations in testgen_report.json.

from solution import count_bidirectional as _case0_count_bidirectional

def test_empty_list():
    """Contract: count bidirectional tuple pairs.
     Input domain: any list of tuples (including empty).
     Oracle: an empty list contains no pairs, so the result must be 0."""
    result = _case0_count_bidirectional([])
    assert isinstance(result, int)
    assert result == 0

from solution import count_bidirectional as _case1_count_bidirectional

def test_single_tuple():
    """Contract: count bidirectional tuple pairs.
     Input domain: list containing exactly one tuple.
     Oracle: with only one tuple there is no pair to compare, so result is 0."""
    result = _case1_count_bidirectional([(1, 2)])
    assert isinstance(result, int)
    assert result == 0

from solution import count_bidirectional as _case2_count_bidirectional

def test_one_bidirectional_pair():
    """Contract: count bidirectional tuple pairs.
     Input domain: list of two tuples that are reverses of each other.
     Oracle: (1,2) and (2,1) are bidirectional — exactly one such pair exists."""
    result = _case2_count_bidirectional([(1, 2), (2, 1)])
    assert isinstance(result, int)
    assert result == 1

from solution import count_bidirectional as _case3_count_bidirectional

def test_no_bidirectional_pairs():
    """Contract: count bidirectional tuple pairs.
     Input domain: list of tuples where none are reverses of each other.
     Oracle: (1,2) and (3,4) share no reversal relationship, so result is 0."""
    result = _case3_count_bidirectional([(1, 2), (3, 4)])
    assert isinstance(result, int)
    assert result == 0

from solution import count_bidirectional as _case4_count_bidirectional

def test_multiple_bidirectional_pairs():
    """Contract: count bidirectional tuple pairs.
     Input domain: list with two independent bidirectional pairs.
     Oracle: (1,2)<->(2,1) and (3,4)<->(4,3) give exactly 2 pairs."""
    result = _case4_count_bidirectional([(1, 2), (2, 1), (3, 4), (4, 3)])
    assert isinstance(result, int)
    assert result == 2

from solution import count_bidirectional as _case5_count_bidirectional

def test_self_comparison_m4_kill():
    """Contract: count bidirectional tuple pairs.
     Input domain: list with a single tuple whose elements are equal.
     Oracle: [(1,1)] has no pairs to compare; result must be 0.
     M4 mutant changes range(idx+1,...) to range(idx+0,...), causing self-comparison.
     Self-compare (1,1): condition checks 1==1 → True, so M4 returns 1 instead of 0."""
    result = _case5_count_bidirectional([(1, 1)])
    assert isinstance(result, int)
    assert result == 0
