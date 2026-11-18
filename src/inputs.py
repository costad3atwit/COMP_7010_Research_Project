import random
import math
import matplotlib.pyplot as plt

MAX_VALUE_MULTIPLIER = 2

def generateDuplicates(size, numDuplicates, maxValue, numGroups=3):
    """Generates a list of size 'size', with "numDuplicates" duplicates split 
        evenly among "numGroups" number of groups in the list. The 
        rest is just randomly selected numbers, all smaller than maxValue"""

    arr = []
    groupSize = numDuplicates//numGroups

    for _ in range(numGroups):
        value = random.randint(1, maxValue)
        arr.extend([value] * groupSize)

    arr.extend(random.randint(1, maxValue) for _ in range(size - numGroups*groupSize))
    random.shuffle(arr)
    return arr


def generateBackwards(size):
    # list comprehension runs at O(n)
    return [size - x for x in range(size)]

def generateRandom(size):
    # random.uniform performs at O(1), list comprehension runs at O(n),
    # runtime of O(n)
    return [int(random.uniform(1, size*MAX_VALUE_MULTIPLIER)) for _ in range(size)]

def generateKiller(size,m,s="SAWTOOTH"): # from the McIlroy paper i found
    # m is just a value that is increased in the original paper like
    # for (m = 1; m < 2*n; m *= 2)
    arr = [0]*size
    i, j = 0, 0; 
    k = 1;
    for i in range(size):
        if s == "SAWTOOTH": arr[i] = i % m
        elif s == "STAGGER":  arr[i] = (i * m + i) % size
        elif s == "PLATEAU":  arr[i] = min(i, m)
        elif "SHUFFLE": # lower values of m seem to be more interesting for this one
            if random.randrange(m) != 0:
                j += 2
                arr[i] = j
            else:
                k += 2
                arr[i] = k
    return arr

if __name__ == "__main__":
    # Example usage
    size = 200
    numDuplicates = size//3
    maxValue = size * MAX_VALUE_MULTIPLIER
    numDuplicateGroups = numDuplicates // 10
    print(f"size: {size} numDuplicates: {numDuplicates}, maxValue: {maxValue}, numDuplicateGroups: {numDuplicateGroups}")
    duplicates_array = generateDuplicates(size, numDuplicates, maxValue, numDuplicateGroups)
    print("Array with duplicates:", duplicates_array)
    print(f"Num distinct elements: {len(set(duplicates_array))}")
    plt.bar([n for n in range(size)],duplicates_array)
    plt.savefig(f"graphs/DUPLICATES.png", dpi=300, bbox_inches="tight")
    plt.cla()


    numDuplicates = size
    maxValue = size * MAX_VALUE_MULTIPLIER
    numDuplicateGroups = 5
    print(f"size: {size} numDuplicates: {numDuplicates}, maxValue: {maxValue}, numDuplicateGroups: {numDuplicateGroups}")
    duplicates_array = generateDuplicates(size, numDuplicates, maxValue, numDuplicateGroups)
    print("Array with duplicates:", duplicates_array)
    print(f"Num distinct elements: {len(set(duplicates_array))}")
    plt.bar([n for n in range(size)],duplicates_array)
    plt.savefig(f"graphs/DUPLICATES2.png", dpi=300, bbox_inches="tight")
    plt.cla()

    backwards_array = generateBackwards(size)
    print("Backwards array:", backwards_array)
    plt.bar([n for n in range(size)],backwards_array)
    plt.savefig(f"graphs/BACKWARDS.png", dpi=300, bbox_inches="tight")
    plt.cla()

    random_array = generateRandom(size)
    print("Random array:", random_array)
    plt.bar([n for n in range(size)],random_array)
    plt.savefig(f"graphs/RANDOM.png", dpi=300, bbox_inches="tight")
    plt.cla()
    
    killer_arrays = "SAWTOOTH","STAGGER","PLATEAU","SHUFFLE"
    for name in killer_arrays:
        arr = generateKiller(size,size//5,name)
        print(f"{name}: {arr}")
        plt.bar([n for n in range(size)],arr)
        plt.savefig(f"graphs/{name}.png", dpi=300, bbox_inches="tight")
        plt.cla()
