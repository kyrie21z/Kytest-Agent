# Accepted by submit_tests; explanations in testgen_report.json.

from solution import next_power_of_2 as _case0_next_power_of_2

def test_power_of_two_returns_itself():
    """Verify that inputs which are exact powers of 2 are returned unchanged."""
    assert _case0_next_power_of_2(1) == 1
    assert _case0_next_power_of_2(2) == 2
    assert _case0_next_power_of_2(4) == 4
    assert _case0_next_power_of_2(8) == 8
    assert _case0_next_power_of_2(16) == 16
    assert _case0_next_power_of_2(1024) == 1024
    assert _case0_next_power_of_2(65536) == 65536

from solution import next_power_of_2 as _case1_next_power_of_2

def test_non_power_of_two_returns_next():
    """Verify that non-power-of-2 inputs map to the next higher power of 2."""
    assert _case1_next_power_of_2(3) == 4
    assert _case1_next_power_of_2(5) == 8
    assert _case1_next_power_of_2(6) == 8
    assert _case1_next_power_of_2(7) == 8
    assert _case1_next_power_of_2(9) == 16
    assert _case1_next_power_of_2(15) == 16
    assert _case1_next_power_of_2(17) == 32

from solution import next_power_of_2 as _case2_next_power_of_2

def test_zero_returns_one():
    """Verify that n=0 returns 1, since 2^0 = 1 is the smallest power of 2 >= 0."""
    assert _case2_next_power_of_2(0) == 1

from solution import next_power_of_2 as _case3_next_power_of_2

def test_large_values():
    """Verify correctness for large inputs near powers of 2 boundaries."""
    assert _case3_next_power_of_2(1048575) == 1048576
    assert _case3_next_power_of_2(1048576) == 1048576
    assert _case3_next_power_of_2(1048577) == 2097152
    assert _case3_next_power_of_2(2 ** 30 - 1) == 2 ** 30
    assert _case3_next_power_of_2(2 ** 30) == 2 ** 30
    assert _case3_next_power_of_2(2 ** 30 + 1) == 2 ** 31

from solution import next_power_of_2 as _case4_next_power_of_2

def test_return_type_is_int():
    """Verify that the function always returns an int for valid integer inputs."""
    result = _case4_next_power_of_2(7)
    assert isinstance(result, int)
    result = _case4_next_power_of_2(0)
    assert isinstance(result, int)
    result = _case4_next_power_of_2(1024)
    assert isinstance(result, int)
    result = _case4_next_power_of_2(2 ** 25)
    assert isinstance(result, int)

from solution import next_power_of_2 as _case5_next_power_of_2

def test_boundary_between_powers():
    """Test inputs that are exactly one less than a power of 2 (worst-case for ceiling)."""
    assert _case5_next_power_of_2(3) == 4
    assert _case5_next_power_of_2(7) == 8
    assert _case5_next_power_of_2(15) == 16
    assert _case5_next_power_of_2(31) == 32
    assert _case5_next_power_of_2(63) == 64
    assert _case5_next_power_of_2(127) == 128
    assert _case5_next_power_of_2(255) == 256
    assert _case5_next_power_of_2(511) == 512
