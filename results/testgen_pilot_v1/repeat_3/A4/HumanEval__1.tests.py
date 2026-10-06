# Accepted by submit_tests; explanations in testgen_report.json.

from solution import separate_paren_groups as _case0_separate_paren_groups

def test_docstring_example():
    result = _case0_separate_paren_groups('( ) (( )) (( )( ))')
    assert result == ['()', '(())', '(()())']

from solution import separate_paren_groups as _case1_separate_paren_groups

def test_single_group_no_spaces():
    result = _case1_separate_paren_groups('()')
    assert result == ['()']

from solution import separate_paren_groups as _case2_separate_paren_groups

def test_empty_string():
    result = _case2_separate_paren_groups('')
    assert result == []

from solution import separate_paren_groups as _case3_separate_paren_groups

def test_only_spaces():
    result = _case3_separate_paren_groups('   ')
    assert result == []

from solution import separate_paren_groups as _case4_separate_paren_groups

def test_two_adjacent_groups_no_separator():
    result = _case4_separate_paren_groups('()()')
    assert result == ['()', '()']

from solution import separate_paren_groups as _case5_separate_paren_groups

def test_return_type_is_list_of_strings():
    result = _case5_separate_paren_groups('(()) (())')
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, str)
