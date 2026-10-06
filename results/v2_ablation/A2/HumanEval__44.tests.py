import pytest


def test_docstring_examples():
    """Test the examples from the docstring."""
    from solution import change_base
    assert change_base(8, 3) == '22'
    assert change_base(8, 2) == '1000'
    assert change_base(7, 2) == '111'


def test_zero_input():
    """Zero should return '0' regardless of base."""
    from solution import change_base
    assert change_base(0, 2) == '0'
    assert change_base(0, 3) == '0'
    assert change_base(0, 9) == '0'


def test_single_digit_values():
    """Numbers smaller than the base should return as a single digit."""
    from solution import change_base
    assert change_base(1, 2) == '1'
    assert change_base(1, 5) == '1'
    assert change_base(1, 9) == '1'
    assert change_base(5, 6) == '5'
    assert change_base(9, 10) == '9'


def test_base_equals_number():
    """A number equal to its base should be '10' in that base."""
    from solution import change_base
    assert change_base(2, 2) == '10'
    assert change_base(3, 3) == '10'
    assert change_base(5, 5) == '10'
    assert change_base(9, 9) == '10'


def test_power_of_two():
    """Powers of two should produce clean binary representations."""
    from solution import change_base
    assert change_base(1, 2) == '1'
    assert change_base(2, 2) == '10'
    assert change_base(4, 2) == '100'
    assert change_base(8, 2) == '1000'
    assert change_base(16, 2) == '10000'
    assert change_base(32, 2) == '100000'
    assert change_base(64, 2) == '1000000'
    assert change_base(128, 2) == '10000000'
    assert change_base(256, 2) == '100000000'
    assert change_base(1024, 2) == '10000000000'


def test_various_bases():
    """Test conversion across different valid bases."""
    from solution import change_base
    # Decimal 10
    assert change_base(10, 2) == '1010'
    assert change_base(10, 3) == '101'
    assert change_base(10, 4) == '22'
    assert change_base(10, 5) == '20'
    assert change_base(10, 6) == '14'
    assert change_base(10, 7) == '13'
    assert change_base(10, 8) == '12'
    assert change_base(10, 9) == '11'

    # Decimal 100
    assert change_base(100, 2) == '1100100'
    assert change_base(100, 3) == '10201'
    assert change_base(100, 4) == '1210'
    assert change_base(100, 5) == '400'
    assert change_base(100, 6) == '244'
    assert change_base(100, 7) == '202'
    assert change_base(100, 8) == '144'
    assert change_base(100, 9) == '121'

    # Decimal 255
    assert change_base(255, 2) == '11111111'
    assert change_base(255, 3) == '100110'
    assert change_base(255, 4) == '3333'
    assert change_base(255, 5) == '2010'
    assert change_base(255, 6) == '1103'
    assert change_base(255, 7) == '513'
    assert change_base(255, 8) == '377'
    assert change_base(255, 9) == '313'


def test_larger_numbers():
    """Test with larger input values."""
    from solution import change_base
    assert change_base(1000, 2) == '1111101000'
    assert change_base(1000, 3) == '1101001'
    assert change_base(1000, 4) == '33220'
    assert change_base(1000, 5) == '13000'
    assert change_base(1000, 6) == '4344'
    assert change_base(1000, 7) == '2626'
    assert change_base(1000, 8) == '1750'
    assert change_base(1000, 9) == '1331'


def test_boundary_max_base():
    """Base 9 is the maximum valid base per the docstring."""
    from solution import change_base
    assert change_base(9, 9) == '10'
    assert change_base(80, 9) == '88'
    assert change_base(81, 9) == '100'


def test_invalid_base_zero():
    """Base 0 should raise ZeroDivisionError."""
    from solution import change_base
    with pytest.raises(ZeroDivisionError):
        change_base(10, 0)


def test_return_type_is_string():
    """The return value should always be a string."""
    from solution import change_base
    assert isinstance(change_base(0, 2), str)
    assert isinstance(change_base(8, 2), str)
    assert isinstance(change_base(100, 5), str)
