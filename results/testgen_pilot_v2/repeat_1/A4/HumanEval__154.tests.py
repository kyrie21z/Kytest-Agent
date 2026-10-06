# Accepted by submit_tests; explanations in testgen_report.json.

from solution import cycpattern_check as _case0_cycpattern_check

def test_basic_positive_from_docstring():
    """Test hello/ell case from docstring."""
    assert _case0_cycpattern_check('hello', 'ell') is True

from solution import cycpattern_check as _case1_cycpattern_check

def test_basic_negative_from_docstring():
    """Test abcd/abd case from docstring — b is not a substring nor any rotation."""
    assert _case1_cycpattern_check('abcd', 'abd') is False

from solution import cycpattern_check as _case2_cycpattern_check

def test_rotation_wrapping_match():
    """Test that a rotated version of b matching a substring works.
    For b='baa', rotations are 'baa','aab','aba'. 'aba' is in 'abab'."""
    assert _case2_cycpattern_check('abab', 'baa') is True

from solution import cycpattern_check as _case3_cycpattern_check

def test_empty_b_returns_true():
    """Empty b should always return True per implementation."""
    assert _case3_cycpattern_check('anything', '') is True
    assert _case3_cycpattern_check('', '') is True

from solution import cycpattern_check as _case4_cycpattern_check

def test_a_equals_b_returns_true():
    """When a equals b, result must be True."""
    assert _case4_cycpattern_check('abc', 'abc') is True
    assert _case4_cycpattern_check('xyz', 'xyz') is True

from solution import cycpattern_check as _case5_cycpattern_check

def test_single_char_substring():
    """Single character b that exists in a should return True."""
    assert _case5_cycpattern_check('hello', 'h') is True
    assert _case5_cycpattern_check('hello', 'o') is True
    assert _case5_cycpattern_check('hello', 'z') is False
