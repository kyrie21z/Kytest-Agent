import pytest
from solution import bf


class TestBfNormalCases:
    """Test normal cases with typical inputs."""

    def test_jupiter_to_neptune(self):
        """Planets between Jupiter and Neptune (in order)."""
        assert bf("Jupiter", "Neptune") == ("Saturn", "Uranus")

    def test_earth_to_mercury_reversed(self):
        """Planet1 is farther from Sun than planet2; should swap internally."""
        assert bf("Earth", "Mercury") == ("Venus",)

    def test_mercury_to_uranus(self):
        """Wide range from Mercury to Uranus."""
        assert bf("Mercury", "Uranus") == ("Venus", "Earth", "Mars", "Jupiter", "Saturn")

    def test_neptune_to_mercury_reverse_order(self):
        """Reverse order spanning almost all planets."""
        assert bf("Neptune", "Mercury") == (
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
        )

    def test_venus_to_earth(self):
        """Two adjacent planets with one planet between them."""
        assert bf("Venus", "Earth") == ()

    def test_mars_to_jupiter_adjacent(self):
        """Adjacent planets: Mars and Jupiter have nothing between them."""
        assert bf("Mars", "Jupiter") == ()

    def test_same_planet(self):
        """Both arguments are the same planet; nothing lies between."""
        assert bf("Earth", "Earth") == ()

    def test_saturn_to_uranus_adjacent(self):
        """Adjacent planets: Saturn and Uranus."""
        assert bf("Saturn", "Uranus") == ()


class TestBfBoundaryCases:
    """Test boundary cases at edges of valid input ranges."""

    def test_first_to_last(self):
        """From closest to farthest planet."""
        assert bf("Mercury", "Neptune") == (
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
        )

    def test_last_to_first(self):
        """From farthest to closest planet (reverse order)."""
        assert bf("Neptune", "Mercury") == (
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
        )

    def test_first_to_second(self):
        """First and second planet (adjacent)."""
        assert bf("Mercury", "Venus") == ()

    def test_seventh_to_eighth(self):
        """Seventh and eighth planet (adjacent)."""
        assert bf("Uranus", "Neptune") == ()

    def test_second_to_first(self):
        """Second to first planet (reversed adjacent)."""
        assert bf("Venus", "Mercury") == ()

    def test_third_to_fifth(self):
        """Middle range: Earth to Jupiter."""
        assert bf("Earth", "Jupiter") == ("Mars",)

    def test_fourth_to_sixth(self):
        """Middle range: Mars to Saturn."""
        assert bf("Mars", "Saturn") == ("Jupiter",)


class TestBfEmptyAndZeroSizeInputs:
    """Test empty, null, or zero-size inputs."""

    def test_both_empty_strings(self):
        """Both arguments are empty strings."""
        assert bf("", "") == ()

    def test_first_empty_string(self):
        """First argument is empty string."""
        assert bf("", "Earth") == ()

    def test_second_empty_string(self):
        """Second argument is empty string."""
        assert bf("Mercury", "") == ()

    def test_none_first(self):
        """First argument is None."""
        assert bf(None, "Earth") == ()

    def test_none_second(self):
        """Second argument is None."""
        assert bf("Mercury", None) == ()

    def test_both_none(self):
        """Both arguments are None."""
        assert bf(None, None) == ()


class TestBfInvalidInputs:
    """Test invalid inputs (non-existent planet names)."""

    def test_pluto_and_earth(self):
        """Non-existent planet 'Pluto' paired with a valid one."""
        assert bf("Pluto", "Earth") == ()

    def test_moon_and_sun(self):
        """Both arguments are non-existent planet names."""
        assert bf("Moon", "Sun") == ()

    def test_lowercase_valid_name(self):
        """Lowercase version of a valid planet name."""
        assert bf("mercury", "earth") == ()

    def test_uppercase_valid_name(self):
        """All-uppercase version of a valid planet name."""
        assert bf("MERCURY", "EARTH") == ()

    def test_mixed_case(self):
        """Mixed-case planet name."""
        assert bf("MeRcUrY", "Earth") == ()

    def test_trailing_space(self):
        """Valid name with trailing whitespace."""
        assert bf("Mercury ", "Earth") == ()

    def test_leading_space(self):
        """Valid name with leading whitespace."""
        assert bf(" Mercury", "Earth") == ()

    def test_integer_input(self):
        """Integer values instead of strings."""
        assert bf(1, 2) == ()

    def test_list_input(self):
        """List passed instead of a string."""
        assert bf(["Mercury"], "Earth") == ()

    def test_whitespace_only(self):
        """Whitespace-only string."""
        assert bf("   ", "Earth") == ()

    def test_special_characters(self):
        """Special characters as planet names."""
        assert bf("@#$%", "Earth") == ()


class TestBfReturnType:
    """Test that the return type is always a tuple."""

    def test_returns_tuple_normal(self):
        """Return type for a normal call."""
        result = bf("Mercury", "Uranus")
        assert isinstance(result, tuple)

    def test_returns_tuple_empty(self):
        """Return type when result is empty."""
        result = bf("Earth", "Earth")
        assert isinstance(result, tuple)

    def test_returns_tuple_invalid(self):
        """Return type for invalid inputs."""
        result = bf("Pluto", "Mars")
        assert isinstance(result, tuple)

    def test_single_element_is_tuple(self):
        """Single-element result is still a tuple."""
        result = bf("Earth", "Mercury")
        assert isinstance(result, tuple)
        assert len(result) == 1

    def test_sorted_by_proximity_to_sun(self):
        """Result is sorted by proximity to the Sun regardless of input order."""
        # Forward order: Jupiter -> Neptune => Saturn, Uranus
        forward = bf("Jupiter", "Neptune")
        # Reverse order: Neptune -> Jupiter => Saturn, Uranus
        reverse = bf("Neptune", "Jupiter")
        assert forward == reverse == ("Saturn", "Uranus")
