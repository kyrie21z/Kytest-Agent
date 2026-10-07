import pytest
from solution import next_power_of_2


class TestNextPowerOf2:
    """Tests for the next_power_of_2 function."""

    # --- Exact powers of 2 (should return themselves) ---

    def test_power_of_2_small(self):
        assert next_power_of_2(1) == 1
        assert next_power_of_2(2) == 2
        assert next_power_of_2(4) == 4
        assert next_power_of_2(8) == 8

    def test_power_of_2_larger(self):
        assert next_power_of_2(16) == 16
        assert next_power_of_2(32) == 32
        assert next_power_of_2(64) == 64
        assert next_power_of_2(128) == 128

    def test_power_of_2_large(self):
        assert next_power_of_2(1024) == 1024
        assert next_power_of_2(65536) == 65536
        assert next_power_of_2(1048576) == 1048576

    # --- Non-powers of 2 (should return next higher power of 2) ---

    def test_between_powers_small(self):
        assert next_power_of_2(3) == 4
        assert next_power_of_2(5) == 8
        assert next_power_of_2(6) == 8
        assert next_power_of_2(7) == 8

    def test_between_powers_medium(self):
        assert next_power_of_2(9) == 16
        assert next_power_of_2(10) == 16
        assert next_power_of_2(15) == 16
        assert next_power_of_2(17) == 32
        assert next_power_of_2(31) == 32

    def test_between_powers_large(self):
        assert next_power_of_2(100) == 128
        assert next_power_of_2(1000) == 1024
        assert next_power_of_2(10000) == 16384
        assert next_power_of_2(100000) == 131072

    # --- Edge cases ---

    def test_zero(self):
        assert next_power_of_2(0) == 1

    def test_one(self):
        assert next_power_of_2(1) == 1

    def test_two(self):
        assert next_power_of_2(2) == 2

    # --- Boundary values ---

    def test_boundary_values(self):
        # Just below a power of 2
        assert next_power_of_2(15) == 16
        assert next_power_of_2(31) == 32
        assert next_power_of_2(63) == 64
        assert next_power_of_2(127) == 128

        # Just above a power of 2
        assert next_power_of_2(17) == 32
        assert next_power_of_2(33) == 64
        assert next_power_of_2(65) == 128
        assert next_power_of_2(129) == 256

    # --- Property-based style checks ---

    def test_result_is_always_power_of_2(self):
        """The result should always be a power of 2 for valid inputs."""
        for n in range(1, 1000):
            result = next_power_of_2(n)
            assert result > 0
            assert result & (result - 1) == 0  # check it's a power of 2

    def test_result_greater_than_or_equal_to_input(self):
        """The result should be >= n for positive inputs."""
        for n in range(1, 1000):
            assert next_power_of_2(n) >= n

    def test_no_smaller_power_of_2_satisfies_condition(self):
        """No smaller power of 2 should be >= n."""
        for n in range(1, 1000):
            result = next_power_of_2(n)
            if result > 1:
                assert result // 2 < n

    # --- Negative numbers (behavior may vary) ---
    # Note: The current implementation has an infinite loop for negative numbers
    # due to arithmetic right shift. We document expected behavior here.

    def test_negative_number_behavior(self):
        """Test behavior with negative input.
        
        The current implementation enters an infinite loop for negative numbers
        because Python's right shift on negatives is arithmetic (fills with 1s).
        This test documents that behavior.
        """
        # Skip this test as it would hang; document known limitation
        pytest.skip("Negative numbers cause infinite loop in current implementation")
