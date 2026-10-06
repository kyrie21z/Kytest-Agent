# Accepted by submit_tests; explanations in testgen_report.json.

from solution import classify as _case0_classify

def test_inside():
    assert _case0_classify(5, 2, 8) == 0

from solution import classify as _case1_classify

def test_below():
    assert _case1_classify(1, 2, 8) == -1

from solution import classify as _case2_classify

def test_above():
    assert _case2_classify(9, 2, 8) == 1

from solution import classify as _case3_classify

def test_low_inclusive():
    assert _case3_classify(2, 2, 8) == 0

from solution import classify as _case4_classify

def test_high_inclusive():
    assert _case4_classify(8, 2, 8) == 0
