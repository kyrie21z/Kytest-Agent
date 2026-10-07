import pytest


def test_docstring_examples():
    """Test the examples from the docstring."""
    from solution import change_base
    assert change_base(8, 3) == '22'
    assert change_base(8, 2) == '1000'
    assert change_base(7, 2) == '111'


def test_zero_input():
    """Test that zero returns '0' regardless of base."""
    from solution import change_base
    assert change_base(0, 2) == '0'
    assert change_base(0, 8) == '0'
    assert change_base(0, 10) == '0'


def test_smallest_positive_numbers():
    """Test converting 1 in various bases."""
    from solution import change_base
    assert change_base(1, 2) == '1'
    assert change_base(1, 3) == '1'
    assert change_base(1, 9) == '1'
    assert change_base(1, 10) == '1'


def test_single_digit_numbers():
    """Test numbers smaller than base return single digit."""
    from solution import change_base
    # Numbers less than base should return themselves as strings
    assert change_base(2, 3) == '2'
    assert change_base(5, 8) == '5'
    assert change_base(9, 10) == '9'
    assert change_base(7, 9) == '7'


def test_number_equals_base():
    """Test when x equals the base (should be '10')."""
    from solution import change_base
    assert change_base(2, 2) == '10'
    assert change_base(3, 3) == '10'
    assert change_base(8, 8) == '10'
    assert change_base(10, 10) == '10'


def test_power_of_two():
    """Test powers of 2 in binary."""
    from solution import change_base
    assert change_base(2, 2) == '10'
    assert change_base(4, 2) == '100'
    assert change_base(8, 2) == '1000'
    assert change_base(16, 2) == '10000'
    assert change_base(32, 2) == '100000'
    assert change_base(64, 2) == '1000000'
    assert change_base(128, 2) == '10000000'
    assert change_base(256, 2) == '100000000'


def test_various_bases():
    """Test conversion across different bases."""
    from solution import change_base
    # Decimal 10
    assert change_base(10, 2) == '1010'
    assert change_base(10, 3) == '101'
    assert change_base(10, 8) == '12'
    assert change_base(10, 10) == '10'

    # Decimal 100
    assert change_base(100, 2) == '1100100'
    assert change_base(100, 3) == '10201'
    assert change_base(100, 8) == '144'
    assert change_base(100, 10) == '100'

    # Decimal 64
    assert change_base(64, 2) == '1000000'
    assert change_base(64, 8) == '100'
    assert change_base(64, 10) == '64'


def test_base_3_conversions():
    """Test conversions to base 3."""
    from solution import change_base
    assert change_base(1, 3) == '1'
    assert change_base(2, 3) == '2'
    assert change_base(3, 3) == '10'
    assert change_base(4, 3) == '11'
    assert change_base(8, 3) == '22'
    assert change_base(9, 3) == '100'
    assert change_base(10, 3) == '101'
    assert change_base(27, 3) == '1000'
    assert change_base(80, 3) == '2222'


def test_base_8_conversions():
    """Test conversions to base 8 (octal)."""
    from solution import change_base
    assert change_base(7, 8) == '7'
    assert change_base(8, 8) == '10'
    assert change_base(64, 8) == '100'
    assert change_base(65, 8) == '101'
    assert change_base(100, 8) == '144'
    assert change_base(511, 8) == '777'
    assert change_base(512, 8) == '1000'


def test_base_9_conversions():
    """Test conversions to base 9."""
    from solution import change_base
    assert change_base(8, 9) == '8'
    assert change_base(9, 9) == '10'
    assert change_base(80, 9) == '88'
    assert change_base(81, 9) == '100'
    assert change_base(100, 9) == '121'


def test_larger_numbers():
    """Test with larger input values."""
    from solution import change_base
    assert change_base(1000, 2) == '1111101000'
    assert change_base(1000, 8) == '1750'
    assert change_base(1000, 10) == '1000'
    assert change_base(1023, 2) == '1111111111'
    assert change_base(1024, 2) == '10000000000'
    assert change_base(9999, 10) == '9999'
    assert change_base(10000, 10) == '10000'


def test_return_type():
    """Verify the return type is always a string."""
    from solution import change_base
    assert isinstance(change_base(0, 2), str)
    assert isinstance(change_base(1, 2), str)
    assert isinstance(change_base(100, 2), str)
    assert isinstance(change_base(1000, 10), str)


def test_consistency_with_python_format():
    """Cross-check against Python's built-in formatting for base 2, 8, 16."""
    from solution import change_base
    # For base 2
    for n in range(0, 100):
        assert change_base(n, 2) == bin(n)[2:]

    # For base 8
    for n in range(0, 100):
        assert change_base(n, 8) == oct(n)[2:]

    # For base 10
    for n in range(0, 100):
        assert change_base(n, 10) == str(n)
