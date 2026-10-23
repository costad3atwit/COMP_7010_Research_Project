import random
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


for f in [firstPivot, lastPivot, randomPivot, medianPivot, midpointPivot]:
    arr = generateRandom(100000)
    total_comparisons, total_swaps = quicksort(arr, 0, len(arr) - 1, f)
    print(f"Total comparisons: {total_comparisons}, Total swaps: {total_swaps}")
