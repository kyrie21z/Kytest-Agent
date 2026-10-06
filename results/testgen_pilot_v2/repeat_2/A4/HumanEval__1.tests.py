# Accepted by submit_tests; explanations in testgen_report.json.

from solution import separate_paren_groups as _case0_separate_paren_groups

def test_empty_string():
    """An empty input string should return an empty list."""
    result = _case0_separate_paren_groups('')
    assert result == []
    assert isinstance(result, list)

from solution import separate_paren_groups as _case1_separate_paren_groups

def test_only_spaces():
    """A string with only spaces should return an empty list."""
    result = _case1_separate_paren_groups('   ')
    assert result == []
    assert isinstance(result, list)

from solution import separate_paren_groups as _case2_separate_paren_groups

def test_basic_docstring_example():
    """Test the exact example from the docstring."""
    result = _case2_separate_paren_groups('( ) (( )) (( )( ))')
    assert result == ['()', '(())', '(()())']

from solution import separate_paren_groups as _case3_separate_paren_groups

def test_single_balanced_group():
    """A single balanced group should be returned as the only element."""
    result = _case3_separate_paren_groups('(())')
    assert result == ['(())']
    assert len(result) == 1

from solution import separate_paren_groups as _case4_separate_paren_groups

def test_multiple_simple_groups():
    """Multiple simple adjacent groups separated by spaces."""
    result = _case4_separate_paren_groups('() () ()')
    assert result == ['()', '()', '()']
    assert len(result) == 3

from solution import separate_paren_groups as _case5_separate_paren_groups

def test_incomplete_trailing_group():
    """A trailing incomplete (unclosed) group should be dropped."""
    result = _case5_separate_paren_groups('() (')
    assert result == ['()']
    assert len(result) == 1
