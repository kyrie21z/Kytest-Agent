import pytest
from solution import bf


class TestBfBasic:
    """Test basic functionality of the bf function."""

    def test_jupiter_to_neptune(self):
        """Test planets between Jupiter and Neptune."""
        result = bf("Jupiter", "Neptune")
        assert result == ("Saturn", "Uranus")

    def test_earth_to_mercury_reversed(self):
        """Test planets between Earth and Mercury (reversed order)."""
        result = bf("Earth", "Mercury")
        assert result == ("Venus",)

    def test_mercury_to_uranus(self):
        """Test planets between Mercury and Uranus."""
        result = bf("Mercury", "Uranus")
        assert result == ("Venus", "Earth", "Mars", "Jupiter", "Saturn")

    def test_adjacent_planets(self):
        """Test planets between two adjacent planets."""
        result = bf("Earth", "Mars")
        assert result == ()

    def test_same_planet(self):
        """Test when both planets are the same."""
        result = bf("Earth", "Earth")
        assert result == ()

    def test_consecutive_planets(self):
        """Test consecutive planets like Venus and Earth."""
        result = bf("Venus", "Earth")
        assert result == ()


class TestBfInvalidInput:
    """Test handling of invalid planet names."""

    def test_invalid_first_planet(self):
        """Test with an invalid first planet name."""
        result = bf("Pluto", "Earth")
        assert result == ()

    def test_invalid_second_planet(self):
        """Test with an invalid second planet name."""
        result = bf("Earth", "Pluto")
        assert result == ()

    def test_both_invalid_planets(self):
        """Test with both planet names being invalid."""
        result = bf("Pluto", "Mars")
        assert result == ()

    def test_nonexistent_planet_name(self):
        """Test with a completely nonexistent planet name."""
        result = bf("Kepler-452b", "Earth")
        assert result == ()

    def test_empty_string(self):
        """Test with empty string as planet name."""
        result = bf("", "Earth")
        assert result == ()

    def test_case_sensitive(self):
        """Test that planet names are case-sensitive."""
        result = bf("earth", "Mars")
        assert result == ()

    def test_lowercase_valid_names(self):
        """Test with lowercase valid planet names."""
        result = bf("mercury", "venus")
        assert result == ()


class TestBfEdgeCases:
    """Test edge cases for the bf function."""

    def test_sun_side_extreme(self):
        """Test from Mercury to Venus (closest to sun)."""
        result = bf("Mercury", "Venus")
        assert result == ()

    def test_far_side_extreme(self):
        """Test from Neptune to Pluto-like scenario."""
        result = bf("Neptune", "Pluto")
        assert result == ()

    def test_full_range_reverse(self):
        """Test full range from Neptune to Mercury."""
        result = bf("Neptune", "Mercury")
        expected = ("Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus")
        assert result == expected

    def test_partial_range_reverse(self):
        """Test partial range in reverse order."""
        result = bf("Neptune", "Jupiter")
        expected = ("Saturn", "Uranus")
        assert result == expected

    def test_returns_tuple_type(self):
        """Test that the return type is always a tuple."""
        result = bf("Mercury", "Neptune")
        assert isinstance(result, tuple)

    def test_single_planet_between(self):
        """Test when only one planet is between."""
        result = bf("Mercury", "Earth")
        assert result == ("Venus",)

    def test_all_planets_between(self):
        """Test when all other planets are between."""
        result = bf("Mercury", "Neptune")
        expected = ("Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus")
        assert result == expected


class TestBfOrdering:
    """Test that results are sorted by proximity to the sun."""

    def test_result_sorted_by_proximity(self):
        """Verify results are sorted from closest to farthest from sun."""
        result = bf("Jupiter", "Neptune")
        planets_order = ["Mercury", "Venus", "Earth", "Mars",
                         "Jupiter", "Saturn", "Uranus", "Neptune"]
        indices = [planets_order.index(p) for p in result]
        assert indices == sorted(indices)

    def test_large_range_sorted(self):
        """Verify large range results are properly sorted."""
        result = bf("Mercury", "Neptune")
        planets_order = ["Mercury", "Venus", "Earth", "Mars",
                         "Jupiter", "Saturn", "Uranus", "Neptune"]
        indices = [planets_order.index(p) for p in result]
        assert indices == sorted(indices)
