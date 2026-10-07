"""A selected public benchmark example; fresh model runs can have different outcomes."""
from ..faults import generate_mutants

ROTATION_SOURCE = "def find_Element(arr,ranges,rotations,index) :  \n    'Write a python function to find element at a given index after number of rotations.'\n    for i in range(rotations - 1,-1,-1 ) : \n        left = ranges[i][0] \n        right = ranges[i][1] \n        if (left <= index and right >= index) : \n            if (index == left) : \n                index = right \n            else : \n                index = index - 1 \n    return arr[index]\n"
ROTATION_TASK = "Generate unit tests for solution.py in the current directory.\nWrite them to test_solution.py using pytest.\n"

# The same complete ROR/LCR/BCR pool as the frozen MBPP/304 experiment.
# Inputs independently witness an error in every fault; none is selected by a generated suite.
_witnesses = (
    ("区间判断 and 错写为 or", ([0,1,2,3,4], [[1,3]], 1, 0), 0),
    ("下边界被排除", ([0,1,2,3,4], [[1,3]], 1, 1), 3),
    ("上边界被排除", ([0,1,2,3,4], [[1,3]], 1, 3), 2),
    ("左端点回绕判断取反", ([0,1,2,3,4], [[1,3]], 1, 1), 3),
)
_mutants=generate_mutants(ROTATION_SOURCE,operators=["ROR","LCR","BCR"])
assert len(_mutants)==len(_witnesses)==4
ROTATION_FAULTS = tuple((mutant.mutant_id,label,mutant.source,witness,expected)
    for mutant,(label,witness,expected) in zip(
        _mutants,_witnesses))
assert len(ROTATION_FAULTS)==4
