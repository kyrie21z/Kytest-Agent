# Accepted by submit_tests; explanations in testgen_report.json.

"""Test all examples given in the docstring."""
from solution import cycpattern_check as _case0_cycpattern_check

def test_docstring_examples():
    assert _case0_cycpattern_check('abcd', 'abd') == False
    assert _case0_cycpattern_check('hello', 'ell') == True
    assert _case0_cycpattern_check('whassup', 'psus') == False
    assert _case0_cycpattern_check('abab', 'baa') == True
    assert _case0_cycpattern_check('efef', 'eeff') == False
    assert _case0_cycpattern_check('himenss', 'simen') == True

"""Test that an empty second word always returns True."""
from solution import cycpattern_check as _case1_cycpattern_check

def test_empty_b_returns_true():
    assert _case1_cycpattern_check('hello', '') is True
    assert _case1_cycpattern_check('', '') is True
    assert _case1_cycpattern_check('abc', '') is True

"""Test that identical strings return True via the equality shortcut."""
from solution import cycpattern_check as _case2_cycpattern_check

def test_a_equals_b():
    assert _case2_cycpattern_check('abc', 'abc') is True
    assert _case2_cycpattern_check('xyz', 'xyz') is True
    assert _case2_cycpattern_check('', '') is True

"""Test that when b is longer than a, no rotation can be a substring."""
from solution import cycpattern_check as _case3_cycpattern_check

def test_b_longer_than_a():
    assert _case3_cycpattern_check('ab', 'abcde') is False
    assert _case3_cycpattern_check('a', 'abcdef') is False
    assert _case3_cycpattern_check('hi', 'longerstring') is False

"""Test single character matching and non-matching scenarios."""
from solution import cycpattern_check as _case4_cycpattern_check

def test_single_char_match_and_no_match():
    assert _case4_cycpattern_check('hello', 'l') is True
    assert _case4_cycpattern_check('ba', 'a') is True
    assert _case4_cycpattern_check('world', 'w') is True
    assert _case4_cycpattern_check('hello', 'z') is False
    assert _case4_cycpattern_check('ba', 'c') is False

"""Test that a rotation of b is found embedded within a."""
from solution import cycpattern_check as _case5_cycpattern_check

def test_rotation_found_embedded():
    assert _case5_cycpattern_check('abracadabra', 'cadab') is True
    assert _case5_cycpattern_check('bcdef', 'cdefb') is True
    assert _case5_cycpattern_check('hello', 'ell') is True
