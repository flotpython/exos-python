# pylint: disable=missing-docstring, unspecified-encoding

"""
a minimal test suite
"""

import time

from solver import Solver, Board

problems = []
problems.append(("1 2 3 4 5 6 7 0 8", 1))
problems.append(("1 2 3 4 5 6 0 7 8", 2))
problems.append(("1 2 3 0 5 6 4 7 8", 3))
problems.append(("2 0 3 1 5 6 4 7 8", 5))
problems.append(("5 0 2 1 8 3 4 7 6", 9))
problems.append(("6 1 3 2 0 8 4 7 5", 12))
problems.append(("6 1 8 0 3 2 4 7 5", 15))
problems.append(("6 1 7 2 0 3 5 4 8", 18))
problems.append(("6 1 8 3 4 5 7 0 2", 21))
problems.append(("6 1 5 7 0 8 4 2 3", 24))
problems.append(("6 1 4 5 3 0 8 2 7", 27))
problems.append(("8 6 7 5 0 1 3 2 4", 30))
# this one is unreachable
problems.append(("6 1 7 4 5 2 3 8 0", float('inf')))


def _test_algo(algo_name, algo_method, cache_method=None):
    solver = Solver()

    with open(f"times_{algo_name}.txt", "w") as out:
        if cache_method:
            begin = time.time()
            cache_method(solver)
            print(f"cached in {time.time() - begin:.3f} s", file=out)

        for (b, ed) in problems:
            print(f"----> {b}", file=out)
            begin = time.time()
            path = algo_method(solver, Board.from_string(b))
            if ed == float('inf'):
                ok = "OK" if len(path) == 0 else "KO"
            else:
                # path contains both ends, so it is one more
                # than the number of moves
                ok = "OK" if len(path) == (ed+1) else "KO"
            assert ok == "OK"
            print(
                f"<-{ok}- {algo_method.__name__}:"
                f" {len(path):>12}  vs  {ed+1:<8}"
                f"in {time.time() - begin:.3f} s", file=out)


def test_s_path_slow():
    _test_algo("s_path", Solver.s_path)


def test_a_star_slow():
    _test_algo("a_star", Solver.a_star)


def test_s_path_cached():
    _test_algo("s_path_cached", Solver.s_path, Solver.s_path_cache)

if __name__ == "__main__":
    test_s_path_cached()
