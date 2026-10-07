"""Unit tests for bf() in solution.py."""

import pytest
from solution import bf


class TestBfNormalCases:
    """Tests with typical valid planet name pairs."""

    def test_jupiter_to_neptune(self):
        """Planets between Jupiter and Neptune: Saturn, Uranus."""
        result = bf("Jupiter", "Neptune")
        assert result == ("Saturn", "Uranus")

    def test_earth_to_mercury_reversed(self):
        """When planet1 is farther from Sun than planet2, still returns
        planets between them sorted by proximity to Sun."""
        result = bf("Earth", "Mercury")
        assert result == ("Venus",)

    def test_mercury_to_uranus(self):
        """All planets between Mercury and Uranus."""
        result = bf("Mercury", "Uranus")
        assert result == ("Venus", "Earth", "Mars", "Jupiter", "Saturn")

    def test_venus_to_saturn(self):
        """Planets between Venus and Saturn."""
        result = bf("Venus", "Saturn")
        assert result == ("Earth", "Mars", "Jupiter")

    def test_mars_to_earth(self):
        """Reversed order: Mars to Earth yields no planets between them
        since they are adjacent (Earth=idx2, Mars=idx3)."""
        result = bf("Mars", "Earth")
        assert result == ()

    def test_saturn_to_jupiter(self):
        """Reversed order: Saturn to Jupiter yields no planets between
        since they are adjacent (Jupiter=idx4, Saturn=idx5)."""
        result = bf("Saturn", "Jupiter")
        assert result == ()


class TestBfBoundaryCases:
    """Tests at the edges of valid input ranges."""

    def test_adjacent_planets_mercury_venus(self):
        """Adjacent planets with nothing between them."""
        result = bf("Mercury", "Venus")
        assert result == ()

    def test_adjacent_planets_venus_earth(self):
        """Adjacent planets with nothing between them."""
        result = bf("Venus", "Earth")
        assert result == ()

    def test_adjacent_planets_neptune_u_ranus(self):
        """Adjacent planets: Uranus to Neptune."""
        result = bf("Uranus", "Neptune")
        assert result == ()

    def test_first_to_last_all_between(self):
        """First and last planets: all 6 intermediate planets."""
        result = bf("Mercury", "Neptune")
        assert result == ("Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus")

    def test_same_planet(self):
        """Same planet for both arguments returns empty tuple."""
        result = bf("Earth", "Earth")
        assert result == ()

    def test_last_to_first_reversed(self):
        """Neptune to Mercury reversed: all 6 intermediate planets."""
        result = bf("Neptune", "Mercury")
        assert result == ("Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus")


class TestBfInvalidInputs:
    """Tests with invalid or non-existent planet names."""

    def test_invalid_planet1(self):
        """planet1 is not a valid planet name."""
        result = bf("Pluto", "Earth")
        assert result == ()

    def test_invalid_planet2(self):
        """planet2 is not a valid planet name."""
        result = bf("Earth", "Pluto")
        assert result == ()

    def test_both_invalid(self):
        """Both planet names are invalid."""
        result = bf("Pluto", "Mars")
        assert result == ()

    def test_completely_fake_name(self):
        """A random string that is not any planet."""
        result = bf("AlphaCentauri", "BetaPictoris")
        assert result == ()

    def test_empty_string_planet1(self):
        """Empty string for planet1."""
        result = bf("", "Earth")
        assert result == ()

    def test_empty_string_planet2(self):
        """Empty string for planet2."""
        result = bf("Earth", "")
        assert result == ()

    def test_both_empty_strings(self):
        """Both arguments are empty strings."""
        result = bf("", "")
        assert result == ()


class TestBfCaseSensitivity:
    """Tests for case sensitivity — the function uses exact string matching."""

    def test_lowercase_planet_names(self):
        """Lowercase planet names should be treated as invalid."""
        result = bf("jupiter", "neptune")
        assert result == ()

    def test_mixed_case(self):
        """Mixed case planet names should be treated as invalid."""
        result = bf("JUPITER", "neptune")
        assert result == ()

    def test_title_case_valid(self):
        """Correct title-case planet names should work."""
        result = bf("Jupiter", "Neptune")
        assert result == ("Saturn", "Uranus")


class TestBfReturnType:
    """Tests verifying the return type is always a tuple."""

    def test_returns_tuple_normal(self):
        """Normal case returns a tuple."""
        result = bf("Mercury", "Uranus")
        assert isinstance(result, tuple)

    def test_returns_tuple_empty_result(self):
        """Empty result still returns a tuple (not a list or other type)."""
        result = bf("Mercury", "Venus")
        assert isinstance(result, tuple)

    def test_returns_tuple_invalid_input(self):
        """Invalid input returns an empty tuple."""
        result = bf("Pluto", "Earth")
        assert isinstance(result, tuple)

    def test_single_element_is_tuple(self):
        """Single-element result is still a tuple."""
        result = bf("Earth", "Mercury")
        assert isinstance(result, tuple)
        assert len(result) == 1
