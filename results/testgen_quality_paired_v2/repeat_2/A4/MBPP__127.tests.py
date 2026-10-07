# Accepted by submit_tests; explanations in testgen_report.json.

import solution as _case0_solution

def test_multiply_positive():
    """Verify basic positive integer multiplication works correctly."""
    assert _case0_solution.multiply_int(3, 4) == 12
    assert _case0_solution.multiply_int(7, 6) == 42
    assert _case0_solution.multiply_int(10, 10) == 100

import solution as _case1_solution

def test_multiply_by_zero():
    """Multiplying any integer by 0 must return 0."""
    assert _case1_solution.multiply_int(5, 0) == 0
    assert _case1_solution.multiply_int(-5, 0) == 0
    assert _case1_solution.multiply_int(0, 0) == 0

import solution as _case2_solution

def test_multiply_by_one():
    """Multiplying any integer by 1 must return that integer."""
    assert _case2_solution.multiply_int(5, 1) == 5
    assert _case2_solution.multiply_int(-5, 1) == -5
    assert _case2_solution.multiply_int(0, 1) == 0

import solution as _case3_solution

def test_multiply_negative_y():
    """When y is negative, result should be negated product."""
    assert _case3_solution.multiply_int(3, -4) == -12
    assert _case3_solution.multiply_int(-3, -4) == 12
    assert _case3_solution.multiply_int(0, -5) == 0

import solution as _case4_solution

def test_multiply_both_negative():
    """Product of two negatives must be positive."""
    assert _case4_solution.multiply_int(-3, -4) == 12
    assert _case4_solution.multiply_int(-7, -3) == 21
    assert _case4_solution.multiply_int(-1, -1) == 1

import solution as _case5_solution

def test_multiply_negative_x_positive_y():
    """Negative x times positive y yields negative result."""
    assert _case5_solution.multiply_int(-3, 4) == -12
    assert _case5_solution.multiply_int(-7, 3) == -21
    assert _case5_solution.multiply_int(-1, 10) == -10
