"""
do a gridsearch on the solver meta-parameters
"""

import math
from itertools import product

from problem import Problem2D
from solver import Solver

ITERATIONS = 10

# ALPHAS = [0.1, 0.5, 1, 2, 5]
ALPHAS = [1]
# BETAS = [0.1, 0.5, 1, 2, 5]
BETAS = [1]
# VAPORIZATIONS = [0.1, 0.5, 0.9]
VAPORIZATIONS = [0.64]
# PHERO_INITS = [0.1, 0.5, 1, 2, 5]
PHERO_INITS = [1]

def use_default_parameters():
    global ALPHAS, BETAS, VAPORIZATIONS, PHERO_INITS
    from solver import ALPHA, BETA, VAPORISATION, PHERO_INIT
    ALPHAS = [ALPHA]
    BETAS = [BETA]
    VAPORIZATIONS = [VAPORISATION]
    PHERO_INITS = [PHERO_INIT]


def gridsearch(filename, iterations):
    p = Problem2D(filename)
    best_distance = math.inf
    best_path = None
    best_params = None

    CUBE = (ALPHAS, BETAS, VAPORIZATIONS, PHERO_INITS)
    nb_combinations = len(ALPHAS) * len(BETAS) * len(VAPORIZATIONS) * len(PHERO_INITS)

    for index, hyper_params in enumerate(product(*CUBE), 1):
        (alpha, beta, vaporization, phero_init) = hyper_params
        s = Solver(p, alpha=alpha, beta=beta, vaporisation=vaporization,
                   phero_init=phero_init)
        path, distance = s.solve(iterations)
        print(
            f"{index}/{nb_combinations} "
            f"alpha={alpha} beta={beta} vaporization={vaporization} phero_init={phero_init}"
            f"path={path} distance={distance}")
        if distance < best_distance:
            best_distance = distance
            best_path = path
            best_params = hyper_params

    print(f"best path={best_path} distance={best_distance} with params={best_params}")
    # save in .path file
    # compute max euclidian diameter
    max_diameter = max(p.distance(i, j)
                       for i, j in product(range(len(p)), repeat=2) if i != j)
    for i in range(len(p)):
        for j in range(i+1, len(p)):
            d = p.distance(i, j)
            if d > max_diameter:
                max_diameter = d
    cheated_filename = filename.replace(".csv", ".path")
    with open(cheated_filename, "w") as f:
        import json
        print(f"saving best path to {cheated_filename}")
        json.dump(dict(
            path=best_path,
            distance=best_distance,
            params=best_params,
            iterations=iterations,
            diameter=max_diameter,
        ), f)

from argparse import ArgumentParser
def main():
    parser = ArgumentParser()
    parser.add_argument("filenames", nargs="+",help="the problem filename (csv)")
    parser.add_argument(
        "-i", "--iterations", type=int, default=ITERATIONS,
        help=f"number of iterations per run (default: {ITERATIONS})")
    # useful only to recompute the .path files
    parser.add_argument(
        "-d", "--default-parameters", action="store_true",
        help="use the default parameters from solver.py instead of the gridsearch")

    args = parser.parse_args()
    if args.default_parameters:
        use_default_parameters()
    for filename in args.filenames:
        gridsearch(filename, args.iterations)

if __name__ == "__main__":
    main()
