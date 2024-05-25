#test la performance de la création d'une liste avec différentes
#méthode. Idem à performanceFonctions.py, mais avec des appels de fonctions
#dans tous les cas. On voit que les appels de fonctions ralentisse
#la contruction



import time, sys, math
reps = 1000
size = 10000

def tester(func, operation):
    startTime = time.time()
    for i in range(reps):
        func(operation)
    elapsed = time.time() - startTime
    return elapsed

def forStatement(operation):
    res = []
    for x in range(size):
        res.append(operation(x))

def listComprehension(operation):
    res = [operation(x) for x in range(size)]

def mapFunction(operation):
    res = list(map(operation, range(size)))

def generatorExpression(operation):
    g = (operation(x) for x in range(size))
    res = list(g)

print(sys.version)
tests = (forStatement, listComprehension, mapFunction, generatorExpression)
list_operation = [
    ('abs', lambda x: abs(x)),
    ('square', lambda x : x**2),
    ('cube', lambda x : x**3),
    ('sqrt', lambda x : math.sqrt(x)),
]
for name, operation in list_operation:
    print(f"\n{name}")
    for testfunc in tests:
        print(f"{testfunc.__name__:>20} => {tester(testfunc, operation):3f}")
