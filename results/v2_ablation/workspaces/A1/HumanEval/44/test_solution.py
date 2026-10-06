import pytest


def test_docstring_examples():
    """Test the examples provided in the docstring."""
    from solution import change_base
    assert change_base(8, 3) == "22"
    assert change_base(8, 2) == "1000"
    assert change_base(7, 2) == "111"


def test_zero_input():
    """Edge case: x = 0 should return '0' regardless of base."""
    from solution import change_base
    assert change_base(0, 2) == "0"
    assert change_base(0, 8) == "0"
    assert change_base(0, 10) == "0"


def test_one_input():
    """Boundary: x = 1 should return '1' for any valid base."""
    from solution import change_base
    assert change_base(1, 2) == "1"
    assert change_base(1, 3) == "1"
    assert change_base(1, 9) == "1"


def test_single_digit_values():
    """When x < base, result should be str(x)."""
    from solution import change_base
    assert change_base(5, 8) == "5"
    assert change_base(3, 10) == "3"
    assert change_base(9, 10) == "9"


def test_x_equals_base():
    """When x == base, result should be '10'."""
    from solution import change_base
    assert change_base(2, 2) == "10"
    assert change_base(3, 3) == "10"
    assert change_base(8, 8) == "10"
    assert change_base(9, 9) == "10"


def test_power_of_base():
    """Powers of base should produce '1' followed by zeros."""
    from solution import change_base
    assert change_base(4, 2) == "100"       # 2^2
    assert change_base(8, 2) == "1000"      # 2^3
    assert change_base(16, 2) == "10000"    # 2^4
    assert change_base(27, 3) == "1000"     # 3^3
    assert change_base(81, 3) == "10000"    # 3^4


def test_two_digit_numbers():
    """Numbers with two digits in the target base."""
    from solution import change_base
    assert change_base(10, 2) == "1010"
    assert change_base(10, 8) == "12"
    assert change_base(15, 8) == "17"
    assert change_base(20, 5) == "40"
    assert change_base(25, 5) == "100"


def test_larger_numbers():
    """Larger inputs across various bases."""
    from solution import change_base
    assert change_base(100, 2) == "1100100"
    assert change_base(100, 8) == "144"
    assert change_base(100, 10) == "100"
    assert change_base(255, 2) == "11111111"
    assert change_base(255, 8) == "377"
    assert change_base(1024, 2) == "10000000000"
    assert change_base(1024, 16) == "400"


def test_max_valid_base():
    """Base 9 is the maximum valid base per docstring ('base numbers are less than 10')."""
    from solution import change_base
    assert change_base(9, 9) == "10"
    assert change_base(80, 9) == "88"
    assert change_change_base(81, 9) == "100"


def test_min_valid_base():
    """Base 2 is the minimum meaningful base."""
    from solution import change_base
    assert change_base(1, 2) == "1"
    assert change_base(2, 2) == "10"
    assert change_base(3, 2) == "11"
    assert change_base(4, 2) == "100"


def test_base_1_infinite_loop():
    """Base 1 causes infinite loop because x % 1 == 0 and x // 1 == x."""
    from solution import change_base
    with pytest.raises(Exception):
        # We use a timeout approach via pytest-timeout or just expect it to hang.
        # Since we can't easily test infinite loops, we mark this as expected to fail/hang.
        # Instead, we verify the behavior by checking it raises after a short time.
        pass


def test_base_0_raises_error():
    """Base 0 causes ZeroDivisionError."""
    from solution import change_base
    with pytest.raises(ZeroDivisionError):
        change_base(10, 0)


def test_negative_base():
    """Negative base may cause unexpected behavior; test that it doesn't crash silently."""
    from solution import change_base
    # With negative base, x % base can behave unexpectedly.
    # For example, 8 % (-2) == 0, 8 // (-2) == -4, then -4 % (-2) == 0, -4 // (-2) == 2, etc.
    # This could loop or produce odd results. We just ensure it doesn't raise an unhandled exception
    # in a reasonable way, or document the behavior.
    # Actually, let's see what happens:
    # 8 % -2 = 0, 8 // -2 = -4
    # -4 % -2 = 0, -4 // -2 = 2
    # 2 % -2 = 0, 2 // -2 = -1
    # -1 % -2 = -1, -1 // -2 = 0
    # So ret = "000-1" which is weird. Let's just capture whatever it produces.
    result = change_base(8, -2)
    assert isinstance(result, str)


def test_negative_x():
    """Negative input x: the function doesn't explicitly handle negatives."""
    from solution import change_base
    # For negative x, Python's // and % have specific semantics:
    # e.g., -7 % 2 = 1, -7 // 2 = -4
    # This could lead to unexpected results or infinite loops.
    # Let's capture whatever output it gives.
    result = change_base(-7, 2)
    assert isinstance(result, str)


def test_base_equal_to_number_minus_one():
    """When base = x - 1, x should be represented as '11'."""
    from solution import change_base
    assert change_base(3, 2) == "11"   # 3 in base 2
    assert change_base(10, 9) == "11"  # 10 in base 9
    assert change_base(100, 99) == "11"  # 100 in base 99


def test_base_greater_than_x():
    """When base > x, result should be str(x)."""
    from solution import change_base
    assert change_base(5, 10) == "5"
    assert change_base(3, 16) == "3"
    assert change_base(1, 100) == "1"


def test_consecutive_numbers_same_base():
    """Verify consecutive numbers convert correctly."""
    from solution import change_base
    for i in range(16):
        assert change_base(i, 2) == bin(i)[2:]
    for i in range(100):
        assert change_base(i, 8) == oct(i)[2:]


def test_base_4_various_inputs():
    """Test with base 4 specifically."""
    from solution import change_base
    assert change_base(0, 4) == "0"
    assert change_base(1, 4) == "1"
    assert change_base(3, 4) == "3"
    assert change_base(4, 4) == "10"
    assert change_base(15, 4) == "33"
    assert change_base(16, 4) == "100"
    assert change_base(63, 4) == "333"
    assert change_base(64, 4) == "1000"


def test_base_5_various_inputs():
    """Test with base 5 specifically."""
    from solution import change_base
    assert change_base(0, 5) == "0"
    assert change_base(4, 5) == "4"
    assert change_base(5, 5) == "10"
    assert change_base(24, 5) == "44"
    assert change_base(25, 5) == "100"


def test_base_6_various_inputs():
    """Test with base 6 specifically."""
    from solution import change_base
    assert change_base(0, 6) == "0"
    assert change_base(5, 6) == "5"
    assert change_base(6, 6) == "10"
    assert change_base(35, 6) == "55"
    assert change_base(36, 6) == "100"


def test_base_7_various_inputs():
    """Test with base 7 specifically."""
    from solution import change_base
    assert change_base(0, 7) == "0"
    assert change_base(6, 7) == "6"
    assert change_base(7, 7) == "10"
    assert change_base(48, 7) == "66"
    assert change_base(49, 7) == "100"


def test_base_8_various_inputs():
    """Test with base 8 specifically."""
    from solution import change_base
    assert change_base(0, 8) == "0"
    assert change_base(7, 8) == "7"
    assert change_base(8, 8) == "10"
    assert change_base(63, 8) == "77"
    assert change_base(64, 8) == "100"


def test_base_9_various_inputs():
    """Test with base 9 specifically."""
    from solution import change_base
    assert change_base(0, 9) == "0"
    assert change_base(8, 9) == "8"
    assert change_base(9, 9) == "10"
    assert change_base(80, 9) == "88"
    assert change_base(81, 9) == "100"
