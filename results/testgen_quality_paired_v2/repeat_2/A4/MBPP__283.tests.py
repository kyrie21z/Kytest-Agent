# Accepted by submit_tests; explanations in testgen_report.json.

from solution import validate as _case0_validate

def test_single_digit_valid():
    """A single digit d appears once; 1 <= d holds for d >= 1."""
    assert _case0_validate(5) is True

from solution import validate as _case1_validate

def test_repeated_digit_1_invalid():
    """Digit 1 appears twice; 2 > 1 violates the contract."""
    assert _case1_validate(11) is False

from solution import validate as _case2_validate

def test_boundary_digit_2_exact():
    """Digit 2 appears exactly twice; 2 <= 2 is the boundary (valid)."""
    assert _case2_validate(22) is True

from solution import validate as _case3_validate

def test_contains_zero_invalid():
    """Digit 0 appears once; frequency 1 > 0 violates the contract."""
    assert _case3_validate(10) is False

from solution import validate as _case4_validate

def test_zero_input():
    """Zero has no digits; vacuously satisfies the condition."""
    assert _case4_validate(0) is True

from solution import validate as _case5_validate

def test_over_count_digit_2():
    """Digit 2 appears three times; 3 > 2 violates the contract."""
    assert _case5_validate(222) is False
