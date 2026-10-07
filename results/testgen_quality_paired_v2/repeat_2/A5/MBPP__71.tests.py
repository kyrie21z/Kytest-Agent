# Accepted by submit_tests; explanations in testgen_report.json.

from solution import comb_sort as _case0_comb_sort

def test_basic_unsorted():
    """Sort a basic unsorted list of integers.

    Contract quote: "Write a function to sort a list of elements."
    Input domain: nums = [3, 1, 4, 1, 5, 9, 2, 6] — a small unsorted list of positive integers.
    Expected result: The returned list must be in non-decreasing order: [1, 1, 2, 3, 4, 5, 6, 9].
    Fault hypothesis: If the function fails to fully sort (e.g., stops early or has a gap bug),
        the output will not be sorted. Asserting nums == sorted(nums) catches partial sorts.
    """
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    result = _case0_comb_sort(nums)
    assert result == [1, 1, 2, 3, 4, 5, 6, 9], f'Expected sorted list, got {result}'
    assert isinstance(result, list), 'Result must be a list'

from solution import comb_sort as _case1_comb_sort

def test_already_sorted():
    """Sort an already sorted list.

    Contract quote: "Write a function to sort a list of elements."
    Input domain: nums = [1, 2, 3, 4, 5] — already in non-decreasing order.
    Expected result: The list remains [1, 2, 3, 4, 5].
    Fault hypothesis: If the function corrupts data or shifts elements incorrectly,
        the output would differ from the input even when already sorted.
    """
    nums = [1, 2, 3, 4, 5]
    result = _case1_comb_sort(nums)
    assert result == [1, 2, 3, 4, 5], f'Already sorted list was corrupted: {result}'

from solution import comb_sort as _case2_comb_sort

def test_reverse_sorted():
    """Sort a reverse-sorted list (worst-case-ish for many algorithms).

    Contract quote: "Write a function to sort a list of elements."
    Input domain: nums = [5, 4, 3, 2, 1] — strictly decreasing sequence.
    Expected result: The list becomes [1, 2, 3, 4, 5].
    Fault hypothesis: Comb sort needs multiple passes with shrinking gaps; if the loop
        terminates too early (gaps > 1 condition wrong), large inversions won't be resolved.
    """
    nums = [5, 4, 3, 2, 1]
    result = _case2_comb_sort(nums)
    assert result == [1, 2, 3, 4, 5], f'Reverse sorted list not fully sorted: {result}'

from solution import comb_sort as _case3_comb_sort

def test_empty_list():
    """Sort an empty list.

    Contract quote: "Write a function to sort a list of elements."
    Input domain: nums = [] — empty list.
    Expected result: Returns [].
    Fault hypothesis: If len([]) causes issues or the while loop accesses invalid indices,
        this could raise an exception or return unexpected output.
    """
    nums = []
    result = _case3_comb_sort(nums)
    assert result == [], f'Empty list should return [], got {result}'
    assert isinstance(result, list), 'Result must be a list'

from solution import comb_sort as _case4_comb_sort

def test_single_element():
    """Sort a single-element list.

    Contract quote: "Write a function to sort a list of elements."
    Input domain: nums = [42] — one element.
    Expected result: Returns [42].
    Fault hypothesis: With len=1, gaps starts at 1, then becomes int(1/1.3)=0;
        the inner loop condition gaps+i < 1 means i < 1, so i=0 checks nums[0] vs nums[0+0],
        which is a self-swap. If buggy, could cause infinite loop or index error.
    """
    nums = [42]
    result = _case4_comb_sort(nums)
    assert result == [42], f'Single element list changed: {result}'
    assert isinstance(result, list), 'Result must be a list'

from solution import comb_sort as _case5_comb_sort

def test_negative_numbers():
    """Sort a list containing negative and positive numbers.

    Contract quote: "Write a function to sort a list of elements."
    Input domain: nums = [-3, -1, 4, -7, 2, 0] — mix of negatives and positives.
    Expected result: [-7, -3, -1, 0, 2, 4].
    Fault hypothesis: Some sorting implementations mishandle negative comparisons;
        verifying full ordering catches comparison bugs.
    """
    nums = [-3, -1, 4, -7, 2, 0]
    result = _case5_comb_sort(nums)
    assert result == [-7, -3, -1, 0, 2, 4], f'Mixed sign list not sorted: {result}'
    assert isinstance(result, list), 'Result must be a list'

from solution import comb_sort as _case6_comb_sort

def test_two_elements_reverse():
    """Sort two elements in reverse order.

    Contract quote: "Write a function to sort a list of elements."
    Input domain: nums = [2, 1] — minimal unsorted list.
    Expected result: [1, 2].
    Fault hypothesis: Mutant M1 (i=0→1) sets i=1 at start of inner loop.
        With gaps=1 (first pass), condition gaps+i < len(nums) = 1+1 < 2 = False,
        so the inner loop body never executes. The inversion is never resolved.
        This test directly targets that survivor.
    """
    nums = [2, 1]
    result = _case6_comb_sort(nums)
    assert result == [1, 2], f'Two-element reverse not sorted: {result}'
    assert isinstance(result, list), 'Result must be a list'

from solution import comb_sort as _case7_comb_sort

def test_three_elements_minimal_unsorted():
    """Sort three elements where smallest is at end.

    Contract quote: "Write a function to sort a list of elements."
    Input domain: nums = [3, 2, 1] — smallest element at the end.
    Expected result: [1, 2, 3].
    Fault hypothesis: With M1 (i=1), the first pass (gaps=2→int(2/1.3)=1)
        checks indices starting at i=1: compares nums[1] vs nums[2] (2 vs 1, swaps).
        But index 0 is never involved in comparisons during this pass.
        Subsequent passes with smaller gaps may not reach index 0 either.
        This catches partial sorting where index 0 is neglected.
    """
    nums = [3, 2, 1]
    result = _case7_comb_sort(nums)
    assert result == [1, 2, 3], f'Three-element list not fully sorted: {result}'
    assert isinstance(result, list), 'Result must be a list'
