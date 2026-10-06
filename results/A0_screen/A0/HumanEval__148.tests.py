import pytest
from solution import bf


class TestBfFunction:
    """Tests for the bf() function that returns planets between two given planets."""

    # --- Valid planet pairs ---

    def test_jupiter_to_neptune(self):
        """Planets between Jupiter and Neptune: Saturn, Uranus."""
        assert bf("Jupiter", "Neptune") == ("Saturn", "Uranus")

    def test_earth_to_mercury(self):
        """Reversed order: planets between Mercury and Earth: Venus."""
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

    def test_adjacent_planets(self):
        """Adjacent planets should return an empty tuple."""
        assert bf("Mercury", "Venus") == ()
        assert bf("Earth", "Mars") == ()
        assert bf("Neptune", "Uranus") == ()

    def test_same_planet(self):
        """Same planet on both sides should return an empty tuple."""
        assert bf("Earth", "Earth") == ()
        assert bf("Jupiter", "Jupiter") == ()

    def test_first_to_last(self):
        """All planets between Mercury and Neptune."""
        assert bf("Mercury", "Neptune") == (
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
        )

    def test_reverse_order_first_to_last(self):
        """Reverse order: all planets between Neptune and Mercury."""
        assert bf("Neptune", "Mercury") == (
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
        )

    def test_middle_planets_forward(self):
        """Planets between Mars and Saturn."""
        assert bf("Mars", "Saturn") == ("Jupiter",)

    def test_middle_planets_reverse(self):
        """Reverse order: planets between Saturn and Mars."""
        assert bf("Saturn", "Mars") == ("Jupiter",)

    def test_venus_to_mars(self):
        """Single planet between Venus and Mars: Earth."""
        assert bf("Venus", "Mars") == ("Earth",)

    def test_venus_to_mars_reversed(self):
        """Reverse order: single planet between Mars and Venus: Earth."""
        assert bf("Mars", "Venus") == ("Earth",)

    # --- Invalid planet names ---

    def test_invalid_planet1(self):
        """First argument is not a valid planet name."""
        assert bf("Pluto", "Earth") == ()

    def test_invalid_planet2(self):
        """Second argument is not a valid planet name."""
        assert bf("Earth", "Pluto") == ()

    def test_both_invalid(self):
        """Both arguments are not valid planet names."""
        assert bf("Pluto", "Kepler-442b") == ()

    def test_nonexistent_planet(self):
        """A fictional planet name."""
        assert bf("Mars", "Krypton") == ()

    def test_lowercase_invalid(self):
        """Lowercase planet names are not recognized (case-sensitive)."""
        assert bf("mercury", "venus") == ()
        assert bf("Earth", "mars") == ()

    def test_mixed_case_invalid(self):
        """Mixed case planet names are not recognized."""
        assert bf("EARTH", "MERCURY") == ()
        assert bf("jupiter", "NEPTUNE") == ()

    def test_empty_string(self):
        """Empty string as planet name."""
        assert bf("", "Earth") == ()
        assert bf("Mars", "") == ()

    def test_numeric_input(self):
        """Numeric values passed as strings."""
        assert bf("1", "2") == ()
        assert bf("0", "8") == ()

    # --- Return type checks ---

    def test_returns_tuple(self):
        """Ensure the return value is always a tuple."""
        result = bf("Mercury", "Neptune")
        assert isinstance(result, tuple)

    def test_returns_tuple_for_empty(self):
        """Empty result should also be a tuple."""
        result = bf("Pluto", "Earth")
        assert isinstance(result, tuple)
        assert len(result) == 0

    def test_returns_tuple_for_single(self):
        """Single-element result should still be a tuple."""
        result = bf("Venus", "Mars")
        assert isinstance(result, tuple)
        assert len(result) == 1
