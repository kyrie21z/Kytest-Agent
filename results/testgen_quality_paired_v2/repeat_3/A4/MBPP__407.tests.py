# Accepted by submit_tests; explanations in testgen_report.json.

from solution import rearrange_bigger as _case0_rearrange_bigger

def test_simple_two_digits():
    """Test basic two-digit number where swapping gives next bigger."""
    assert _case0_rearrange_bigger(12) == 21

from solution import rearrange_bigger as _case1_rearrange_bigger

def test_descending_returns_false():
    """When digits are in descending order, no bigger rearrangement exists."""
    assert _case1_rearrange_bigger(4321) is False

from solution import rearrange_bigger as _case2_rearrange_bigger

def test_single_digit_returns_false():
    """A single digit has no other rearrangement."""
    assert _case2_rearrange_bigger(5) is False

from solution import rearrange_bigger as _case3_rearrange_bigger

def test_with_duplicates():
    """Test numbers with repeated digits."""
    assert _case3_rearrange_bigger(122) == 212
    assert _case3_rearrange_bigger(212) == 221

from solution import rearrange_bigger as _case4_rearrange_bigger

def test_return_type_int_or_bool():
    """Return value must be int when successful, False when impossible."""
    result1 = _case4_rearrange_bigger(12)
    assert isinstance(result1, int)
    result2 = _case4_rearrange_bigger(4321)
    assert result2 is False
    result3 = _case4_rearrange_bigger(5)
    assert result3 is False

from solution import rearrange_bigger as _case5_rearrange_bigger

def test_next_permutation_chain():
    """Verify consecutive calls produce the correct sequence of next permutations."""
    r1 = _case5_rearrange_bigger(1234)
    assert r1 == 1243
    r2 = _case5_rearrange_bigger(r1)
    assert r2 == 1324
    r3 = _case5_rearrange_bigger(r2)
    assert r3 == 1342
    r4 = _case5_rearrange_bigger(r3)
    assert r4 == 1423
    r5 = _case5_rearrange_bigger(r4)
    assert r5 == 1432
    r6 = _case5_rearrange_bigger(r5)
    assert r6 == 2134
    r_last = _case5_rearrange_bigger(4321)
    assert r_last is False
