from problem import Problem2D

from solver import Solver

def demo_solver():
    p = Problem2D("data/video-10.csv")
    s = Solver(p)
    path, distance = s.solve(20)
    print("found path=", path, "distance=", p.distance_along_path(path))

demo_solver()