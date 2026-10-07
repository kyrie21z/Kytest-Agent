# Accepted by submit_tests; explanations in testgen_report.json.

import solution as _case0_solution

def test_multiply_positive_positive():
    """Verify basic positive * positive multiplication."""
    assert _case0_solution.multiply_int(3, 4) == 12

import solution as _case1_solution

def test_multiply_negative_first_arg():
    """Verify negative * positive yields negative result."""
    assert _case1_solution.multiply_int(-3, 4) == -12

import solution as _case2_solution

def test_multiply_positive_negative_y():
    """Verify positive * negative yields negative result via recursive negation."""
    assert _case2_solution.multiply_int(3, -4) == -12

import solution as _case3_solution

def test_multiply_both_negative():
    """Verify negative * negative yields positive result."""
    assert _case3_solution.multiply_int(-3, -4) == 12

import solution as _case4_solution

def test_multiply_by_zero():
    """Verify any number multiplied by 0 yields 0."""
    assert _case4_solution.multiply_int(7, 0) == 0
    assert _case4_solution.multiply_int(0, 7) == 0
    assert _case4_solution.multiply_int(0, 0) == 0

import solution as _case5_solution

def test_multiply_by_one_identity():
    """Verify multiplying by 1 returns the other operand unchanged."""
    assert _case5_solution.multiply_int(5, 1) == 5
    assert _case5_solution.multiply_int(-7, 1) == -7
