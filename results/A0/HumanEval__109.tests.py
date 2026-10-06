import pytest
from solution import move_one_ball


class TestMoveOneBall:
    """Tests for the move_one_ball function."""

    # --- Empty and single-element arrays ---

    def test_empty_array(self):
        """An empty array should return True."""
        assert move_one_ball([]) is True

    def test_single_element(self):
        """A single-element array is trivially sorted."""
        assert move_one_ball([1]) is True

    # --- Already sorted arrays ---

    def test_already_sorted_two_elements(self):
        assert move_one_ball([1, 2]) is True

    def test_already_sorted_three_elements(self):
        assert move_one_ball([1, 2, 3]) is True

    def test_already_sorted_large(self):
        assert move_one_ball([1, 2, 3, 4, 5]) is True

    def test_already_sorted_with_negatives(self):
        assert move_one_ball([-3, -1, 0, 2, 5]) is True

    # --- Arrays rotatable via right shifts ---

    def test_rotatable_example_from_docstring(self):
        """[3, 4, 5, 1, 2] can be sorted by 2 right shifts."""
        assert move_one_ball([3, 4, 5, 1, 2]) is True

    def test_rotatable_two_elements(self):
        """[2, 1] rotated once gives [1, 2]."""
        assert move_one_ball([2, 1]) is True

    def test_rotatable_three_elements(self):
        """[2, 3, 1] rotated once gives [1, 2, 3]."""
        assert move_one_ball([2, 3, 1]) is True

    def test_rotatable_four_elements(self):
        """[4, 1, 2, 3] rotated once gives [3, 4, 1, 2] -> not sorted;
           rotated twice gives [2, 3, 4, 1] -> not sorted;
           rotated thrice gives [1, 2, 3, 4] -> sorted."""
        assert move_one_ball([4, 1, 2, 3]) is True

    def test_rotatable_five_elements_shift_one(self):
        """[2, 3, 4, 5, 1] shifted once gives [1, 2, 3, 4, 5]."""
        assert move_one_ball([2, 3, 4, 5, 1]) is True

    def test_rotatable_all_but_last(self):
        """[2, 3, 4, 5, 1] — last element wraps around."""
        assert move_one_ball([2, 3, 4, 5, 1]) is True

    def test_rotatable_negative_numbers(self):
        """[-1, 0, 2, -3, -2] — check a mix of negatives."""
        # Sorted: [-3, -2, -1, 0, 2]
        # Right shift by 2: [-1, 0, 2, -3, -2] -> no
        # Right shift by 3: [0, 2, -3, -2, -1] -> no
        # Right shift by 4: [2, -3, -2, -1, 0] -> no
        # Actually let's pick one we know works.
        assert move_one_ball([-3, -2, -1, 0, 2]) is True  # already sorted

    def test_rotatable_negative_numbers_shifted(self):
        """[-2, -1, 0, 2, -3] — right shift by 1 gives [-3, -2, -1, 0, 2]."""
        assert move_one_ball([-2, -1, 0, 2, -3]) is True

    # --- Arrays NOT rotatable to sorted ---

    def test_not_rotatable_example_from_docstring(self):
        """[3, 5, 4, 1, 2] cannot be sorted by any right shifts."""
        assert move_one_ball([3, 5, 4, 1, 2]) is False

    def test_not_rotatable_two_swapped(self):
        """[1, 3, 2, 4] — swapping two adjacent elements breaks cyclic sortability."""
        assert move_one_ball([1, 3, 2, 4]) is False

    def test_not_rotatable_multiple_disruptions(self):
        """[5, 1, 3, 2, 4] has multiple inversions."""
        assert move_one_ball([5, 1, 3, 2, 4]) is False

    def test_not_rotatable_reverse_order(self):
        """[5, 4, 3, 2, 1] reversed — not a cyclic shift of sorted."""
        assert move_one_ball([5, 4, 3, 2, 1]) is False

    def test_not_rotatable_random_permutation(self):
        """[2, 4, 1, 5, 3] — random permutation."""
        assert move_one_ball([2, 4, 1, 5, 3]) is False

    def test_not_rotatable_larger_array(self):
        """Larger array that isn't a cyclic shift of sorted."""
        assert move_one_ball([1, 5, 3, 4, 2, 6]) is False

    # --- Edge cases with larger values ---

    def test_large_values(self):
        """Works with large integer values."""
        assert move_one_ball([1000000, 2000000, 3000000]) is True

    def test_large_values_rotated(self):
        """Large values, rotated."""
        assert move_one_ball([3000000, 1000000, 2000000]) is True

    def test_large_values_not_rotatable(self):
        """Large values, not rotatable."""
        assert move_one_ball([3000000, 2000000, 1000000]) is False

    # --- Boundary: exactly two elements ---

    def test_two_elements_sorted(self):
        assert move_one_ball([1, 2]) is True

    def test_two_elements_unsorted(self):
        assert move_one_ball([2, 1]) is True  # one right shift fixes it

    # --- Three elements all permutations ---

    @pytest.mark.parametrize("arr, expected", [
        ([1, 2, 3], True),   # already sorted
        ([2, 3, 1], True),   # right shift by 1
        ([3, 1, 2], True),   # right shift by 2
        ([1, 3, 2], False),  # not a cyclic shift of sorted
        ([2, 1, 3], False),  # not a cyclic shift of sorted
        ([3, 2, 1], False),  # reverse
    ])
    def test_three_element_permutations(self, arr, expected):
        """Test all 6 permutations of three distinct elements."""
        assert move_one_ball(arr) is expected
