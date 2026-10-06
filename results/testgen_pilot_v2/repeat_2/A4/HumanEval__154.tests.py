# Accepted by submit_tests; explanations in testgen_report.json.

from solution import cycpattern_check as _case0_cycpattern_check

def test_docstring_examples():
    assert _case0_cycpattern_check('abcd', 'abd') == False
    assert _case0_cycpattern_check('hello', 'ell') == True
    assert _case0_cycpattern_check('whassup', 'psus') == False
    assert _case0_cycpattern_check('abab', 'baa') == True
    assert _case0_cycpattern_check('efef', 'eeff') == False
    assert _case0_cycpattern_check('himenss', 'simen') == True

from solution import cycpattern_check as _case1_cycpattern_check

def test_empty_b_returns_true():
    assert _case1_cycpattern_check('hello', '') == True
    assert _case1_cycpattern_check('', '') == True
    assert _case1_cycpattern_check('abc', '') == True

from solution import cycpattern_check as _case2_cycpattern_check

def test_rotation_needed():
    assert _case2_cycpattern_check('abcdef', 'bcd') == True
    assert _case2_cycpattern_check('abcdef', 'cab') == True
    assert _case2_cycpattern_check('xyzab', 'zab') == True
    assert _case2_cycpattern_check('xyzab', 'abz') == True

from solution import cycpattern_check as _case3_cycpattern_check

def test_single_char_strings():
    assert _case3_cycpattern_check('a', 'a') == True
    assert _case3_cycpattern_check('a', 'b') == False
    assert _case3_cycpattern_check('hello', 'h') == True
    assert _case3_cycpattern_check('hello', 'o') == True
    assert _case3_cycpattern_check('hello', 'z') == False
    assert _case3_cycpattern_check('a', 'aa') == False

from solution import cycpattern_check as _case4_cycpattern_check

def test_no_match_cases():
    assert _case4_cycpattern_check('ab', 'abc') == False
    assert _case4_cycpattern_check('a', 'abc') == False
    assert _case4_cycpattern_check('abc', 'xyz') == False
    assert _case4_cycpattern_check('abc', 'def') == False
    assert _case4_cycpattern_check('aaa', 'aab') == False

from solution import cycpattern_check as _case5_cycpattern_check

def test_return_type_and_repeated_chars():
    assert isinstance(_case5_cycpattern_check('hello', 'ell'), bool)
    assert isinstance(_case5_cycpattern_check('hello', 'xyz'), bool)
    assert _case5_cycpattern_check('aaaa', 'aa') == True
    assert _case5_cycpattern_check('aaaa', 'aaa') == True
    assert _case5_cycpattern_check('abab', 'ab') == True
    assert _case5_cycpattern_check('abab', 'ba') == True
    assert _case5_cycpattern_check('xxx', 'x') == True
    assert _case5_cycpattern_check('xxx', 'xx') == True
