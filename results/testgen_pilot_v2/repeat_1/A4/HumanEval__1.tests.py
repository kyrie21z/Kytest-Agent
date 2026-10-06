# Accepted by submit_tests; explanations in testgen_report.json.

from solution import separate_paren_groups as _case0_separate_paren_groups

def test_empty_string():
    """An empty input string should produce an empty list."""
    result = _case0_separate_paren_groups('')
    assert result == []
    assert isinstance(result, list)

from solution import separate_paren_groups as _case1_separate_paren_groups

def test_spaces_only():
    """A string containing only spaces should yield an empty list."""
    result = _case1_separate_paren_groups('   ')
    assert result == []
    assert isinstance(result, list)

from solution import separate_paren_groups as _case2_separate_paren_groups

def test_basic_docstring_example():
    """Verify the exact example from the docstring."""
    result = _case2_separate_paren_groups('( ) (( )) (( )( ))')
    assert result == ['()', '(())', '(()())']

from solution import separate_paren_groups as _case3_separate_paren_groups

def test_single_group():
    """A single balanced group should be returned as the only element."""
    result = _case3_separate_paren_groups('(())')
    assert result == ['(())']
    assert len(result) == 1
    assert all((isinstance(s, str) for s in result))

from solution import separate_paren_groups as _case4_separate_paren_groups

def test_adjacent_groups_no_space():
    """Two adjacent balanced groups without separating spaces should still be separated correctly."""
    result = _case4_separate_paren_groups('()()')
    assert result == ['()', '()']
    assert len(result) == 2

from solution import separate_paren_groups as _case5_separate_paren_groups

def test_deeply_nested_group():
    """A deeply nested single group should be preserved intact."""
    result = _case5_separate_paren_groups('(((())))')
    assert result == ['(((())))']
    assert len(result) == 1
    assert result[0] == '(((())))'
