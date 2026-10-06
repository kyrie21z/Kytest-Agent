# Accepted by submit_tests; explanations in testgen_report.json.

from solution import separate_paren_groups as _case0_separate_paren_groups

def test_docstring_example():
    """Test the exact example from the docstring."""
    result = _case0_separate_paren_groups('( ) (( )) (( )( ))')
    assert result == ['()', '(())', '(()())']

from solution import separate_paren_groups as _case1_separate_paren_groups

def test_single_group():
    """A single balanced group should return a list with one element."""
    result = _case1_separate_paren_groups('()')
    assert result == ['()']
    assert isinstance(result, list)
    assert len(result) == 1

from solution import separate_paren_groups as _case2_separate_paren_groups

def test_empty_string():
    """Empty input should return an empty list."""
    result = _case2_separate_paren_groups('')
    assert result == []
    assert isinstance(result, list)

from solution import separate_paren_groups as _case3_separate_paren_groups

def test_spaces_only():
    """A string of only spaces should return an empty list since no groups exist."""
    result = _case3_separate_paren_groups('     ')
    assert result == []
    assert isinstance(result, list)

from solution import separate_paren_groups as _case4_separate_paren_groups

def test_multiple_simple_groups():
    """Multiple adjacent simple groups should each be returned separately."""
    result = _case4_separate_paren_groups('()()()')
    assert result == ['()', '()', '()']
    assert len(result) == 3

from solution import separate_paren_groups as _case5_separate_paren_groups

def test_deeply_nested():
    """Deeply nested parentheses form a single group."""
    result = _case5_separate_paren_groups('(((())))')
    assert result == ['(((())))']
    assert len(result) == 1
    assert result[0].count('(') == 4
    assert result[0].count(')') == 4
