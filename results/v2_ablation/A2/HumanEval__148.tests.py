"""Unit tests for solution.bf() — planets between two given orbits."""

import pytest
from solution import bf


# ── Normal / typical cases ────────────────────────────────────────────────

class TestNormalCases:
    """Typical inputs exercising the documented examples and common pairs."""

    def test_jupiter_to_neptune(self):
        """Documented example: Jupiter → Neptune."""
        assert bf("Jupiter", "Neptune") == ("Saturn", "Uranus")

    def test_earth_to_mercury(self):
        """Documented example: Earth → Mercury (reversed order)."""
        assert bf("Earth", "Mercury") == ("Venus",)

    def test_mercury_to_uranus(self):
        """Documented example: Mercury → Uranus."""
        assert bf("Mercury", "Uranus") == (
            "Venus", "Earth", "Mars", "Jupiter", "Saturn"
        )

    def test_neptune_to_mercury(self):
        """Reversed extreme: outermost → innermost."""
        assert bf("Neptune", "Mercury") == (
            "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus"
        )

    def test_venus_to_saturn(self):
        """Middle-to-middle pair."""
        assert bf("Venus", "Saturn") == (
            "Earth", "Mars", "Jupiter"
        )

    def test_saturn_to_venus(self):
        """Same pair but reversed argument order."""
        assert bf("Saturn", "Venus") == (
            "Earth", "Mars", "Jupiter"
        )

    def test_mars_to_earth(self):
        """Adjacent-ish pair with one planet between."""
        assert bf("Mars", "Earth") == ()

    def test_earth_to_mars(self):
        """Adjacent planets in forward order."""
        assert bf("Earth", "Mars") == ()


# ── Boundary cases ────────────────────────────────────────────────────────

class TestBoundaryCases:
    """Edges of valid input ranges."""

    def test_adjacent_forward(self):
        """Two consecutive planets — nothing between."""
        assert bf("Mercury", "Venus") == ()

    def test_adjacent_backward(self):
        """Two consecutive planets reversed — nothing between."""
        assert bf("Venus", "Mercury") == ()

    def test_same_planet(self):
        """Both arguments refer to the same planet."""
        assert bf("Earth", "Earth") == ()

    def test_full_range(self):
        """Innermost to outermost: everything except endpoints."""
        assert bf("Mercury", "Neptune") == (
            "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus"
        )

    def test_full_range_reversed(self):
        """Outermost to innermost: same result."""
        assert bf("Neptune", "Mercury") == (
            "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus"
        )

    def test_inner_pair(self):
        """Closest planets to the Sun."""
        assert bf("Mercury", "Earth") == ("Venus",)

    def test_outer_pair(self):
        """Farthest planets from the Sun."""
        assert bf("Uranus", "Neptune") == ()


# ── Empty / null / zero-size inputs ───────────────────────────────────────

class TestEmptyOrNullInputs:
    """Edge cases involving empty strings, None, etc."""

    def test_empty_string_first_arg(self):
        assert bf("", "Earth") == ()

    def test_empty_string_second_arg(self):
        assert bf("Earth", "") == ()

    def test_both_empty_strings(self):
        assert bf("", "") == ()

    def test_none_first_arg(self):
        assert bf(None, "Earth") == ()

    def test_none_second_arg(self):
        assert bf("Earth", None) == ()

    def test_both_none(self):
        assert bf(None, None) == ()


# ── Invalid inputs ────────────────────────────────────────────────────────

class TestInvalidInputs:
    """Planet names that are not recognized."""

    @pytest.mark.parametrize("invalid_name", [
        "Pluto",
        "Moon",
        "Sun",
        "Kepler-442b",
        "pluto",          # lowercase
        "EARTH",          # uppercase
        "mercury ",       # trailing space
        " mercury",       # leading space
        "Mer cury",       # embedded space
        "Mercuryx",       # typo
        "Venu",           # truncated
    ])
    def test_invalid_first_arg(self, invalid_name):
        assert bf(invalid_name, "Earth") == ()

    @pytest.mark.parametrize("invalid_name", [
        "Pluto",
        "Moon",
        "Sun",
        "pluto",
        "EARTH",
        "mercury ",
        "Mercuryx",
    ])
    def test_invalid_second_arg(self, invalid_name):
        assert bf("Earth", invalid_name) == ()

    @pytest.mark.parametrize("pair", [
        ("Pluto", "Mars"),
        ("Moon", "Sun"),
        ("Kepler-442b", "Neptune"),
    ])
    def test_both_invalid(self, pair):
        assert bf(*pair) == ()


# ── Non-string types ──────────────────────────────────────────────────────

class TestNonStringTypes:
    """Arguments that are not strings at all."""

    @pytest.mark.parametrize("bad_value", [
        0,
        42,
        3.14,
        [],
        {},
        set(),
        True,
        False,
    ])
    def test_non_string_first_arg(self, bad_value):
        assert bf(bad_value, "Earth") == ()

    @pytest.mark.parametrize("bad_value", [
        0,
        42,
        3.14,
        [],
        {},
        set(),
        True,
        False,
    ])
    def test_non_string_second_arg(self, bad_value):
        assert bf("Earth", bad_value) == ()


# ── Return-type checks ────────────────────────────────────────────────────

class TestReturnType:
    """Verify the function always returns a tuple."""

    @pytest.mark.parametrize("p1, p2", [
        ("Mercury", "Neptune"),
        ("Earth", "Mars"),
        ("Pluto", "Earth"),
        ("", "Earth"),
        (None, "Earth"),
    ])
    def test_returns_tuple(self, p1, p2):
        result = bf(p1, p2)
        assert isinstance(result, tuple)
