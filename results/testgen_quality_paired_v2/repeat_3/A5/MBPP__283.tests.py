# Accepted by submit_tests; explanations in testgen_report.json.

from solution import validate as _case0_validate

def test_single_digit_within_limit():
    """A single digit n should return True since it appears exactly once and 1 <= n for n >= 1."""
    assert _case0_validate(1) == True
    assert _case0_validate(2) == True
    assert _case0_validate(3) == True
    assert _case0_validate(5) == True
    assert _case0_validate(9) == True

from solution import validate as _case1_validate

def test_digit_one_repeated():
    """Digit 1 can appear at most once. Two or more 1s must return False."""
    assert _case1_validate(1) == True
    assert _case1_validate(11) == False
    assert _case1_validate(111) == False
    assert _case1_validate(121) == False

from solution import validate as _case2_validate

def test_digit_two_boundary():
    """Digit 2 can appear at most twice. Exactly 2 is OK, 3 is not."""
    assert _case2_validate(2) == True
    assert _case2_validate(22) == True
    assert _case2_validate(222) == False
    assert _case2_validate(122) == True
    assert _case2_validate(1222) == False

from solution import validate as _case3_validate

def test_multi_digit_valid():
    """A multi-digit number where every digit satisfies the constraint should return True."""
    assert _case3_validate(123) == True
    assert _case3_validate(12) == True
    assert _case3_validate(333) == True
    assert _case3_validate(4444) == True
    assert _case3_validate(55555) == True
    assert _case3_validate(999999999) == True

from solution import validate as _case4_validate

def test_multi_digit_invalid():
    """A multi-digit number violating any digit's frequency constraint should return False."""
    assert _case4_validate(112) == False
    assert _case4_validate(2223) == False
    assert _case4_validate(111) == False
    assert _case4_validate(1222) == False
    assert _case4_validate(10) == False
