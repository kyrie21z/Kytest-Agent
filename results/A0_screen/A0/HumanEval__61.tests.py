from solution import correct_bracketing


class TestCorrectBracketing:

    def test_empty_string(self):
        assert correct_bracketing("") is True

    def test_single_opening(self):
        assert correct_bracketing("(") is False

    def test_single_closing(self):
        assert correct_bracketing(")") is False

    def test_simple_pair(self):
        assert correct_bracketing("()") is True

    def test_nested(self):
        assert correct_bracketing("(())") is True

    def test_multiple_pairs(self):
        assert correct_bracketing("()()") is True

    def test_complex_balanced(self):
        assert correct_bracketing("(()())") is True

    def test_wrong_order(self):
        assert correct_bracketing(")(") is False

    def test_wrong_order_with_content(self):
        assert correct_bracketing(")(()") is False

    def test_unmatched_opening_at_end(self):
        assert correct_bracketing("(()") is False

    def test_unmatched_closing_at_start(self):
        assert correct_bracketing("())") is False

    def test_deeply_nested(self):
        assert correct_bracketing("(((())))") is True

    def test_alternating_nested(self):
        assert correct_bracketing("()(())") is True

    def test_many_openings_no_closings(self):
        assert correct_bracketing("(((((") is False

    def test_many_closings_no_openings(self):
        assert correct_bracketing("))))") is False

    def test_mixed_valid_and_invalid(self):
        assert correct_bracketing("(()))(") is False
