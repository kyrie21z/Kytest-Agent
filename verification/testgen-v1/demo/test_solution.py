# Accepted by submit_tests; explanations in testgen_report.json.

from solution import increment as _case0_increment

def test_valid():
    assert _case0_increment(2) == 3

from solution import increment as _case1_increment

def test_wrong():
    assert _case1_increment(3) == 4

from solution import increment as _case2_increment

def test_type():
    assert isinstance(_case2_increment(2), int)
