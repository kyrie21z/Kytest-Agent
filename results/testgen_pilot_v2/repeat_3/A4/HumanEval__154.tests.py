# Accepted by submit_tests; explanations in testgen_report.json.

"""Test that a direct substring match returns True."""
from solution import cycpattern_check as _case0_cycpattern_check

def test_basic_positive():
    assert _case0_cycpattern_check('hello', 'ell') is True

"""Test that no rotation being a substring returns False."""
from solution import cycpattern_check as _case1_cycpattern_check

def test_basic_negative():
    assert _case1_cycpattern_check('abcd', 'abd') is False

"""Test that a rotated version of b being a substring returns True."""
from solution import cycpattern_check as _case2_cycpattern_check

def test_rotation_match():
    assert _case2_cycpattern_check('abab', 'baa') is True
    assert _case2_cycpattern_check('himenss', 'simen') is True

"""Test single-character b values for both presence and absence."""
from solution import cycpattern_check as _case3_cycpattern_check

def test_single_char():
    assert _case3_cycpattern_check('hello', 'h') is True
    assert _case3_cycpattern_check('hello', 'z') is False
    assert _case3_cycpattern_check('x', 'x') is True

"""Test that when b is longer than a, result is False (unless b is empty)."""
from solution import cycpattern_check as _case4_cycpattern_check

def test_b_longer_than_a():
    assert _case4_cycpattern_check('hi', 'hello') is False
    assert _case4_cycpattern_check('ab', 'abc') is False

"""Test that an empty second word always returns True."""
from solution import cycpattern_check as _case5_cycpattern_check

def test_empty_b_returns_true():
    assert _case5_cycpattern_check('hello', '') is True
    assert _case5_cycpattern_check('', '') is True
