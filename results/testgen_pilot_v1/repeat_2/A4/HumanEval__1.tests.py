# Accepted by submit_tests; explanations in testgen_report.json.

"""Test that an empty input string yields an empty list."""
from solution import separate_paren_groups as _case0_separate_paren_groups

def test_empty_string():
    """An empty input string should yield an empty list.

    Contract quote: The function processes a string of parentheses groups.
    With no characters, there are zero groups.

    Input domain: paren_string = '' — zero length.

    Expected result: No iterations occur, results stays [].

    Fault hypothesis: Some implementations might return [None], [''], or
    raise an exception on empty input instead of returning [].
    """
    result = _case0_separate_paren_groups('')
    assert result == []

"""Test a deeply nested single group returned intact."""
from solution import separate_paren_groups as _case1_separate_paren_groups

def test_deeply_nested_single_group():
    """A deeply nested single group should be returned intact.

    Contract quote: 'groups of nested parentheses' — nesting is expected.

    Input domain: paren_string = '((( )))' — three levels of nesting.

    Expected result: cnt goes 1->2->3->2->1->0, emitting '((()))' once.

    Fault hypothesis: An implementation that resets cnt prematurely or
    miscounts depth could split this into multiple incorrect groups.
    """
    result = _case1_separate_paren_groups('((( )))')
    assert result == ['((()))']

"""Test groups with different nesting depths captured correctly."""
from solution import separate_paren_groups as _case2_separate_paren_groups

def test_mixed_nesting_depths():
    """Groups with different nesting depths should each be captured correctly.

    Contract quote: 'multiple groups of nested parentheses' — variety is allowed.

    Input domain: paren_string = '() ((())) ()' — depths 1, 3, 1.

    Expected result: Three groups: '()', '((()))', '()'.

    Fault hypothesis: An implementation might merge groups across boundaries
    or lose the middle deeply-nested group.
    """
    result = _case2_separate_paren_groups('() ((())) ()')
    assert result == ['()', '((()))', '()']

"""Test the exact example from the function's docstring."""
from solution import separate_paren_groups as _case3_separate_paren_groups

def test_docstring_example():
    """Verify the exact example from the function's docstring.

    Contract quote: 'Input to this function is a string containing
    multiple groups of nested parentheses.'

    Input domain: paren_string = '( ) (( )) (( )( ))'

    Expected result: After stripping spaces the string becomes
    '()(()))(()())'. Scanning left-to-right: '(' -> cnt=1, ')' -> cnt=0
    emits '()'; then '(' -> cnt=1, '(' -> cnt=2, ')' -> cnt=1, ')' -> cnt=0
    emits '(())'; then '(' -> cnt=1, '(' -> cnt=2, ')' -> cnt=1,
    '(' -> cnt=2, ')' -> cnt=1, ')' -> cnt=0 emits '(()())'.
    Result: ['()', '(())', '(()())'].

    Fault hypothesis: A faulty implementation might fail to ignore spaces
    or might incorrectly split on spaces instead of balancing parentheses.
    """
    result = _case3_separate_paren_groups('( ) (( )) (( )( ))')
    assert result == ['()', '(())', '(()())']

"""Test adjacent balanced groups without separating spaces."""
from solution import separate_paren_groups as _case4_separate_paren_groups

def test_multiple_simple_groups_without_spaces():
    """Adjacent balanced groups without separating spaces should still be
    detected as separate groups.

    Contract quote: 'Separate groups are balanced (each open brace is
    properly closed) and not nested within each other'

    Input domain: paren_string = '()()()' — three adjacent simple pairs.

    Expected result: Each pair independently reaches cnt=0, so three
    groups are emitted: '()', '()', '()'.

    Fault hypothesis: An implementation that requires space separators
    would return ['()()()'] as a single element, failing to split.
    """
    result = _case4_separate_paren_groups('()()()')
    assert result == ['()', '()', '()']

"""Test that the return value is a list of strings."""
from solution import separate_paren_groups as _case5_separate_paren_groups

def test_return_type_is_list_of_strings():
    """The return value must be a list whose elements are strings.

    Contract quote: 'separate those group into separate strings and
    return the list of those.'

    Input domain: paren_string = '() (())' — mixed groups.

    Expected result: A Python list containing exactly two string elements.

    Fault hypothesis: An implementation might return a tuple, set, or
    a list containing non-string types.
    """
    result = _case5_separate_paren_groups('() (())')
    assert isinstance(result, list)
    assert all((isinstance(item, str) for item in result))
