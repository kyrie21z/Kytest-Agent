"""Unit tests for solution.bf function."""

import pytest
from solution import bf


class TestNormalCases:
    """Test typical valid inputs."""

    def test_jupiter_to_neptune(self):
        """Planets between Jupiter and Neptune (closer to farther)."""
        assert bf("Jupiter", "Neptune") == ("Saturn", "Uranus")

    def test_earth_to_mercury(self):
        """Planets between Earth and Mercury (farther to closer)."""
        assert bf("Earth", "Mercury") == ("Venus",)

    def test_mercury_to_uranus(self):
        """Planets between Mercury and Uranus."""
        assert bf("Mercury", "Uranus") == (
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
        )

    def test_mercury_to_neptune(self):
        """Planets between Mercury and Neptune (first and last)."""
        assert bf("Mercury", "Neptune") == (
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
        )

    def test_neptune_to_mercury_reversed(self):
        """Reversed order: Neptune to Mercury should give same result."""
        assert bf("Neptune", "Mercury") == (
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
        )

    def test_venus_to_earth(self):
        """Adjacent planets: Venus to Earth."""
        assert bf("Venus", "Earth") == ()

    def test_earth_to_venus_reversed(self):
        """Adjacent planets reversed: Earth to Venus."""
        assert bf("Earth", "Venus") == ()

    def test_saturn_to_jupiter(self):
        """Adjacent planets reversed: Saturn to Jupiter."""
        assert bf("Saturn", "Jupiter") == ()

    def test_mars_to_saturn(self):
        """Single planet between Mars and Saturn."""
        assert bf("Mars", "Saturn") == ("Jupiter",)

    def test_saturn_to_mars_reversed(self):
        """Single planet between Saturn and Mars (reversed)."""
        assert bf("Saturn", "Mars") == ("Jupiter",)

    def test_venus_to_mars(self):
        """Two planets between Venus and Mars."""
        assert bf("Venus", "Mars") == ("Earth",)

    def test_mars_to_venus_reversed(self):
        """Two planets between Mars and Venus (reversed)."""
        assert bf("Mars", "Venus") == ("Earth",)

    def test_uranus_to_saturn(self):
        """Adjacent planets: Uranus to Saturn."""
        assert bf("Uranus", "Saturn") == ()

    def test_saturn_to_uranus_reversed(self):
        """Adjacent planets reversed: Saturn to Uranus."""
        assert bf("Saturn", "Uranus") == ()


class TestBoundaryCases:
    """Test edge cases at boundaries of valid input ranges."""

    def test_same_planet(self):
        """Same planet for both arguments yields empty tuple."""
        assert bf("Mercury", "Mercury") == ()
        assert bf("Earth", "Earth") == ()
        assert bf("Neptune", "Neptune") == ()

    def test_first_and_last_adjacent(self):
        """First two planets: Mercury and Venus."""
        assert bf("Mercury", "Venus") == ()

    def test_last_two_planets(self):
        """Last two planets: Uranus and Neptune."""
        assert bf("Uranus", "Neptune") == ()

    def test_entire_range_forward(self):
        """Full range from Mercury to Neptune."""
        expected = (
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
        )
        assert bf("Mercury", "Neptune") == expected

    def test_entire_range_backward(self):
        """Full range from Neptune to Mercury (reversed)."""
        expected = (
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
        )
        assert bf("Neptune", "Mercury") == expected

    def test_return_type_is_tuple(self):
        """Result must always be a tuple, even when empty."""
        assert isinstance(bf("Mercury", "Venus"), tuple)
        assert isinstance(bf("Jupiter", "Neptune"), tuple)


class TestEmptyAndNullInputs:
    """Test empty, null, or zero-size inputs."""

    def test_empty_string_for_both(self):
        """Both arguments are empty strings."""
        assert bf("", "") == ()

    def test_empty_string_for_first(self):
        """First argument is empty string."""
        assert bf("", "Earth") == ()

    def test_empty_string_for_second(self):
        """Second argument is empty string."""
        assert bf("Earth", "") == ()

    def test_none_for_both(self):
        """Both arguments are None."""
        assert bf(None, None) == ()

    def test_none_for_first(self):
        """First argument is None."""
        assert bf(None, "Earth") == ()

    def test_none_for_second(self):
        """Second argument is None."""
        assert bf("Earth", None) == ()

    def test_whitespace_only(self):
        """Arguments that are whitespace-only strings."""
        assert bf("   ", "Earth") == ()
        assert bf("Earth", "   ") == ()
        assert bf("   ", "   ") == ()


class TestInvalidInputs:
    """Test invalid planet names."""

    def test_pluto(self):
        """Non-existent planet Pluto."""
        assert bf("Pluto", "Earth") == ()
        assert bf("Earth", "Pluto") == ()
        assert bf("Pluto", "Neptune") == ()

    def test_moon(self):
        """Moon is not a planet."""
        assert bf("Moon", "Earth") == ()

    def test_star(self):
        """Star is not a planet."""
        assert bf("Sun", "Earth") == ()

    def test_case_sensitive_wrong_case(self):
        """Planet names are case-sensitive; wrong casing is invalid."""
        assert bf("jupiter", "neptune") == ()
        assert bf("JUPITER", "NEPTUNE") == ()
        assert bf("Jupiter", "neptune") == ()
        assert bf("jupiter", "Neptune") == ()

    def test_partial_name(self):
        """Partial planet names are invalid."""
        assert bf("Mer", "Earth") == ()
        assert bf("Earth", "Mar") == ()

    def test_special_characters(self):
        """Special characters as planet names."""
        assert bf("@#$", "Earth") == ()
        assert bf("Earth", "123") == ()

    def test_numeric_input(self):
        """Numeric inputs are not valid planet names."""
        assert bf(1, 2) == ()
        assert bf(0, 7) == ()

    def test_list_input(self):
        """List as input is not a valid planet name."""
        assert bf(["Earth"], "Mars") == ()

    def test_boolean_input(self):
        """Boolean inputs are not valid planet names."""
        assert bf(True, "Earth") == ()
        assert bf("Earth", False) == ()


class TestExceptionCases:
    """Test that the function handles unexpected inputs gracefully."""

    def test_unicode_input(self):
        """Unicode characters as planet names."""
        assert bf("地球", "火星") == ()
        assert bf("🪐", "🌍") == ()

    def test_very_long_string(self):
        """Very long string as planet name."""
        long_name = "A" * 10000
        assert bf(long_name, "Earth") == ()

    def test_newline_in_input(self):
        """Newline character in planet name."""
        assert bf("Ear\nth", "Mars") == ()

    def test_dict_input(self):
        """Dictionary as input is not a valid planet name."""
        assert bf({"name": "Earth"}, "Mars") == ()

    def test_function_as_input(self):
        """Function object as input is not a valid planet name."""
        assert bf(lambda: "Earth", "Mars") == ()
