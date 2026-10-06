# Accepted by submit_tests; explanations in testgen_report.json.

from solution import separate_paren_groups as _case0_separate_paren_groups

def test_single_group():
    """Test that a single balanced group is returned as-is."""
    result = _case0_separate_paren_groups('(())')
    assert result == ['(())'], f"Expected ['(())'], got {result}"
    assert isinstance(result, list), f'Expected list, got {type(result)}'

from solution import separate_paren_groups as _case1_separate_paren_groups

def test_multiple_groups():
    """Test the doctest example with three groups."""
    result = _case1_separate_paren_groups('( ) (( )) (( )( ))')
    assert result == ['()', '(())', '(()())'], f"Expected ['()', '(())', '(()())'], got {result}"
    assert len(result) == 3, f'Expected 3 groups, got {len(result)}'

from solution import separate_paren_groups as _case2_separate_paren_groups

def test_empty_string():
    """Test that an empty string returns an empty list."""
    result = _case2_separate_paren_groups('')
    assert result == [], f'Expected [], got {result}'
    assert isinstance(result, list), f'Expected list, got {type(result)}'

from solution import separate_paren_groups as _case3_separate_paren_groups

def test_only_spaces():
    """Test that a string with only spaces returns an empty list."""
    result2 = _case3_separate_paren_groups('     ')
    assert result2 == [], f'Expected [] for all-spaces, got {result2}'
    result = _case3_separate_paren_groups('   ( )   (( ))   ')
    assert result == ['()', '(())'], f"Expected ['()', '(())'], got {result}"

from solution import separate_paren_groups as _case4_separate_paren_groups

def test_deeply_nested():
    """Test deeply nested single group."""
    result = _case4_separate_paren_groups('((((()))))')
    assert result == ['((((()))))'], f"Expected ['((((()))))'], got {result}"
    assert len(result) == 1, f'Expected 1 group, got {len(result)}'
    assert result[0] == '((((()))))', f'Group content mismatch: {result[0]}'

from solution import separate_paren_groups as _case5_separate_paren_groups

def test_adjacent_without_space():
    """Test two adjacent balanced groups without space separator."""
    result = _case5_separate_paren_groups('()()')
    assert result == ['()', '()'], f"Expected ['()', '()'], got {result}"
    assert len(result) == 2, f'Expected 2 groups, got {len(result)}'
