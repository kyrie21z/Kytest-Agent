import pytest
from solution import f


class TestF:
    """Tests for the function f(n)."""

    # --- Edge cases ---

    def test_zero(self):
        """n=0 should return an empty list."""
        assert f(0) == []

    def test_one(self):
        """n=1 should return [1]."""
        assert f(1) == [1]

    def test_two(self):
        """n=2 should return [1, 2]."""
        assert f(2) == [1, 2]

    # --- Provided example ---

    def test_example_n5(self):
        """The docstring example: f(5) == [1, 2, 6, 24, 15]."""
        assert f(5) == [1, 2, 6, 24, 15]

    # --- Correctness for small n ---

    def test_n_3(self):
        """i=1→sum(1)=1, i=2→fact(2)=2, i=3→sum(3)=6."""
        assert f(3) == [1, 2, 6]

    def test_n_4(self):
        """i=1→1, i=2→2, i=3→6, i=4→fact(4)=24."""
        assert f(4) == [1, 2, 6, 24]

    def test_n_6(self):
        """Extends f(5) with i=6→fact(6)=720."""
        assert f(6) == [1, 2, 6, 24, 15, 720]

    def test_n_7(self):
        """Extends f(6) with i=7→sum(7)=28."""
        assert f(7) == [1, 2, 6, 24, 15, 720, 28]

    # --- Odd-index values are sums 1..i ---

    @pytest.mark.parametrize("i,expected", [
        (1, 1),
        (3, 6),
        (5, 15),
        (7, 28),
        (9, 45),
        (11, 66),
    ])
    def test_odd_index_sum(self, i, expected):
        """For odd i, element at index i-1 should be sum(1..i)."""
        result = f(i)
        assert result[i - 1] == expected

    # --- Even-index values are factorials ---

    @pytest.mark.parametrize("i,expected", [
        (2, 2),
        (4, 24),
        (6, 720),
        (8, 40320),
        (10, 3628800),
    ])
    def test_even_index_factorial(self, i, expected):
        """For even i, element at index i-1 should be factorial(i)."""
        result = f(i)
        assert result[i - 1] == expected

    # --- Return type and length ---

    def test_returns_list(self):
        """f should always return a list."""
        assert isinstance(f(5), list)

    def test_length_equals_n(self):
        """The returned list must have exactly n elements."""
        for n in range(0, 11):
            assert len(f(n)) == n

    # --- Larger inputs ---

    def test_n_10(self):
        """Verify a larger input manually."""
        # i=1→1, 2→2, 3→6, 4→24, 5→15, 6→720, 7→28, 8→40320, 9→45, 10→3628800
        assert f(10) == [1, 2, 6, 24, 15, 720, 28, 40320, 45, 3628800]

    def test_n_15(self):
        """Test with n=15 to exercise more iterations."""
        result = f(15)
        assert len(result) == 15
        # Check a few known values
        assert result[0] == 1   # i=1, sum=1
        assert result[1] == 2   # i=2, fact=2
        assert result[4] == 15  # i=5, sum=15
        assert result[9] == 3628800  # i=10, fact=10!
