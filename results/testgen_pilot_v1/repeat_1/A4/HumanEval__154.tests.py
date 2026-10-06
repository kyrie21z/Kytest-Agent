# Accepted by submit_tests; explanations in testgen_report.json.

"""'ell' is directly a substring of 'hello'.

Contract quote: 'You need to return True if the second word or any of its
rotations is a substring in the first word'

Input domain: a='hello', b='ell' — standard non-empty words where b is an
exact substring of a.

Expected result: True, because 'ell' appears contiguously in 'hello' at
index 1. No rotation needed.

Fault hypothesis: A faulty implementation might only check exact equality
between a and b, missing substring matches entirely.
"""
from solution import cycpattern_check as _case0_cycpattern_check

def test_basic_substring_match():
    assert _case0_cycpattern_check('hello', 'ell') is True

"""A rotation of 'baa' ('aba') is a substring of 'abab'.

Contract quote: 'You need to return True if the second word or any of its
rotations is a substring in the first word'

Input domain: a='abab', b='baa' — b is not a direct substring of a,
but one of its rotations is.

Expected result: True. Rotations of 'baa': 'baa', 'aab', 'aba'. The
rotation 'aba' is found in 'abab' (at index 0).

Fault hypothesis: An implementation that does not generate all rotations
of b will miss this case and incorrectly return False.
"""
from solution import cycpattern_check as _case1_cycpattern_check

def test_rotation_is_substring():
    assert _case1_cycpattern_check('abab', 'baa') is True

"""Neither 'abd' nor any rotation of it is a substring of 'abcd'.

Contract quote: 'cycpattern_check("abcd","abd") => False'

Input domain: a='abcd', b='abd' — neither b nor any cyclic shift of b
appears in a.

Expected result: False. Rotations of 'abd': 'abd', 'bda', 'dab'. None
are substrings of 'abcd'.

Fault hypothesis: A buggy implementation might incorrectly report True
when partial character overlap exists but no full rotation matches.
"""
from solution import cycpattern_check as _case2_cycpattern_check

def test_no_match_or_rotation():
    assert _case2_cycpattern_check('abcd', 'abd') is False

"""Empty string b is considered a substring of any a.

Contract quote: 'You are given 2 words. You need to return True if the second word or any of its rotations is a substring in the first word'

Input domain: a='hello', b='' — b is the empty string.

Expected result: True, because the empty string is a substring of every
string (including itself).

Fault hypothesis: An implementation that skips the empty-b guard clause
may raise an error or return False incorrectly.
"""
from solution import cycpattern_check as _case3_cycpattern_check

def test_empty_b_returns_true():
    assert _case3_cycpattern_check('hello', '') is True

"""When a equals b exactly, the function returns True.

Contract quote: 'You are given 2 words. You need to return True if the second word or any of its rotations is a substring in the first word'

Input domain: a='abc', b='abc' — both arguments are identical.

Expected result: True, since b is trivially a substring of a.

Fault hypothesis: An implementation that relies solely on rotation logic
without the explicit a==b shortcut might still work, but this test
verifies the documented early-return path.
"""
from solution import cycpattern_check as _case4_cycpattern_check

def test_equal_strings_return_true():
    assert _case4_cycpattern_check('abc', 'abc') is True

"""When b is longer than a, no rotation of b can fit inside a.

Contract quote: 'You are given 2 words. You need to return True if the second word or any of its rotations is a substring in the first word'

Input domain: a='hi', b='world' — len(b) > len(a).

Expected result: False, because even the shortest rotation of b has
length 5, which exceeds len(a)=2.

Fault hypothesis: An implementation that doesn't account for length
differences might produce incorrect results due to out-of-range indexing.
"""
from solution import cycpattern_check as _case5_cycpattern_check

def test_b_longer_than_a_returns_false():
    assert _case5_cycpattern_check('hi', 'world') is False
