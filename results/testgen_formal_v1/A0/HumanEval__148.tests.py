import pytest
from solution import bf


class TestBf:
    """Tests for the bf function."""

    def test_basic_jupiter_neptune(self):
        result = bf("Jupiter", "Neptune")
        assert result == ("Saturn", "Uranus")

    def test_earth_mercury_reversed(self):
        result = bf("Earth", "Mercury")
        assert result == ("Venus",)

    def test_mercury_uranus(self):
        result = bf("Mercury", "Uranus")
        assert result == ("Venus", "Earth", "Mars", "Jupiter", "Saturn")

    def test_adjacent_planets(self):
        result = bf("Earth", "Mars")
        assert result == ()

    def test_same_planet(self):
        result = bf("Earth", "Earth")
        assert result == ()

    def test_first_and_last(self):
        result = bf("Mercury", "Neptune")
        assert result == (
            "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus"
        )

    def test_invalid_planet1(self):
        result = bf("Pluto", "Earth")
        assert result == ()

    def test_invalid_planet2(self):
        result = bf("Earth", "Pluto")
        assert result == ()

    def test_both_invalid(self):
        result = bf("Pluto", "Mars")
        assert result == ()

    def test_one_valid_one_invalid(self):
        result = bf("Sun", "Jupiter")
        assert result == ()

    def test_reverse_order(self):
        result = bf("Neptune", "Jupiter")
        assert result == ("Saturn", "Uranus")

    def test_reverse_order_earth_mercury(self):
        result = bf("Mercury", "Earth")
        assert result == ("Venus",)

    def test_returns_tuple_type(self):
        result = bf("Jupiter", "Neptune")
        assert isinstance(result, tuple)

    def test_empty_result_is_tuple(self):
        result = bf("Earth", "Earth")
        assert isinstance(result, tuple)

    def test_no_planets_between(self):
        result = bf("Venus", "Earth")
        assert result == ()

    def test_single_planet_between(self):
        result = bf("Mercury", "Earth")
        assert result == ("Venus",)

    def test_all_planets_between(self):
        result = bf("Mercury", "Neptune")
        expected = (
            "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus"
        )
        assert result == expected

    def test_case_sensitive(self):
        result = bf("jupiter", "neptune")
        assert result == ()

    def test_planets_sorted_by_proximity_to_sun(self):
        result = bf("Mercury", "Neptune")
        planets_order = [
            "Mercury", "Venus", "Earth", "Mars",
            "Jupiter", "Saturn", "Uranus", "Neptune"
        ]
        for i in range(len(result) - 1):
            idx_a = planets_order.index(result[i])
            idx_b = planets_order.index(result[i + 1])
            assert idx_a < idx_b
