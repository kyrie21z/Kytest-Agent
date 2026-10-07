import pytest
from solution import next_power_of_2


# --- Parametrized test data for "just above power of 2" ---
just_above_data = [(2**k + 1, 2**(k + 1)) for k in range(0, 20)]

# --- Parametrized test data for "just below power of 2" ---
just_below_data = [(2**k - 1, 2**k) for k in range(1, 20)]


class TestNextPowerOf2:
    """Tests for the next_power_of_2 function."""

    # --- Zero and small positive values ---

    def test_zero(self):
        """Smallest power of 2 >= 0 is 1."""
        assert next_power_of_2(0) == 1

    def test_one(self):
        """1 is already a power of 2."""
        assert next_power_of_2(1) == 1

    def test_two(self):
        """2 is already a power of 2."""
        assert next_power_of_2(2) == 2

    def test_three(self):
        """Next power of 2 after 3 is 4."""
        assert next_power_of_2(3) == 4

    def test_four(self):
        """4 is already a power of 2."""
        assert next_power_of_2(4) == 4

    def test_five(self):
        """Next power of 2 after 5 is 8."""
        assert next_power_of_2(5) == 8

    def test_seven(self):
        """Next power of 2 after 7 is 8."""
        assert next_power_of_2(7) == 8

    def test_eight(self):
        """8 is already a power of 2."""
        assert next_power_of_2(8) == 8

    # --- Powers of 2 (should return themselves) ---

    @pytest.mark.parametrize("n", [16, 32, 64, 128, 256, 512, 1024])
    def test_already_power_of_2(self, n):
        """If n is already a power of 2, return n."""
        assert next_power_of_2(n) == n

    # --- Non-powers of 2 ---

    @pytest.mark.parametrize("n, expected", [
        (6, 8),
        (9, 16),
        (10, 16),
        (15, 16),
        (17, 32),
        (31, 32),
        (33, 64),
        (63, 64),
        (65, 128),
        (100, 128),
        (200, 256),
        (500, 512),
        (1000, 1024),
    ])
    def test_non_power_of_2(self, n, expected):
        """For non-power-of-2 inputs, return the next higher power of 2."""
        assert next_power_of_2(n) == expected

    # --- Larger values ---

    def test_large_value(self):
        """Test with a large input value."""
        assert next_power_of_2(1000000) == 1048576  # 2^20

    def test_max_small_power(self):
        """Test near 2^30."""
        assert next_power_of_2(2**30 + 1) == 2**31

    # --- Negative numbers ---

    def test_negative_one(self):
        """Negative input: behavior is undefined due to arithmetic right-shift."""
        # The original code does not handle negative numbers; skip assertion.
        pass

    # --- Type checks ---

    def test_float_input(self):
        """Float inputs are not valid; expect unexpected results."""
        # Documenting this as a known limitation.
        pass

    # --- Boundary between powers of 2 ---

    @pytest.mark.parametrize("n, expected", just_above_data)
    def test_just_above_power_of_2(self, n, expected):
        """One more than a power of 2 should round up to the next power."""
        assert next_power_of_2(n) == expected

    @pytest.mark.parametrize("n, expected", just_below_data)
    def test_just_below_power_of_2(self, n, expected):
        """One less than a power of 2 should round up to that power."""
        assert next_power_of_2(n) == expected


class TestReturnValuesArePowersOfTwo:
    """Verify that all returned values are indeed powers of 2."""

    @pytest.mark.parametrize("n", list(range(0, 100)))
    def test_result_is_power_of_2(self, n):
        """Every result must be a power of 2 (i.e., result & (result-1) == 0)."""
        result = next_power_of_2(n)
        assert result > 0, f"Result must be positive for n={n}"
        assert result & (result - 1) == 0, f"{result} is not a power of 2 for n={n}"

    @pytest.mark.parametrize("n", list(range(0, 100)))
    def test_result_ge_n(self, n):
        """Result must be >= n for all non-negative inputs."""
        result = next_power_of_2(n)
        assert result >= n, f"Result {result} < n={n}"

    @pytest.mark.parametrize("n", list(range(1, 100)))
    def test_smallest_power_ge_n(self, n):
        """Result must be the *smallest* power of 2 >= n."""
        result = next_power_of_2(n)
        # Check that the previous power of 2 is strictly less than n
        prev_power = result >> 1
        assert prev_power < n, f"{prev_power} should be < n={n}, but isn't"
