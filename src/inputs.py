import random

MAX_VALUE = 100000000

def generateDuplicates(size, numDuplicates, capRange):
    pass

def generateBackwards(size):
    # list comprehension runs at O(n)
    return [size - x for x in range(size)]

def generateRandom(size):
    # random.uniform performs at O(1), list comprehension runs at O(n),
    # runtime of O(n)
    return [int(random.uniform(1, MAX_VALUE)) for _ in range(size)]

def generateKiller(k:int): # from the McIlroy paper i found
    pass

