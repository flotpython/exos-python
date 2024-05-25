"""
Ce module vérifie que la distributions des nombres aléatoires
en Python est uniforme.
"""

import random

def frequence_rand_v0(maxint = 100, maxtry = 1000000):
    """
	return a dict containing the frequence of random numbers

	maxtin : takes numbers between 1 and maxint
	maxtry : makes maxtry try
    """
    L = []
    for i in range(maxtry):
        L.append(random.randint(1,maxint))

    frequence = {}
    for x in range(1,maxint+1):
        frequence[x] = L.count(x)

    #frequence = {x: L.count(x) for x in range(1, maxint+1)}

    return frequence

def frequence_rand_v1(maxint = 100, maxtry = 1000000):
    """
	return a dict containing the frequence of random numbers

	maxtin : takes numbers between 1 and maxint
	maxtry : makes maxtry try
    """
    L = [random.randint(1,maxint) for i in range(maxtry)]

    frequence = {}
    for x in range(1,maxint+1):
        frequence[x] = L.count(x)

    #frequence = {x: L.count(x) for x in range(1, maxint+1)}

    return frequence

def frequence_rand_v2(maxint = 100, maxtry = 1000000):
    """
	return a dict containing the frequence of random numbers
	This version does not create temporary lists, but only uses
	iterators, it is more memory efficient.

	maxtin : takes numbers between 1 and maxint
	maxtry : makes maxtry try
    """

    frequence = {}
    for i in range(1,maxtry+1):
        a_try = random.randint(1,maxint)
        frequence[a_try] = frequence.setdefault(a_try, 0) + 1

    return frequence

def frequence_rand_v3(maxint = 100, maxtry = 1000000):
    """
	use the collections.Counter to count automatically

	maxtin : takes numbers between 1 and maxint
	maxtry : makes maxtry try
    """

    import collections

    # expression génératrice
    L = (random.randint(1,maxint) for i in range(maxtry))

    return collections.Counter(L)

def print_frequence(frequence):
    """
	print the frequence of random numbers.

	frequence : a dict returned by frequence_rand
    """
    for k, v in frequence.items():
        print(f'{k:>3} {v:>5}')


import timeit
if __name__ == '__main__':
    print(f"v0: {timeit.timeit(stmt='frequence_rand_v0(30)', number=1, globals=globals())}s")
    print(f"v1: {timeit.timeit(stmt='frequence_rand_v1(30)', number=1, globals=globals())}s")
    print(f"v2: {timeit.timeit(stmt='frequence_rand_v2(30)', number=1, globals=globals())}s")
    print(f"v3: {timeit.timeit(stmt='frequence_rand_v3(30)', number=1, globals=globals())}s")
    d = frequence_rand_v0(30)
    print_frequence(d)
