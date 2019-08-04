import random
import itertools
import time

def GetOneRandomNumberInRangeL2(start, end):
    if (start == 0 and end == 0):
        return 0

    if (start == end):
        return start

    #n = random.sample(range(start, end), 1)

    l1 = [i for i in range(start, end)]
    l2 = l1.copy()
    random.shuffle(l2)
    ch = random.choice(l1)
    return l2[ch]

def GetOneRandomNumberInRangeL1(start, end):
    return random.choice(range(start, end))

def GetOneRandomNumberInRangeExcludingOneParticular(start, end, exclude):
    if (start == 0 and end == 0):
        return 0

    if (start == end):
        return start

    if((start <= exclude) and (exclude < end)):
        r1 = range(start, exclude)
        r2 = range(exclude + 1, end)
        return random.choice(list(r1) + list(r2))

    return GetOneRandomNumberInRangeL1(start, end)

def GenerateAllPermutationsOfTheGivenTuple(keyTuple):
    c = [x for x in itertools.permutations(list(keyTuple))]
    return c

#Debug
"""
print(GetOneRandomNumberInRange(0,0))
print(GetOneRandomNumberInRange(5,5))

print("-----")
for x in range(0,2):
    print(GetOneRandomNumberInRange(0,5))
"""