"""
the core of the matter
"""

from problem import Problem

class Solver:

    def __init__(self, problem: Problem):
        self.problem = problem


    def solve(self, nb_iterations) -> list[int]:
        """
        this is where you should write the algorithm
        it should return a permutation of the indices in problem
        """
        indices = list(range(len(self.problem)))

        import random
        return random.shuffle(indices)
