#test la performance de recherche d'element dans des type built-in
import time, sys
reps = 3
size = 10000

def tester(func):
    startTime = time.time()
    for i in range(reps):
        func()
    elapsed = time.time() - startTime
    return elapsed

def searchTuple():
    T = tuple(range(size));
    for x in range(size):
        x in T

def searchList():
    T = range(size);
    for x in range(size):
        x in T

def searchIter():
    T = range(size);
    for x in range(size):
        x in T

def searchDictKeys():
    T = {x:x for x in range(size)};
    for x in range(size):
        x in T

def searchDictValues():
    T = {x: x for x in range(size)};
    Val = T.values()
    for x in range(size):
        x in Val

def searchSet():
    T = set(range(size));
    for x in range(size):
        x in T

print(sys.version)
tests = (searchTuple,searchList , searchIter, searchDictKeys, searchDictValues, searchSet )
for testfunc in tests:
    print(f"{testfunc.__name__:>20} => {tester(testfunc)}")
