"""
This module implements a solver for the puzzle8 game

NOTE: the code still contains sequels of alternative approaches

- the full graph is computed, but not used in either of the two algorithms
- the code supports the A* algorithm; this is how we could assess that in this
  particular instance, given the size of the problem, A* performs slightly
  better as compared to Dijkstra, but at the cost of a slightly more complex
  implementation; however it can still be interesting to compare both
  algorithms on larger sizes

so if we were to keep only the useful code for the Dijkstra algorithm, we would
likely end up with a much shorter code
"""

import random
from typing import Iterator
from math import factorial

from queue import PriorityQueue
from dataclasses import dataclass, field

GOAL = [1, 2, 3, 4, 5, 6, 7, 8, 0]

NEIGHBOURS = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4, 8],
    6: [3, 7],
    7: [4, 6, 8],
    8: [5, 7],
}


class Board:
    """
    represents a board of the puzzle8 game
    encoded as a tuple of the 9 integers 0..8
    """

    manhattan_distance_cache: dict[tuple[int, int], int] = dict()

    def __init__(self, array=None):
        if array is None:
            array = GOAL
        self.internal = tuple(array)
        self.h = hash(self.internal)

    @staticmethod
    def from_string(s):
        """
        convenience method to create a Board from a string
        of the form "1 2 3 4 5 6 7 8 0"
        """
        return Board(map(int, s.split()))

    def to_string(self):
        """
        opposite of from_string
        """
        return " ".join(map(str, self.internal))

    @staticmethod
    def random():
        """
        returns a random board
        """
        return Board(random.sample(range(9), 9))

    def __repr__(self):
        return repr(self.internal)

    # make Board hashable
    # this is crucial for using it as a key in a dictionary
    def __eq__(self, other):
        return self.h == other.h

    def __hash__(self):
        return self.h

    #
    def iter_moves(self) -> Iterator['Board']:
        """
        yields all boards that can be reached in one move
        """
        zero_index = self.internal.index(0)
        neighbours_indices = NEIGHBOURS[zero_index]
        for neighbour_index in neighbours_indices:
            # use a list so we can alter it
            tmp = list(self.internal)
            tmp[zero_index], tmp[neighbour_index] = (
                tmp[neighbour_index], tmp[zero_index])
            yield Board(tmp)

    #
    def parity(self) -> bool:
        """
        computes the parity of the permutation
        """
        # copy as we're going to mess with it
        tmp = list(self.internal)
        n = len(tmp)
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                if tmp[i] > tmp[j]:
                    count += 1
                    tmp[i], tmp[j] = tmp[j], tmp[i]
        assert tmp == list(sorted(self.internal))
        return count % 2 == 0
        #
        # WARNING: approaches based on this code are not correct !
        # parity = 0
        # for i in range(9):
        #     for j in range(i):
        #         if self.internal[j] > self.internal[i]:
        #             parity += 1
        # return parity % 2

    def reachable(self, other) -> bool:
        """
        checks if the board is reachable from the other board
        """
        # for that we do not only compare their parity !
        # because obviously, a board one move away
        # is reachable but has a different parity...
        # instead: the parities must be the same iff
        # their holes are in the same chessboard color
        # think black and white tiles on a chessboard

        self_hole_parity = self.internal.index(0) % 2
        other_hole_parity = other.internal.index(0) % 2
        same_parity = self_hole_parity == other_hole_parity
        same = other.parity() == self.parity()
        return same if same_parity else not same

    #
    # for A* only
    def manhattan_distance(self, other) -> int:
        """
        computes the manhattan distance between two boards
        """

        if not self.manhattan_distance_cache:
            def coords(i):
                return i // 3, i % 3
            for i in range(9):
                for j in range(9):
                    xi, yi = coords(i)
                    xj, yj = coords(j)
                    self.manhattan_distance_cache[(i, j)] = (
                        abs(xi - xj) + abs(yi - yj))
        count = 0
        for i in range(9):
            self_i = self.internal.index(i)
            other_i = other.internal.index(i)
            count += self.manhattan_distance_cache[(self_i, other_i)]
        return count

    def hamming_distance(self, other) -> int:
        """
        computes the hamming distance between two boards
        """
        return sum(
            slot_i != slot_other
            for slot_i, slot_other in zip(self.internal, other.internal))


class Solver:
    """
    provides miscellaneous methods to solve the puzzle8 game

    NOTE: the code for building the full graph is not completely required; it
    did seem to speed up the computation of the shortest path

    """
    def __init__(self):
        # the shortest path from the standard goal
        # will be cached once a full scan is performed
        self.came_from = None
        self.cost_so_far = None

    # for using in PriorityQueue
    @dataclass(order=True)
    class Item:
        """
        used to store items in the priority queue
        """
        priority: int
        board: Board = field(compare=False)

    def s_path_details(self, from_board, goal) -> tuple[
                        dict[Board, Board],
                        dict[Board, int]]:
        """
        computes the details of scanning for the shortest path
        in the graph from from_board to goal

        NOTE: the rest of the code actually calls this with
        reversed parameters, i.e. with the standard goal as from_board
        and the starting point as goal; this is on purpose to allow caching
        the results for the standard goal

        it outputs 2 dictionaries:
        - came_from: a dictionary of the form {board: previous_board}
          that allows to rebuild the path
        - cost_so_far: a dictionary of the form {board: cost} which gives the
          shortest path from from_board for all nodes encountered during the
          search note that passing goal=None will scan the whole connected
          component reachable from from_board from from_board
        """

        # if we have already computed the shortest path from the standard goal
        # we can just reuse the cached results
        if from_board == Board() and self.came_from is not None:
            return self.came_from, self.cost_so_far

        frontier = PriorityQueue()
        frontier.put(self.Item(0, from_board))

        came_from = {from_board: None}
        cost_so_far = {from_board: 0}

        while not frontier.empty():
            current = frontier.get().board

            # passing an unreachable goal (like e.g. None) will scan the whole
            # connected component reachable from from_board
            if current == goal:
                break

            # it appears that using self.graph[current] here improves
            # computation speed, but as computing the graph itself is rather
            # expensive, this is probably not worth the while
            for neighbour in current.iter_moves():
                new_cost = cost_so_far[current] + 1
                if (neighbour not in cost_so_far
                        or new_cost < cost_so_far[neighbour]):
                    priority = new_cost
                    frontier.put(self.Item(priority, neighbour))
                    cost_so_far[neighbour] = new_cost
                    came_from[neighbour] = current
        else:
            # the goal is not reachable so we have scanned the whole connected
            # component reachable from from_board
            # so if from_board is the standard goal,
            # we can cache the results for next time as it contains
            # the shortest path for all nodes in the connected component
            if from_board == Board():
                self.came_from = came_from
                self.cost_so_far = cost_so_far

        return came_from, cost_so_far

    def reconstruct_path(
            self, came_from,
            from_board, goal, reverse: bool) -> list[Board]:
        """
        returns the path from from_board to goal
        using the came_from dictionary
        """
        current = goal
        path = []
        if goal not in came_from:
            return path
        while current != from_board:
            path.append(current)
            current = came_from[current]
        path.append(from_board)
        if reverse:
            path.reverse()
        return path

    def s_path(self, from_board, goal=None) -> list[Board]:
        """
        computes the (one) shortest path in the graph from
        from_board to goal
        """
        if goal is None:
            goal = Board()

        # passing parameters in that order is on purpose
        # to allow caching the results for the standard goal
        # pylint: disable=arguments-out-of-order
        came_from, _ = self.s_path_details(goal, from_board)
        return self.reconstruct_path(came_from, goal, from_board, False)

    def s_path_cache(self):
        """
        dry run of s_path on an unreachable board
        so the results get cached

        returns nothing, but after that all computations
        will return almost instantly

        NOTE: the same result is achived when calling s_path
        with an unreachable goal
        """
        # create a fake unreachable configuration
        # this is to ensure we scan the whole graph
        # when caching the results
        unreachable = GOAL.copy()
        # assumes the hole is neither in the first nor second position
        unreachable[0], unreachable[1] = unreachable[1], unreachable[0]
        # this will scan the whole graph and cache the results
        self.s_path_details(Board(), Board(unreachable))

    # A* algorithm
    def a_star_details(self, from_board, goal) -> tuple[
                        dict[Board, Board],
                        dict[Board, int]]:
        """
        returns the details of scanning using the A* algorithm
        """
        frontier = PriorityQueue()
        frontier.put(self.Item(0, from_board))

        came_from = {from_board: None}
        cost_so_far = {from_board: 0}
        came_from[from_board] = None
        cost_so_far[from_board] = 0

        while not frontier.empty():
            current = frontier.get().board

            if current == goal:
                break

            for neighbour in current.iter_moves():
                new_cost = (cost_so_far[current]
                            + current.manhattan_distance(neighbour))
                if (neighbour not in cost_so_far
                        or new_cost < cost_so_far[neighbour]):
                    cost_so_far[neighbour] = new_cost
                    priority = new_cost + neighbour.manhattan_distance(goal)
                    frontier.put(self.Item(priority, neighbour))
                    came_from[neighbour] = current
        return came_from, cost_so_far

    def a_star(self, from_board, goal=None) -> list[Board]:
        """
        computes the (one) shortest path in the graph from
        from_board to goal which defaults to
        (1, 2, 3, 4, 5, 6, 7, 8, 0) using the A* algorithm

        does NOT use self.graph, and does NOT require to
        have computed the full graph beforehand
        """
        if goal is None:
            goal = Board()

        if not from_board.reachable(goal):
            return []

        came_from, _ = self.a_star_details(from_board, goal)
        # reverse the reconstructed path
        return self.reconstruct_path(came_from, from_board, goal, True)
