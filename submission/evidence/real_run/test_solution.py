# Accepted by submit_tests; explanations in testgen_report.json.

import pytest as _case0_pytest

def test_multiply_positive():
    """Test basic positive integer multiplication."""
    from solution import multiply_int
    assert multiply_int(3, 4) == 12

import pytest as _case1_pytest

def test_multiply_return_type():
    """The function should always return an int for integer inputs."""
    from solution import multiply_int
    result = multiply_int(6, 7)
    assert isinstance(result, int), f'Expected int, got {type(result)}'

import pytest as _case2_pytest

def test_multiply_by_zero():
    """Contract: y==0 must return 0 regardless of x. Detects M3 (return 0 -> return 1)."""
    from solution import multiply_int
    assert multiply_int(0, 0) == 0
    assert multiply_int(42, 0) == 0
    assert multiply_int(-7, 0) == 0

import pytest as _case3_pytest

def test_multiply_by_one():
    """Contract: y==1 must return x unchanged. Also verifies recursion terminates correctly."""
    from solution import multiply_int
    assert multiply_int(5, 1) == 5
    assert multiply_int(-3, 1) == -3
    assert multiply_int(0, 1) == 0

import pytest as _case4_pytest

def test_multiply_negative_y():
    """Contract: y<0 negates the product via -multiply_int(x, -y)."""
    from solution import multiply_int
    assert multiply_int(3, -4) == -12
    assert multiply_int(-3, -4) == 12
    assert multiply_int(0, -5) == 0

import pytest as _case5_pytest

def test_multiply_both_negative():
    """Two negatives produce a positive product via double negation."""
    from solution import multiply_int
    assert multiply_int(-3, -5) == 15
    assert multiply_int(-1, -1) == 1
