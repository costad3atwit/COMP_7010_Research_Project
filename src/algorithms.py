import random
import pytest
from inputs import generateDuplicates, generateBackwards, generateRandom, generateKiller


# pivot functions
def firstPivot(arr, l, h):
    return 0

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

def heapsort(arr):
    #TODO: IMPLEMENT HEAPSORT - ANDREW
    pass

### TESTING & VALIDATION ###

def test_quicksort():
    for f in [firstPivot, lastPivot, randomPivot, medianPivot, midpointPivot]:
        arr = generateRandom(100000)
        total_comparisons, total_swaps = quicksort(arr, 0, len(arr) - 1, f)
        print(f"Total comparisons: {total_comparisons}, Total swaps: {total_swaps}")

# TODO: add generateDuplicates / generateKiller once they're implemented
@pytest.mark.parametrize("generator", [generateRandom, generateBackwards])
@pytest.mark.parametrize("size", [0, 1, 2, 10, 1000, 100000])
def test_mergesort(generator, size):
    arr = generator(size)
    expected = sorted(arr)

    total_comparisons, total_swaps = mergesort(arr, 0, len(arr) - 1)

    assert arr == expected
    # mergesort never does more than n * ceil(log2 n) comparisons
    print(f"Expected O(nlogn): {size * max(0, (size - 1).bit_length())}")
    print(f"Actual: {total_comparisons}")
    assert total_comparisons <= size * max(0, (size - 1).bit_length())
    print(f"{generator.__name__}({size}): comparisons={total_comparisons}, swaps={total_swaps}")

def test_heapsort():
    pass

def test_partition():
    pass

def benchmark_time_complexity(n):
    print(f"Expected O(nlogn): {n * (n.bit_length() - 1)}")
    print(f"Actual: {n}")
    pass