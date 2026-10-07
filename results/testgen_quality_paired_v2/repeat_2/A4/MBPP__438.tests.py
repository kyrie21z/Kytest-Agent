# Accepted by submit_tests; explanations in testgen_report.json.

from solution import count_bidirectional as _case0_count_bidirectional

def test_empty_list():
    """Test with empty list returns 0."""
    result = _case0_count_bidirectional([])
    assert result == 0
    assert isinstance(result, int)

from solution import count_bidirectional as _case1_count_bidirectional

def test_single_element():
    """Test with a single-element list returns 0."""
    result = _case1_count_bidirectional([(1, 2)])
    assert result == 0
    assert isinstance(result, int)

from solution import count_bidirectional as _case2_count_bidirectional

def test_basic_bidirectional_pairs():
    """Test counting pairs where t2[0] == t1[1].
    
    Actual logic: for each pair (t1, t2), check t2[0] == t1[1].
    
    List: [(1, 2), (2, 3), (3, 4)]
    Pairs:
      ((1,2), (2,3)): t2[0]=2 == t1[1]=2 -> YES
      ((1,2), (3,4)): t2[0]=3 != t1[1]=2 -> NO
      ((2,3), (3,4)): t2[0]=3 == t1[1]=3 -> YES
    Expected: 2
    """
    result = _case2_count_bidirectional([(1, 2), (2, 3), (3, 4)])
    assert result == 2
    assert isinstance(result, int)

from solution import count_bidirectional as _case3_count_bidirectional

def test_symmetric_tuples():
    """Test with symmetric tuples (a, a).
    
    List: [(1, 1), (2, 2), (3, 3)]
    Pairs:
      ((1,1), (2,2)): t2[0]=2 == t1[1]=1? NO
      ((1,1), (3,3)): t2[0]=3 == t1[1]=1? NO
      ((2,2), (3,3)): t2[0]=3 == t1[1]=2? NO
    Expected: 0
    
    Even though tuples are symmetric, t2[0] never equals t1[1] here.
    """
    result = _case3_count_bidirectional([(1, 1), (2, 2), (3, 3)])
    assert result == 0
    assert isinstance(result, int)

from solution import count_bidirectional as _case4_count_bidirectional

def test_mixed_matching_and_nonmatching():
    """Test with mix of matching and non-matching pairs.
    
    List: [(1, 2), (2, 1), (3, 4)]
    Pairs:
      ((1,2), (2,1)): t2[0]=2 == t1[1]=2 -> YES
      ((1,2), (3,4)): t2[0]=3 == t1[1]=2? NO
      ((2,1), (3,4)): t2[0]=3 == t1[1]=1? NO
    Expected: 1
    """
    result = _case4_count_bidirectional([(1, 2), (2, 1), (3, 4)])
    assert result == 1
    assert isinstance(result, int)

from solution import count_bidirectional as _case5_count_bidirectional

def test_return_type_is_int():
    """Verify return type is always int regardless of input."""
    result = _case5_count_bidirectional([(5, 6), (6, 7), (7, 8), (8, 9)])
    assert isinstance(result, int)
    assert not isinstance(result, bool)
    large_list = [(i, i + 1) for i in range(100)]
    result2 = _case5_count_bidirectional(large_list)
    assert isinstance(result2, int)
    assert result2 >= 0
