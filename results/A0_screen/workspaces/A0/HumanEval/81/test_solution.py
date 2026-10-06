import pytest
from solution import numerical_letter_grade


class TestNumericalLetterGrade:
    """Tests for the numerical_letter_grade function."""

    # --- Boundary value tests (exact thresholds) ---
    # Note: The function uses strict `>` comparisons, so exact threshold values
    # fall into the next lower grade bucket.

    def test_perfect_gpa_4_0(self):
        """GPA of exactly 4.0 should return 'A+'."""
        assert numerical_letter_grade([4.0]) == ["A+"]

    def test_gpa_3_7(self):
        """GPA of exactly 3.7 is not > 3.7, so falls to next bucket: 'A-'."""
        assert numerical_letter_grade([3.7]) == ["A-"]

    def test_gpa_3_3(self):
        """GPA of exactly 3.3 is not > 3.3, so falls to next bucket: 'B+'."""
        assert numerical_letter_grade([3.3]) == ["B+"]

    def test_gpa_3_0(self):
        """GPA of exactly 3.0 is not > 3.0, so falls to next bucket: 'B'."""
        assert numerical_letter_grade([3.0]) == ["B"]

    def test_gpa_2_7(self):
        """GPA of exactly 2.7 is not > 2.7, so falls to next bucket: 'B-'."""
        assert numerical_letter_grade([2.7]) == ["B-"]

    def test_gpa_2_3(self):
        """GPA of exactly 2.3 is not > 2.3, so falls to next bucket: 'C+'."""
        assert numerical_letter_grade([2.3]) == ["C+"]

    def test_gpa_2_0(self):
        """GPA of exactly 2.0 is not > 2.0, so falls to next bucket: 'C'."""
        assert numerical_letter_grade([2.0]) == ["C"]

    def test_gpa_1_7(self):
        """GPA of exactly 1.7 is not > 1.7, so falls to next bucket: 'C-'."""
        assert numerical_letter_grade([1.7]) == ["C-"]

    def test_gpa_1_3(self):
        """GPA of exactly 1.3 is not > 1.3, so falls to next bucket: 'D+'."""
        assert numerical_letter_grade([1.3]) == ["D+"]

    def test_gpa_1_0(self):
        """GPA of exactly 1.0 is not > 1.0, so falls to next bucket: 'D'."""
        assert numerical_letter_grade([1.0]) == ["D"]

    def test_gpa_0_7(self):
        """GPA of exactly 0.7 is not > 0.7, so falls to next bucket: 'D-'."""
        assert numerical_letter_grade([0.7]) == ["D-"]

    def test_gpa_0_0(self):
        """GPA of exactly 0.0 should return 'E'."""
        assert numerical_letter_grade([0.0]) == ["E"]

    # --- Just above each threshold ---

    def test_just_above_3_7(self):
        """GPA just above 3.7 should return 'A'."""
        assert numerical_letter_grade([3.8]) == ["A"]

    def test_just_above_3_3(self):
        """GPA just above 3.3 should return 'A-'."""
        assert numerical_letter_grade([3.4]) == ["A-"]

    def test_just_above_3_0(self):
        """GPA just above 3.0 should return 'B+'."""
        assert numerical_letter_grade([3.1]) == ["B+"]

    def test_just_above_2_7(self):
        """GPA just above 2.7 should return 'B'."""
        assert numerical_letter_grade([2.8]) == ["B"]

    def test_just_above_2_3(self):
        """GPA just above 2.3 should return 'B-'."""
        assert numerical_letter_grade([2.4]) == ["B-"]

    def test_just_above_2_0(self):
        """GPA just above 2.0 should return 'C+'."""
        assert numerical_letter_grade([2.1]) == ["C+"]

    def test_just_above_1_7(self):
        """GPA just above 1.7 should return 'C'."""
        assert numerical_letter_grade([1.8]) == ["C"]

    def test_just_above_1_3(self):
        """GPA just above 1.3 should return 'C-'."""
        assert numerical_letter_grade([1.4]) == ["C-"]

    def test_just_above_1_0(self):
        """GPA just above 1.0 should return 'D+'."""
        assert numerical_letter_grade([1.1]) == ["D+"]

    def test_just_above_0_7(self):
        """GPA just above 0.7 should return 'D'."""
        assert numerical_letter_grade([0.8]) == ["D"]

    def test_just_above_0_0(self):
        """GPA just above 0.0 should return 'D-'."""
        assert numerical_letter_grade([0.1]) == ["D-"]

    # --- Mid-range values ---

    def test_mid_range_a(self):
        """GPA in the middle of the A range."""
        assert numerical_letter_grade([3.9]) == ["A"]

    def test_mid_range_b_plus(self):
        """GPA in the middle of the B+ range."""
        assert numerical_letter_grade([3.2]) == ["B+"]

    def test_mid_range_c(self):
        """GPA in the middle of the C range."""
        assert numerical_letter_grade([1.9]) == ["C"]

    def test_mid_range_d(self):
        """GPA in the middle of the D range."""
        assert numerical_letter_grade([0.9]) == ["D"]

    # --- Example from docstring ---

    def test_docstring_example(self):
        """Test the example provided in the docstring."""
        result = numerical_letter_grade([4.0, 3, 1.7, 2, 3.5])
        expected = ['A+', 'B', 'C-', 'C', 'A-']
        assert result == expected

    # --- Empty input ---

    def test_empty_list(self):
        """An empty list should return an empty list."""
        assert numerical_letter_grade([]) == []

    # --- Multiple grades ---

    def test_multiple_grades_all_same(self):
        """Multiple identical GPAs should produce identical letter grades."""
        assert numerical_letter_grade([3.0, 3.0, 3.0]) == ["B", "B", "B"]

    def test_multiple_grades_mixed(self):
        """Mixed GPAs should produce correct corresponding letter grades."""
        result = numerical_letter_grade([4.0, 3.8, 3.4, 3.1, 2.8, 2.4, 2.1, 1.8, 1.4, 1.1, 0.8, 0.1, 0.0])
        expected = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"]
        assert result == expected

    # --- Integer inputs ---

    def test_integer_inputs(self):
        """Integer GPA values should work correctly."""
        # 4 -> A+, 3 -> B (not > 3.0, but > 2.7), 2 -> C (not > 2.0, but > 1.7)
        # 1 -> D (not > 1.0, but > 0.7), 0 -> E
        assert numerical_letter_grade([4, 3, 2, 1, 0]) == ["A+", "B", "C", "D", "E"]

    # --- Negative or invalid-like values ---

    def test_negative_gpa(self):
        """Negative GPA should return 'E' (falls through to else)."""
        assert numerical_letter_grade([-1.0]) == ["E"]

    def test_zero_gpa(self):
        """Zero GPA should return 'E'."""
        assert numerical_letter_grade([0]) == ["E"]

    # --- Return type check ---

    def test_returns_list_of_strings(self):
        """The function should always return a list of strings."""
        result = numerical_letter_grade([4.0, 0.0])
        assert isinstance(result, list)
        assert all(isinstance(grade, str) for grade in result)

    # --- All possible letter grades are covered ---

    def test_all_letter_grades_present(self):
        """Verify every possible letter grade can be produced."""
        gpas = [4.0, 3.8, 3.4, 3.1, 2.8, 2.4, 2.1, 1.8, 1.4, 1.1, 0.8, 0.1, 0.0]
        expected_grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"]
        result = numerical_letter_grade(gpas)
        assert result == expected_grades
        # Also verify all unique grades are present
        assert set(result) == set(expected_grades)
