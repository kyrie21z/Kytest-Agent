"""Unit tests for the is_prime function in solution.py."""

import pytest
from solution import is_prime


# ---------------------------------------------------------------------------
# 1. Normal cases – typical prime and composite inputs
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Tests with typical, expected inputs."""

    # --- Primes ---
    @pytest.mark.parametrize("n, expected", [
        (2, True),
        (3, True),
        (5, True),
        (7, True),
        (11, True),
        (13, True),
        (17, True),
        (19, True),
        (23, True),
        (29, True),
        (31, True),
        (37, True),
        (41, True),
        (43, True),
        (47, True),
        (53, True),
        (59, True),
        (61, True),
        (67, True),
        (71, True),
        (73, True),
        (79, True),
        (83, True),
        (89, True),
        (97, True),
        (101, True),
        (13441, True),
    ])
    def test_primes(self, n, expected):
        assert is_prime(n) == expected

    # --- Composites ---
    @pytest.mark.parametrize("n, expected", [
        (4, False),
        (6, False),
        (8, False),
        (9, False),
        (10, False),
        (12, False),
        (14, False),
        (15, False),
        (16, False),
        (18, False),
        (20, False),
        (21, False),
        (22, False),
        (24, False),
        (25, False),
        (26, False),
        (27, False),
        (28, False),
        (30, False),
        (33, False),
        (34, False),
        (35, False),
        (36, False),
        (38, False),
        (39, False),
        (40, False),
        (42, False),
        (44, False),
        (45, False),
        (46, False),
        (48, False),
        (49, False),
        (50, False),
        (51, False),
        (52, False),
        (54, False),
        (55, False),
        (56, False),
        (57, False),
        (58, False),
        (60, False),
        (62, False),
        (63, False),
        (64, False),
        (65, False),
        (66, False),
        (68, False),
        (69, False),
        (70, False),
        (72, False),
        (74, False),
        (75, False),
        (76, False),
        (77, False),
        (78, False),
        (80, False),
        (81, False),
        (82, False),
        (84, False),
        (85, False),
        (86, False),
        (87, False),
        (88, False),
        (90, False),
        (91, False),
        (92, False),
        (93, False),
        (94, False),
        (95, False),
        (96, False),
        (98, False),
        (99, False),
        (100, False),
    ])
    def test_composites(self, n, expected):
        assert is_prime(n) == expected


# ---------------------------------------------------------------------------
# 2. Boundary cases – edges of the valid input range
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Tests at the boundaries of the input domain."""

    @pytest.mark.parametrize("n, expected", [
        (0, False),   # lowest non-negative boundary
        (1, False),   # explicitly not prime (per docstring)
        (2, True),    # smallest prime
        (3, True),    # second smallest prime
    ])
    def test_boundaries(self, n, expected):
        assert is_prime(n) == expected


# ---------------------------------------------------------------------------
# 3. Larger / less common inputs
# ---------------------------------------------------------------------------

class TestLargerInputs:
    """Tests with larger numbers to exercise the sqrt-based loop."""

    @pytest.mark.parametrize("n, expected", [
        (997, True),       # largest 3-digit prime
        (1000, False),     # round number, composite
        (1001, False),     # 7 × 11 × 13
        (1009, True),      # prime just above 1000
        (10000, False),    # round number
        (10007, True),     # prime just above 10000
        (100000, False),   # round number
        (100003, True),    # prime just above 100000
        (13441, True),     # from docstring
    ])
    def test_larger_numbers(self, n, expected):
        assert is_prime(n) == expected


# ---------------------------------------------------------------------------
# 4. Invalid inputs – negative numbers
# ---------------------------------------------------------------------------

class TestNegativeInputs:
    """Negative integers are not prime."""

    @pytest.mark.parametrize("n", [-1, -2, -3, -5, -10, -100, -1000])
    def test_negative_numbers(self, n):
        assert is_prime(n) is False


# ---------------------------------------------------------------------------
# 5. Exception cases – unsupported types that will raise TypeError
# ---------------------------------------------------------------------------

class TestInvalidTypes:
    """Passing truly unsupported types should raise an exception."""

    @pytest.mark.parametrize("invalid_input", [
        None,
        "hello",
        "",
        [2],
        {"key": "value"},
        (2,),
        b"bytes",
    ])
    def test_unsupported_type_raises_error(self, invalid_input):
        with pytest.raises(TypeError):
            is_prime(invalid_input)
