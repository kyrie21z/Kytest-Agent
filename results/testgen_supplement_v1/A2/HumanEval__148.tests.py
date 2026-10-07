"""Unit tests for solution.bf().

The bf(planet1, planet2) function returns a tuple of planets whose orbits lie
strictly between planet1 and planet2 (sorted by proximity to the Sun).
Valid planet names are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.
If either argument is not a valid planet name, an empty tuple is returned.
"""

import pytest
from solution import bf


# ---------------------------------------------------------------------------
# 1. Normal / typical input cases
# ---------------------------------------------------------------------------

class TestNormalCases:
    """Tests with well-known, valid planet names."""

    def test_jupiter_to_neptune(self):
        """Planets between Jupiter and Neptune (closer-to-farther ordering)."""
        assert bf("Jupiter", "Neptune") == ("Saturn", "Uranus")

    def test_earth_to_mercury(self):
        """Reversed ordering: Earth is farther; should still return Venus."""
        assert bf("Earth", "Mercury") == ("Venus",)

    def test_mercury_to_uranus(self):
        """From first to near-last planet."""
        assert bf("Mercury", "Uranus") == (
            "Venus", "Earth", "Mars", "Jupiter", "Saturn",
        )

    def test_saturn_to_jupiter(self):
        """Reversed: Saturn is farther than Jupiter; expect nothing between them."""
        assert bf("Saturn", "Jupiter") == ()

    def test_venus_to_mars(self):
        """Three consecutive planets in forward order."""
        assert bf("Venus", "Mars") == ("Earth",)

    def test_venus_to_mars_reversed(self):
        """Three consecutive planets in reverse order."""
        assert bf("Mars", "Venus") == ("Earth",)

    def test_earth_to_neptune(self):
        """From middle to last planet."""
        assert bf("Earth", "Neptune") == (
            "Mars", "Jupiter", "Saturn", "Uranus",
        )

    def test_neptune_to_earth(self):
        """From last to middle planet (reversed)."""
        assert bf("Neptune", "Earth") == (
            "Mars", "Jupiter", "Saturn", "Uranus",
        )

    def test_mercury_to_neptune(self):
        """Full range: first to last planet."""
        assert bf("Mercury", "Neptune") == (
            "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus",
        )

    def test_neptune_to_mercury(self):
        """Full range in reverse."""
        assert bf("Neptune", "Mercury") == (
            "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus",
        )


# ---------------------------------------------------------------------------
# 2. Boundary cases
# ---------------------------------------------------------------------------

class TestBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_adjacent_forward(self):
        """Adjacent planets (no planets between them)."""
        assert bf("Mercury", "Venus") == ()

    def test_adjacent_backward(self):
        """Adjacent planets in reverse order."""
        assert bf("Venus", "Mercury") == ()

    def test_adjacent_middle(self):
        """Adjacent planets somewhere in the middle (Mars & Jupiter have nothing between)."""
        assert bf("Mars", "Jupiter") == ()

    def test_adjacent_last_pair(self):
        """Last pair of adjacent planets."""
        assert bf("Uranus", "Neptune") == ()

    def test_same_planet(self):
        """Same planet passed as both arguments — no planets between."""
        assert bf("Earth", "Earth") == ()

    def test_first_and_second(self):
        """First two planets in the list."""
        assert bf("Mercury", "Venus") == ()

    def test_last_two(self):
        """Last two planets in the list."""
        assert bf("Uranus", "Neptune") == ()


# ---------------------------------------------------------------------------
# 3. Invalid inputs
# ---------------------------------------------------------------------------

class TestInvalidInputs:
    """Tests with invalid or non-existent planet names."""

    def test_invalid_planet1(self):
        """planet1 is not a valid planet name."""
        assert bf("Pluto", "Earth") == ()

    def test_invalid_planet2(self):
        """planet2 is not a valid planet name."""
        assert bf("Earth", "Pluto") == ()

    def test_both_invalid(self):
        """Both arguments are invalid."""
        assert bf("Pluto", "Krypton") == ()

    def test_empty_string_planet1(self):
        """Empty string for planet1."""
        assert bf("", "Earth") == ()

    def test_empty_string_planet2(self):
        """Empty string for planet2."""
        assert bf("Earth", "") == ()

    def test_empty_string_both(self):
        """Both arguments are empty strings."""
        assert bf("", "") == ()

    def test_wrong_case(self):
        """Planet names with incorrect casing."""
        assert bf("earth", "mars") == ()

    def test_uppercase_planet_name(self):
        """Fully uppercase planet name."""
        assert bf("EARTH", "MARS") == ()

    def test_mixed_case(self):
        """Mixed-case planet name."""
        assert bf("eArTh", "mArS") == ()

    def test_numeric_string(self):
        """Numeric-looking string."""
        assert bf("42", "99") == ()

    def test_whitespace(self):
        """String containing whitespace."""
        assert bf(" Earth ", " Mars ") == ()


# ---------------------------------------------------------------------------
# 4. Exception / edge-type inputs
# ---------------------------------------------------------------------------

class TestExceptionCases:
    """Tests that may raise exceptions or behave unexpectedly."""

    def test_none_input(self):
        """None passed as an argument."""
        # The function checks `planet1 not in planets`, which handles None gracefully.
        assert bf(None, "Earth") == ()

    def test_none_both(self):
        """Both arguments are None."""
        assert bf(None, None) == ()

    def test_integer_input(self):
        """Integer passed instead of a string."""
        assert bf(1, 2) == ()

    def test_list_input(self):
        """List passed instead of a string."""
        assert bf(["Earth"], ["Mars"]) == ()

    def test_tuple_input(self):
        """Tuple passed instead of a string."""
        assert bf(("Earth",), ("Mars",)) == ()

    def test_boolean_input(self):
        """Boolean values (True/False) as arguments."""
        assert bf(True, False) == ()

    def test_unicode_characters(self):
        """Unicode characters as planet names."""
        assert bf("地球", "火星") == ()

    def test_long_string(self):
        """Very long string as planet name."""
        assert bf("A" * 1000, "B" * 1000) == ()


# ---------------------------------------------------------------------------
# 5. Return type verification
# ---------------------------------------------------------------------------

class TestReturnType:
    """Verify that the return value is always a tuple."""

    def test_returns_tuple_normal(self):
        result = bf("Jupiter", "Neptune")
        assert isinstance(result, tuple)

    def test_returns_tuple_empty(self):
        result = bf("Mercury", "Venus")
        assert isinstance(result, tuple)

    def test_returns_tuple_invalid(self):
        result = bf("Pluto", "Earth")
        assert isinstance(result, tuple)

    def test_returns_tuple_single_element(self):
        result = bf("Venus", "Mars")
        assert isinstance(result, tuple)
        assert len(result) == 1

    def test_returns_tuple_full_range(self):
        result = bf("Mercury", "Neptune")
        assert isinstance(result, tuple)
        assert len(result) == 6
