from solution import next_power_of_2


class TestNextPowerOf2:
    """Unit tests for the next_power_of_2 function."""

    # --- Basic positive integer cases ---

    def test_n_is_one(self):
        """1 is already a power of 2 (2^0), so should return 1."""
        assert next_power_of_2(1) == 1

    def test_n_is_two(self):
        """2 is already a power of 2 (2^1), so should return 2."""
        assert next_power_of_2(2) == 2

    def test_n_is_three(self):
        """3 is not a power of 2; next power is 4."""
        assert next_power_of_2(3) == 4

    def test_n_is_four(self):
        """4 is already a power of 2 (2^2), so should return 4."""
        assert next_power_of_2(4) == 4

    def test_n_is_five(self):
        """5 is not a power of 2; next power is 8."""
        assert next_power_of_2(5) == 8

    def test_n_is_seven(self):
        """7 is not a power of 2; next power is 8."""
        assert next_power_of_2(7) == 8

    def test_n_is_eight(self):
        """8 is already a power of 2 (2^3), so should return 8."""
        assert next_power_of_2(8) == 8

    def test_n_is_nine(self):
        """9 is not a power of 2; next power is 16."""
        assert next_power_of_2(9) == 16

    def test_n_is_twelve(self):
        """12 is not a power of 2; next power is 16."""
        assert next_power_of_2(12) == 16

    def test_n_is_fifteen(self):
        """15 is not a power of 2; next power is 16."""
        assert next_power_of_2(15) == 16

    def test_n_is_sixteen(self):
        """16 is already a power of 2 (2^4), so should return 16."""
        assert next_power_of_2(16) == 16

    # --- Larger values ---

    def test_n_is_100(self):
        """100 is not a power of 2; next power is 128."""
        assert next_power_of_2(100) == 128

    def test_n_is_1023(self):
        """1023 is not a power of 2; next power is 1024."""
        assert next_power_of_2(1023) == 1024

    def test_n_is_1024(self):
        """1024 is already a power of 2 (2^10), so should return 1024."""
        assert next_power_of_2(1024) == 1024

    def test_n_is_1025(self):
        """1025 is not a power of 2; next power is 2048."""
        assert next_power_of_2(1025) == 2048

    def test_large_n(self):
        """Test with a larger value near a power-of-2 boundary."""
        assert next_power_of_2(1 << 20) == (1 << 20)
        assert next_power_of_2((1 << 20) + 1) == (1 << 21)

    # --- Edge case: zero ---

    def test_n_is_zero(self):
        """0 is not a power of 2; the smallest power of 2 >= 0 is 1."""
        assert next_power_of_2(0) == 1

    # --- Boundary between powers of 2 ---

    def test_between_powers_of_two(self):
        """Values between two consecutive powers of 2 should round up."""
        # Between 2 and 4
        for i in range(3, 4):
            assert next_power_of_2(i) == 4
        # Between 4 and 8
        for i in range(5, 8):
            assert next_power_of_2(i) == 8
        # Between 8 and 16
        for i in range(9, 16):
            assert next_power_of_2(i) == 16

    # --- Return type check ---

    def test_return_type(self):
        """Ensure the return value is an integer."""
        assert isinstance(next_power_of_2(5), int)
        assert isinstance(next_power_of_2(0), int)

    # --- Property-based checks ---

    def test_result_is_power_of_two_for_positive_input(self):
        """For any positive n, the result should be a power of 2."""
        for n in range(1, 1000):
            result = next_power_of_2(n)
            assert result > 0
            assert result & (result - 1) == 0  # power of 2 check

    def test_result_greater_or_equal_to_input(self):
        """For any positive n, the result should be >= n."""
        for n in range(1, 1000):
            assert next_power_of_2(n) >= n
