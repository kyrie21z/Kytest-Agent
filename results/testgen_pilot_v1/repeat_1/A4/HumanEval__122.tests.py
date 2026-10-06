# Accepted by submit_tests; explanations in testgen_report.json.

from solution import add_elements as _case0_add_elements

def test_docstring_example():
    result = _case0_add_elements([111, 21, 3, 4000, 5, 6, 7, 8, 9], 4)
    assert result == 24

from solution import add_elements as _case1_add_elements

def test_all_qualify():
    result = _case1_add_elements([1, 2, 3], 3)
    assert result == 6

from solution import add_elements as _case2_add_elements

def test_none_qualify():
    result = _case2_add_elements([100, 200, 300], 3)
    assert result == 0

from solution import add_elements as _case3_add_elements

def test_negative_two_digit():
    result = _case3_add_elements([-5, -99, 100], 3)
    assert result == -104

from solution import add_elements as _case4_add_elements

def test_boundary_99_vs_100():
    result = _case4_add_elements([99, 100], 2)
    assert result == 99

from solution import add_elements as _case5_add_elements

def test_zero_element():
    result = _case5_add_elements([0, 100], 2)
    assert result == 0
