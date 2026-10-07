# Accepted by submit_tests; explanations in testgen_report.json.

from solution import specialFilter as _case0_specialFilter

def test_docstring_example_1():
    """Verify the first example from the docstring."""
    assert _case0_specialFilter([15, -73, 14, -15]) == 1

from solution import specialFilter as _case1_specialFilter

def test_docstring_example_2():
    """Verify the second example from the docstring."""
    assert _case1_specialFilter([33, -2, -3, 45, 21, 109]) == 2

from solution import specialFilter as _case2_specialFilter

def test_empty_list():
    """Verify correct handling of an empty input list."""
    assert _case2_specialFilter([]) == 0

from solution import specialFilter as _case3_specialFilter

def test_all_qualify():
    """Verify counting when every element satisfies the predicate."""
    assert _case3_specialFilter([11, 13, 15, 17, 19]) == 5

from solution import specialFilter as _case4_specialFilter

def test_none_qualify():
    """Verify that numbers <= 10 do not qualify."""
    assert _case4_specialFilter([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 0

from solution import specialFilter as _case5_specialFilter

def test_boundary_11():
    """Verify that 11 is the smallest qualifying number."""
    assert _case5_specialFilter([11]) == 1
