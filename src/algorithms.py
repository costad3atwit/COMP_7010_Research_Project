import random
import math
from collections import Counter
import pytest
from inputs import generateDuplicates, generateBackwards, generateRandom, generateKiller


# pivot functions
# BUG: returns 0 instead of l. On any subarray (l > 0) partition 
# swaps a[0] (see line 37) wjich is an element OUTSIDE the range being sorted
def firstPivot(arr, l, h):
    return 0

# BUG: same as above but for hi instead of low
def lastPivot(arr, l, h):
    return len(arr) -1

def randomPivot(arr, low, high):
    return random.randint(low, high)

def midpointPivot(arr, low, high):
    return min(max(low, int((low+high)/2)), high)

def medianPivot(arr, low, high):
    mid = (low + high) // 2
    
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]

    return mid

def partition(a, low, high, pivotFunc):
    pivot = pivotFunc(a, low, high)
    # TODO: remove the below debug line so timings aren't skewed.
    print("bad") if medianPivot(a,low,high) != midpointPivot(a,low,high) else None
    a[pivot], a[high] = a[high], a[pivot]
    pivot, wall = a[high], low
    comparisons = 0
    swaps = 0
    for j in range(low, high):
        comparisons += 1
        if a[j] <= pivot:
            swaps += 1
            a[wall], a[j] = a[j], a[wall]
            wall += 1
    a[wall], a[high] = a[high], a[wall]
    swaps += 2 # for the initial swap and the swap back
    return wall, comparisons, swaps

def quicksort(arr, start, stop, pivotFunc=firstPivot):
    if start >= stop:
        return 0, 0 

    p, partition_comparisons, partition_swaps = partition(arr, start, stop, pivotFunc)

    left_comps, left_swaps = quicksort(arr, start, p - 1, pivotFunc)
    right_comps, right_swaps = quicksort(arr, p + 1, stop, pivotFunc)

    total_comparisons = partition_comparisons + left_comps + right_comps
    total_swaps = partition_swaps + left_swaps + right_swaps

    return total_comparisons, total_swaps

# Note: mergesort never exchanges elements, so its "swaps" count is the number
# of array writes made while merging. Quicksort/heapsort "swaps" are exchanges.
def mergesort(arr, start, stop):
    if start >= stop:
        return 0, 0

    mid = (start + stop) // 2
    left_comps, left_swaps = mergesort(arr, start, mid)
    right_comps, right_swaps = mergesort(arr, mid + 1, stop)

    comparisons, swaps = merge(arr, start, mid, stop)

    total_comparisons = left_comps + right_comps + comparisons
    total_swaps = left_swaps + right_swaps + swaps

    return total_comparisons, total_swaps

def merge(arr, start, mid, stop):
    left = arr[start:mid + 1]
    right = arr[mid + 1:stop + 1]

    i = j = 0
    k = start
    comparisons = 0
    swaps = 0

    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        swaps += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
        swaps += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
        swaps += 1

    return comparisons, swaps

def heapify(arr, size, i):
    largest = i
    leftChild = 2*i + 1
    rightChild = 2*i + 2

    comps = 0
    swaps = 0

    if leftChild < size:
        comps += 1
        if arr[leftChild] > arr[largest]:
            largest = leftChild
    if rightChild < size:
        comps += 1
        if arr[rightChild] > arr[largest]:
            largest = rightChild

    c = 0
    s = 0
    if largest != i:
        swaps += 1
        arr[largest], arr[i] = arr[i], arr[largest]
        c, s = heapify(arr, size, largest)
    return comps+c, swaps+s

def heapsort(arr):
    comparisons = 0
    swaps = 0
    for i in range( math.floor(len(arr)/2), -1, -1 ):
        c,s = heapify(arr, len(arr), i)
        comparisons += c
        swaps += s
    
    for end in range(len(arr)-1, 0, -1):
        swaps += 1
        arr[0],arr[end] = arr[end],arr[0]
        c,s = heapify(arr, end, 0)
        comparisons += c
        swaps += s

    return comparisons, swaps

### SHARED MEASUREMENT HELPERS ###
# Used by the tests below and by benchmark.py so both treat every algorithm the
# same way. Each SORTERS entry sorts `arr` in place and returns
# (comparisons, swaps).

SORTERS = {
    "quicksort_first":    lambda arr: quicksort(arr, 0, len(arr) - 1, firstPivot),
    "quicksort_last":     lambda arr: quicksort(arr, 0, len(arr) - 1, lastPivot),
    "quicksort_random":   lambda arr: quicksort(arr, 0, len(arr) - 1, randomPivot),
    "quicksort_midpoint": lambda arr: quicksort(arr, 0, len(arr) - 1, midpointPivot),
    "quicksort_median3":  lambda arr: quicksort(arr, 0, len(arr) - 1, medianPivot),
    "mergesort":          lambda arr: mergesort(arr, 0, len(arr) - 1),
    "heapsort":           heapsort,
}

# Each INPUTS entry takes a size n and returns a list of n ints, or None while
# the generator is still a stub (callers skip those).
INPUTS = {
    "random":     generateRandom,
    "backwards":  generateBackwards,
    "sorted":     lambda n: list(range(1, n + 1)),
    "equal":      lambda n: [7] * n,
    "duplicates": lambda n: generateDuplicates(n, n // 2, max(1, n // 10)),
    "killer":     generateKiller,
}


def is_correctly_sorted(original, result):
    """True if `result` is a sorted permutation of `original`."""
    return (
        len(result) == len(original)
        and all(result[i] <= result[i + 1] for i in range(len(result) - 1))
        and Counter(result) == Counter(original)
    )


### TESTING & VALIDATION ###

TEST_SIZES = [0, 1, 2, 3, 10, 1000]


@pytest.mark.parametrize("size", TEST_SIZES)
@pytest.mark.parametrize("input_name", list(INPUTS))
@pytest.mark.parametrize("sorter_name", list(SORTERS))
def test_sort_correctness(sorter_name, input_name, size):
    original = INPUTS[input_name](size)
    if original is None:
        pytest.skip(f"input generator '{input_name}' not implemented yet")

    arr = list(original)
    comparisons, swaps = SORTERS[sorter_name](arr)

    assert is_correctly_sorted(original, arr)
    print(f"{sorter_name} on {input_name}({size}): comparisons={comparisons}, swaps={swaps}")


@pytest.mark.parametrize("input_name", ["random", "backwards", "sorted", "equal"])
@pytest.mark.parametrize("size", [1, 2, 10, 1000, 100000])
def test_mergesort_comparison_bound(input_name, size):
    arr = INPUTS[input_name](size)
    comparisons, _ = SORTERS["mergesort"](arr)
    # mergesort never does more than n * ceil(log2 n) comparisons
    assert comparisons <= size * (size - 1).bit_length()


@pytest.mark.parametrize("input_name", ["random", "backwards", "sorted", "equal"])
@pytest.mark.parametrize("size", [1, 2, 10, 1000, 100000])
def test_heapsort_comparison_bound(input_name, size):
    arr = INPUTS[input_name](size)
    comparisons, _ = SORTERS["heapsort"](arr)
    # each sift-down does <= 2 comparisons per level of a ceil(log2 n)-deep heap
    assert comparisons <= 2 * size * (size - 1).bit_length() + 2 * size


@pytest.mark.parametrize("pivotFunc", [randomPivot, midpointPivot, medianPivot])
def test_partition(pivotFunc):
    arr = generateRandom(1000)
    original = list(arr)
    low, high = 100, 899  # interior subarray, to catch out-of-range bugs
    p, _, _ = partition(arr, low, high, pivotFunc)

    assert low <= p <= high
    assert all(arr[i] <= arr[p] for i in range(low, p))
    assert all(arr[i] > arr[p] for i in range(p + 1, high + 1))
    # elements outside [low, high] are untouched; inside is a permutation
    assert arr[:low] == original[:low] and arr[high + 1:] == original[high + 1:]
    assert Counter(arr[low:high + 1]) == Counter(original[low:high + 1])
