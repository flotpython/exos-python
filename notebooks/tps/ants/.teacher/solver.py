"""
the core of the ants colony algorithm
"""

import random
import numpy as np
# import itertools

from problem import Problem


### meta parameters

# the weights used in the probability of choosing the next vertex
# pheromone
ALPHA = 2.
# distance
BETA = 2.
# the ratio that remains after evaporation
VAPORISATION = 0.9
# how much pheromones we start with
PHERO_INIT = 1.

# the constant to compute the edges
# WARNING: not a parameter
# this will be set from problem in Solver.__init__()
DIST_WEIGHT = None


### debug
DEBUG = False
# DEBUG = True

def debug(*args, **kwargs):
    if not DEBUG:
        return
    # display large arrays properly
    with np.printoptions(edgeitems=30, linewidth=100000, precision=5):
        args2 = []
        for arg in args:
            args2.append(arg if not isinstance(arg, np.ndarray) else repr(arg))
        print("DBG:", *args2, **kwargs)


class Pheromones:
    """
    pheromones representation
    links are symmetric, so we only store them once
    coded as a triangular matrix, diagonal excluded
    """

    def __init__(self, problem: Problem):
        self.problem = problem
        n = len(problem)
        # initialize to avoid division by zero
        # see random.choices below
        self.edges = PHERO_INIT*np.ones((n, n), dtype=float)

    def __len__(self):
        n, _ = self.edges.shape
        return n

    def __repr__(self):
        return repr(self.edges)

    # use upper right triangle only
    def __getitem__(self, idx2):
        i, j = idx2
        if i == j:
            raise ValueError("no self loop")
        i, j = min(i, j), max(i, j)
        return self.edges[i, j]

    def __setitem__(self, idx2, x):
        i, j = idx2
        if i == j:
            raise ValueError("no self loop")
        i, j = min(i, j), max(i, j)
        i, j = min(i, j), max(i, j)
        self.edges[i, j] = x

    def copy(self):
        clone = Pheromones(self.problem)
        clone.edges = self.edges.copy()
        return clone


class Ant:
    def __init__(self, problem: Problem, pheromones: Pheromones,  start_vertex: int):
        """
        the incoming pheromones object is read only
        """
        self.problem = problem
        self.pheromones = pheromones
        self.start_vertex = start_vertex
        self.current_vertex = start_vertex
        self.possible = set(range(len(self.pheromones))) - {self.current_vertex}
        self.path = [start_vertex]
        self.total = 0

    def pick_next(self):
        weights = []
        # just consider the non visited nodes
        for i in self.possible:
            # for each one, the probability is proportional to this amount
            probability = (
                (self.pheromones[self.current_vertex, i]**ALPHA)
                 / (self.problem.distance(self.current_vertex, i)**BETA)
            )
            weights.append(probability)
        # pick the next vertex
        # random.choices does the weight normalization for us, no need to divide
        # there's one exception though: if all the weights are zero
        # so for now we just ignore this case by starting with a pheromone of 1
        # debug(f"PICK current_vertex={self.current_vertex}")
        # debug(f"PICK {candidates=}")
        # debug(f"PICK distances=", [self.problem.distances[self.current_vertex, candidate] for candidate in candidates])
        # debug(f"PICK {weights=}")
        next_vertex = random.choices(list(self.possible), weights=weights)[0]
        # debug(f"PICK {next_vertex=}")
        self.path.append(next_vertex)
        self.possible.remove(next_vertex)
        self.total += self.problem.distance(self.current_vertex, next_vertex)
        self.current_vertex = next_vertex

    def walk(self):
        # debug(f"{self.pheromones=}")
        debug(f"walk from {self.current_vertex}")
        while self.possible:
            self.pick_next()
        # go back to the start
        self.path.append(self.path[0])
        self.total += self.problem.distance(self.current_vertex, self.path[0])
        return self.total


class Solver:
    """
    the solver class
    """
    def __init__(
            self, problem: Problem, *,
            alpha: float = ALPHA, beta: float = BETA,
            vaporisation: float = VAPORISATION,
            phero_init: float = PHERO_INIT,
            ):
        self.problem = problem
        # set the meta parameters
        global ALPHA, BETA, VAPORISATION, PHERO_INIT
        ALPHA = alpha
        BETA = beta
        VAPORISATION = vaporisation
        PHERO_INIT = phero_init
        # global, but not a parameter
        global DIST_WEIGHT
        DIST_WEIGHT = problem.mean_distance()
        self.pheromones = Pheromones(problem)

    Solution = tuple[list[int], float]

    def solve(self, nb_iterations) -> Solution:
        """
        this is where you should write the algorithm
        it should return a permutation of the indices in problem
        """
        debug(10*'\n')
        debug(f"epoch 0, self.pheromones=\n", self.pheromones)
        for iteration in range(nb_iterations):
            debug(f"\n\n{10*'='} iteration {iteration}")

            # create one ant per starting vertex and make it walk the graph
            ants = [ Ant(self.problem, self.pheromones, start_vertex) 
                     for start_vertex in range(len(self.problem))
                   ]
            for ant in ants:
                ant.walk()
                debug(f"ant {ant.start_vertex} has picked path {ant.path} with total distance {ant.total}")

            # update the pheromones
            self.new_pheromones = self.pheromones.copy()
            # update the edges
            self.new_pheromones.edges *= VAPORISATION

            for ant in ants:
                # # follow the ants path: we artificially add the starting vertex at the end
                # full_path = list(itertools.chain(ant.path, [ant.path[0]]))
                # so we can iterate over the pairs of vertices
                # including the one that returns to the starting point
                debug(f"pheromone contrib for ant #{ant.start_vertex}")
                for i, j in zip(ant.path, ant.path[1:]):
                    debug(f"contrib {i=} {j=} before: {self.new_pheromones[i, j]:.5f}", end=' ')
                    self.new_pheromones[i, j] += DIST_WEIGHT / ant.total
                    debug(f"after: {self.new_pheromones[i, j]:.5f}")
            # adopt the new pheromones
            self.pheromones = self.new_pheromones
            debug(f"after update, self.pheromones=\n", self.pheromones)

        # we're done with the iterations, let's return the best path
        # it's not clear whether the result depends on the starting vertex
        # for now we always start at 0
        best_path = [0]
        remaining = set(range(len(self.problem))) - {best_path[0]}
        while len(best_path) < len(self.problem):
            best = 0
            for i in remaining:
                if self.pheromones[best_path[-1], i] > best:
                    best = self.pheromones[best_path[-1], i]
                    best_candidate = i
            best_path.append(best_candidate)
            remaining.remove(best_candidate)
        distance = self.problem.distance_along_path(best_path)
        return best_path, distance
