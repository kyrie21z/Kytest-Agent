# Accepted by submit_tests; explanations in testgen_report.json.

from solution import cycpattern_check as _case0_cycpattern_check

def test_basic_substring_no_rotation():
    assert _case0_cycpattern_check('hello', 'ell') is True

from solution import cycpattern_check as _case1_cycpattern_check

def test_rotation_needed_match():
    assert _case1_cycpattern_check('abab', 'baa') is True

from solution import cycpattern_check as _case2_cycpattern_check

def test_no_match_any_rotation():
    assert _case2_cycpattern_check('abcd', 'abd') is False

from solution import cycpattern_check as _case3_cycpattern_check

def test_empty_b_returns_true():
    assert _case3_cycpattern_check('hello', '') is True
    assert _case3_cycpattern_check('', '') is True

from solution import cycpattern_check as _case4_cycpattern_check

def test_equal_strings_return_true():
    assert _case4_cycpattern_check('abc', 'abc') is True
    assert _case4_cycpattern_check('same', 'same') is True

from solution import cycpattern_check as _case5_cycpattern_check

def test_b_longer_than_a_returns_false():
    assert _case5_cycpattern_check('a', 'abc') is False
    assert _case5_cycpattern_check('hi', 'longer') is False
