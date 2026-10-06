import pytest
from solution import below_zero


class TestBelowZero:
    """Tests for the below_zero function."""

    def test_no_negative_balance(self):
        """Balance never falls below zero with all positive operations."""
        assert below_zero([1, 2, 3]) is False

    def test_balance_drops_below_zero(self):
        """Balance falls below zero after a withdrawal."""
        assert below_zero([1, 2, -4, 5]) is True

    def test_empty_operations(self):
        """Empty operations list should return False (balance stays at zero)."""
        assert below_zero([]) is False

    def test_single_positive_operation(self):
        """Single deposit keeps balance above zero."""
        assert below_zero([5]) is False

    def test_single_negative_operation(self):
        """Single withdrawal makes balance fall below zero."""
        assert below_zero([-1]) is True

    def test_single_zero_operation(self):
        """Single zero operation keeps balance at zero (not below)."""
        assert below_zero([0]) is False

    def test_balance_exactly_zero(self):
        """Balance hits exactly zero but never goes below."""
        assert below_zero([1, -1]) is False

    def test_balance_hovers_around_zero(self):
        """Balance fluctuates but dips below zero in the middle."""
        assert below_zero([3, -2, -2, 1]) is True

    def test_all_zeros(self):
        """All zero operations keep balance at zero."""
        assert below_zero([0, 0, 0]) is False

    def test_large_positive_then_negative(self):
        """Large deposit followed by larger withdrawal."""
        assert below_zero([100, -200]) is True

    def test_negative_then_positive(self):
        """Withdrawal first causes immediate below-zero."""
        assert below_zero([-5, 10]) is True

    def test_multiple_below_zero_points(self):
        """Balance goes below zero multiple times."""
        assert below_zero([1, -2, 3, -5]) is True

    def test_withdrawal_at_start(self):
        """First operation is a withdrawal."""
        assert below_zero([-10, 5, 5]) is True

    def test_recovery_after_below_zero(self):
        """Balance recovers after going below zero."""
        assert below_zero([1, -3, 5]) is True

    def test_exact_zero_boundary(self):
        """Operations that bring balance to exactly zero."""
        assert below_zero([5, -5, 3]) is False

    def test_all_negative_operations(self):
        """All operations are withdrawals."""
        assert below_zero([-1, -2, -3]) is True

    def test_mixed_operations_no_below_zero(self):
        """Mixed operations but balance never drops below zero."""
        assert below_zero([10, -3, -4, -2]) is False

    def test_large_values(self):
        """Test with large integer values."""
        assert below_zero([1000000, -2000000]) is True
        assert below_zero([1000000, -500000]) is False

    def test_docstring_example_1(self):
        """Verify docstring example: [1, 2, 3] -> False."""
        assert below_zero([1, 2, 3]) is False

    def test_docstring_example_2(self):
        """Verify docstring example: [1, 2, -4, 5] -> True."""
        assert below_zero([1, 2, -4, 5]) is True
