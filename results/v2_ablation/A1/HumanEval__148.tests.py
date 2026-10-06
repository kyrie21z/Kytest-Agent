"""Unit tests for solution.bf().

The bf(planet1, planet2) function returns a tuple of planets whose orbits lie
between planet1 and planet2 (sorted by proximity to the Sun).  Planets are
ordered: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.

Test categories:
  1. Normal cases – typical inputs with clear expected outputs.
  2. Boundary cases – adjacent planets, same planet, first/last extremes.
  3. Empty / null / zero-size inputs.
  4. Invalid inputs – wrong names, case mismatch, non-string types.
  5. Exception cases – None, unexpected types that could raise.
"""

import pytest
from solution import bf


# ---------------------------------------------------------------------------
# Helper: ordered planet list used throughout
# ---------------------------------------------------------------------------
PLANETS = [
    "Mercury", "Venus", "Earth", "Mars",
    "Jupiter", "Saturn", "Uranus", "Neptune",
]


# ===========================================================================
# 1. Normal cases
# ===========================================================================
class TestNormalCases:
    """Typical inputs where both planets are valid."""

    def test_jupiter_to_neptune(self):
        result = bf("Jupiter", "Neptune")
        assert result == ("Saturn", "Uranus")

    def test_earth_to_mercury(self):
        # Reversed order should still work
        result = bf("Earth", "Mercury")
        assert result == ("Venus",)

    def test_mercury_to_uranus(self):
        result = bf("Mercury", "Uranus")
        assert result == ("Venus", "Earth", "Mars", "Jupiter", "Saturn")

    def test_venus_to_saturn(self):
        result = bf("Venus", "Saturn")
        assert result == ("Earth", "Mars", "Jupiter")

    def test_reverse_order_same_result(self):
        # Swapping arguments should yield the same result
        assert bf("Jupiter", "Neptune") == bf("Neptune", "Jupiter")
        assert bf("Earth", "Mercury") == bf("Mercury", "Earth")

    def test_neptune_to_mercury(self):
        result = bf("Neptune", "Mercury")
        assert result == tuple(PLANETS[1:-1])  # all except first & last

    def test_earth_to_mars(self):
        result = bf("Earth", "Mars")
        assert result == ()  # no planet between Earth and Mars


# ===========================================================================
# 2. Boundary cases
# ===========================================================================
class TestBoundaryCases:
    """Edge-of-range inputs."""

    def test_adjacent_planets_nothing_between(self):
        """Two planets next to each other in the solar system."""
        assert bf("Mercury", "Venus") == ()
        assert bf("Venus", "Earth") == ()
        assert bf("Earth", "Mars") == ()
        assert bf("Mars", "Jupiter") == ()
        assert bf("Jupiter", "Saturn") == ()
        assert bf("Saturn", "Uranus") == ()
        assert bf("Uranus", "Neptune") == ()

    def test_same_planet(self):
        """Both arguments are the same planet → empty tuple."""
        for planet in PLANETS:
            assert bf(planet, planet) == ()

    def test_first_and_last_planets(self):
        """Full range from Mercury to Neptune."""
        result = bf("Mercury", "Neptune")
        assert result == tuple(PLANETS[1:-1])

    def test_last_and_first_planets(self):
        """Reversed full range."""
        result = bf("Neptune", "Mercury")
        assert result == tuple(PLANETS[1:-1])

    def test_largest_gap_reversed(self):
        """Largest gap with reversed argument order."""
        result = bf("Neptune", "Mercury")
        assert len(result) == 6

    def test_smallest_valid_gap(self):
        """Smallest gap between any two distinct planets."""
        # Every adjacent pair should return empty tuple
        for i in range(len(PLANETS) - 1):
            assert bf(PLANETS[i], PLANETS[i + 1]) == ()


# ===========================================================================
# 3. Empty, null, or zero-size inputs
# ===========================================================================
class TestEmptyNullZeroSize:
    """Inputs that are empty, null, or zero-length."""

    def test_empty_string_both_args(self):
        result = bf("", "")
        assert result == ()

    def test_empty_string_first_arg(self):
        result = bf("", "Earth")
        assert result == ()

    def test_empty_string_second_arg(self):
        result = bf("Earth", "")
        assert result == ()

    def test_none_first_arg(self):
        result = bf(None, "Earth")
        assert result == ()

    def test_none_second_arg(self):
        result = bf("Earth", None)
        assert result == ()

    def test_none_both_args(self):
        result = bf(None, None)
        assert result == ()


# ===========================================================================
# 4. Invalid inputs
# ===========================================================================
class TestInvalidInputs:
    """Planet names that are not recognized."""

    def test_invalid_name_one_arg(self):
        result = bf("Pluto", "Earth")
        assert result == ()

    def test_invalid_name_other_arg(self):
        result = bf("Earth", "Pluto")
        assert result == ()

    def test_both_invalid_names(self):
        result = bf("Pluto", "Mars")
        assert result == ()

    def test_case_sensitive_lowercase(self):
        """Lowercase planet names should be treated as invalid."""
        assert bf("earth", "mercury") == ()

    def test_case_sensitive_mixed(self):
        """Mixed-case planet names should be treated as invalid."""
        assert bf("EARTH", "Mercury") == ()
        assert bf("earth", "MERCURY") == ()

    def test_typo_in_name(self):
        """Misspelled planet names."""
        assert bf("Mars", "Jupiter") == ()
        assert bf("Mart", "Jupiter") == ()

    def test_non_planet_word(self):
        assert bf("Alpha", "Beta") == ()
        assert bf("Sun", "Moon") == ()

    def test_numeric_input(self):
        """Integer inputs should not crash; treated as invalid."""
        assert bf(1, 2) == ()

    def test_list_input(self):
        """List input should not crash."""
        assert bf(["Earth"], ["Mars"]) == ()


# ===========================================================================
# 5. Exception cases
# ===========================================================================
class TestExceptionCases:
    """Inputs that might cause exceptions – verify none are raised."""

    def test_boolean_input(self):
        """Boolean values passed as arguments."""
        assert bf(True, False) == ()

    def test_dict_input(self):
        """Dictionary passed as argument."""
        assert bf({"name": "Earth"}, "Mars") == ()

    def test_tuple_input(self):
        """Tuple passed as argument."""
        assert bf(("Earth",), ("Mars",)) == ()

    def test_unicode_input(self):
        """Unicode characters as planet names."""
        assert bf("地球", "火星") == ()

    def test_whitespace_input(self):
        """Whitespace-only strings."""
        assert bf(" ", "Earth") == ()
        assert bf("\t\n", "Mars") == ()

    def test_long_string(self):
        """Very long string as argument."""
        assert bf("A" * 10000, "Earth") == ()

    def test_returns_tuple_type(self):
        """Verify the return type is always a tuple."""
        for p1, p2 in [
            ("Mercury", "Neptune"),
            ("Earth", "Mercury"),
            ("Pluto", "Earth"),
            ("", ""),
            (None, None),
        ]:
            result = bf(p1, p2)
            assert isinstance(result, tuple)
