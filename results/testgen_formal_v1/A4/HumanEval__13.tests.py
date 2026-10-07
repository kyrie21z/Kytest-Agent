# Accepted by submit_tests; explanations in testgen_report.json.

import solution as _case0_solution

def test_gcd_basic_positive():
    """Test GCD with standard positive integer pairs."""
    assert _case0_solution.greatest_common_divisor(3, 5) == 1
    assert _case0_solution.greatest_common_divisor(25, 15) == 5
    assert _case0_solution.greatest_common_divisor(12, 8) == 4
    assert _case0_solution.greatest_common_divisor(100, 75) == 25

import solution as _case1_solution

def test_gcd_one_divides_other():
    """When one integer divides the other, GCD equals the divisor."""
    assert _case1_solution.greatest_common_divisor(10, 5) == 5
    assert _case1_solution.greatest_common_divisor(5, 10) == 5
    assert _case1_solution.greatest_common_divisor(7, 1) == 1
    assert _case1_solution.greatest_common_divisor(1, 7) == 1

import solution as _case2_solution

def test_gcd_same_number():
    """GCD of a number with itself is the number."""
    assert _case2_solution.greatest_common_divisor(7, 7) == 7
    assert _case2_solution.greatest_common_divisor(42, 42) == 42
    assert _case2_solution.greatest_common_divisor(1, 1) == 1

import solution as _case3_solution

def test_gcd_with_zero():
    """GCD(x, 0) = |x| and GCD(0, x) = |x| per Euclidean algorithm."""
    assert _case3_solution.greatest_common_divisor(0, 5) == 5
    assert _case3_solution.greatest_common_divisor(5, 0) == 5
    assert _case3_solution.greatest_common_divisor(0, 0) == 0

import solution as _case4_solution

def test_gcd_return_type():
    """Verify the return value is always an int."""
    result = _case4_solution.greatest_common_divisor(25, 15)
    assert isinstance(result, int), f'Expected int, got {type(result)}'
    result2 = _case4_solution.greatest_common_divisor(0, 0)
    assert isinstance(result2, int), f'Expected int, got {type(result2)}'

import solution as _case5_solution

def test_gcd_negative_numbers():
    """Verify GCD with negative inputs matches the actual implementation behavior.
    Python's modulo preserves the sign of the divisor, so the final non-zero
    remainder may be negative depending on which argument is last."""
    assert _case5_solution.greatest_common_divisor(12, -8) == -4
    assert _case5_solution.greatest_common_divisor(-12, 8) == 4
    assert _case5_solution.greatest_common_divisor(-12, -8) == -4
