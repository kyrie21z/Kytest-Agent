import pytest


def test_docstring_examples():
    """Test the examples from the docstring."""
    from solution import change_base
    assert change_base(8, 3) == "22"
    assert change_base(8, 2) == "1000"
    assert change_base(7, 2) == "111"


def test_zero():
    """Test that 0 returns '0' regardless of base."""
    from solution import change_base
    assert change_base(0, 2) == "0"
    assert change_base(0, 3) == "0"
    assert change_base(0, 9) == "0"


def test_single_digit_numbers():
    """Test numbers smaller than the base (single digit output)."""
    from solution import change_base
    assert change_base(1, 2) == "1"
    assert change_base(2, 3) == "2"
    assert change_base(5, 8) == "5"
    assert change_base(9, 10) == "9"


def test_base_2_binary():
    """Test conversion to binary (base 2)."""
    from solution import change_base
    assert change_base(1, 2) == "1"
    assert change_base(2, 2) == "10"
    assert change_base(3, 2) == "11"
    assert change_base(4, 2) == "100"
    assert change_base(10, 2) == "1010"
    assert change_base(15, 2) == "1111"
    assert change_base(16, 2) == "10000"
    assert change_base(255, 2) == "11111111"
    assert change_base(256, 2) == "100000000"


def test_base_3():
    """Test conversion to base 3."""
    from solution import change_base
    assert change_base(1, 3) == "1"
    assert change_base(2, 3) == "2"
    assert change_base(3, 3) == "10"
    assert change_base(4, 3) == "11"
    assert change_base(8, 3) == "22"
    assert change_base(9, 3) == "100"
    assert change_base(10, 3) == "101"
    assert change_base(27, 3) == "1000"


def test_base_4():
    """Test conversion to base 4."""
    from solution import change_base
    assert change_base(1, 4) == "1"
    assert change_base(4, 4) == "10"
    assert change_base(8, 4) == "20"
    assert change_base(15, 4) == "33"
    assert change_base(16, 4) == "100"
    assert change_base(64, 4) == "1000"


def test_base_5():
    """Test conversion to base 5."""
    from solution import change_base
    assert change_base(1, 5) == "1"
    assert change_base(5, 5) == "10"
    assert change_base(10, 5) == "20"
    assert change_base(24, 5) == "44"
    assert change_base(25, 5) == "100"
    assert change_base(100, 5) == "400"


def test_base_8_octal():
    """Test conversion to octal (base 8)."""
    from solution import change_base
    assert change_base(1, 8) == "1"
    assert change_base(7, 8) == "7"
    assert change_base(8, 8) == "10"
    assert change_base(64, 8) == "100"
    assert change_base(65, 8) == "101"
    assert change_base(100, 8) == "144"


def test_base_9():
    """Test conversion to base 9."""
    from solution import change_base
    assert change_base(1, 9) == "1"
    assert change_base(8, 9) == "8"
    assert change_base(9, 9) == "10"
    assert change_base(18, 9) == "20"
    assert change_base(80, 9) == "88"
    assert change_base(81, 9) == "100"


def test_larger_numbers():
    """Test with larger input values."""
    from solution import change_base
    assert change_base(100, 2) == "1100100"
    assert change_base(100, 3) == "10201"
    assert change_base(100, 4) == "1210"
    assert change_base(100, 5) == "400"
    assert change_base(1000, 2) == "1111101000"
    assert change_base(1000, 10) == "1000"
    assert change_base(1024, 2) == "10000000000"
    assert change_base(1024, 4) == "100000"
    assert change_base(1024, 8) == "2000"
    assert change_base(1024, 16) == "400"


def test_base_equals_number():
    """Test when the number equals the base (should return '10')."""
    from solution import change_base
    assert change_base(2, 2) == "10"
    assert change_base(3, 3) == "10"
    assert change_base(5, 5) == "10"
    assert change_base(9, 9) == "10"


def test_power_of_base():
    """Test powers of the base (should produce '1' followed by zeros)."""
    from solution import change_base
    assert change_base(4, 2) == "100"       # 2^2
    assert change_base(8, 2) == "1000"      # 2^3
    assert change_base(16, 2) == "10000"    # 2^4
    assert change_base(27, 3) == "1000"     # 3^3
    assert change_base(81, 3) == "10000"    # 3^4
    assert change_base(64, 4) == "1000"     # 4^3
    assert change_base(125, 5) == "1000"    # 5^3
    assert change_base(49, 7) == "100"      # 7^2
    assert change_base(81, 9) == "100"      # 9^2


def test_negative_input():
    """Test behavior with negative numbers (may raise exception or loop)."""
    from solution import change_base
    # The function as written may not handle negatives well;
    # we test that it either raises an error or produces a result.
    # Based on the implementation, negative numbers could cause infinite loops.
    # We set a timeout via pytest-timeout if available, otherwise just note it.
    # For now, skip this test as the function isn't designed for negatives.
    pytest.skip("Function does not support negative numbers")


def test_invalid_base_zero():
    """Test that base 0 raises ZeroDivisionError."""
    from solution import change_base
    with pytest.raises(ZeroDivisionError):
        change_base(10, 0)


def test_invalid_base_one():
    """Test that base 1 causes issues (infinite loop / no termination).
    Skipping because it would hang the test runner."""
    pytest.skip("Base 1 causes infinite loop; not tested")


def test_consistency_with_int_conversion():
    """Verify that converting back from the string gives the original number."""
    from solution import change_base
    for num in range(0, 200):
        for base in range(2, 10):
            converted = change_base(num, base)
            reconstructed = int(converted, base)
            assert reconstructed == num, f"Mismatch for num={num}, base={base}: got '{converted}'"
