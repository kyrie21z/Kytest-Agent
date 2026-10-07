# Accepted by submit_tests; explanations in testgen_report.json.

import solution as _case0_solution

def test_empty_list():
    assert _case0_solution.is_Monotonic([]) is True

import solution as _case1_solution

def test_single_element():
    assert _case1_solution.is_Monotonic([42]) is True

import solution as _case2_solution

def test_strictly_increasing():
    assert _case2_solution.is_Monotonic([1, 2, 3, 4, 5]) is True

import solution as _case3_solution

def test_not_monotonic_up_then_down():
    assert _case3_solution.is_Monotonic([1, 3, 2]) is False

import solution as _case4_solution

def test_plateau_then_drop():
    assert _case4_solution.is_Monotonic([3, 3, 2]) is True

import solution as _case5_solution

def test_type_return_is_bool():
    result = _case5_solution.is_Monotonic([1, 2, 3])
    assert isinstance(result, bool)

import solution as _case6_solution

def test_strictly_decreasing_detects_m5():
    assert _case6_solution.is_Monotonic([5, 4, 3, 2, 1]) is True

import solution as _case7_solution

def test_two_element_decreasing():
    assert _case7_solution.is_Monotonic([3, 1]) is True
