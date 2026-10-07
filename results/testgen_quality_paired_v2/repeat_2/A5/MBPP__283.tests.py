# Accepted by submit_tests; explanations in testgen_report.json.

def test_validate_single_digit_one():
    """Single digit 1: frequency of digit 1 is 1, which equals 1. Valid."""
    from solution import validate
    result = validate(1)
    assert isinstance(result, bool)
    assert result is True

def test_validate_digit_one_twice():
    """Number 11: digit 1 appears twice. 2 > 1, so invalid."""
    from solution import validate
    result = validate(11)
    assert isinstance(result, bool)
    assert result is False

def test_validate_contains_zero():
    """Number 10: contains digit 0. Frequency of 0 is 1, but 1 > 0, so invalid."""
    from solution import validate
    result = validate(10)
    assert isinstance(result, bool)
    assert result is False

def test_validate_digit_two_boundary():
    """Number 22: digit 2 appears exactly twice. 2 <= 2, so valid."""
    from solution import validate
    result = validate(22)
    assert isinstance(result, bool)
    assert result is True

def test_validate_digit_three_over_limit():
    """Number 3333: digit 3 appears 4 times. 4 > 3, so invalid."""
    from solution import validate
    result = validate(3333)
    assert isinstance(result, bool)
    assert result is False

def test_validate_mixed_distinct_digits():
    """Number 123456789: each digit 1-9 appears once. All frequencies <= digit value. Valid."""
    from solution import validate
    result = validate(123456789)
    assert isinstance(result, bool)
    assert result is True
