"""
a basic UI for entering a puzzle 8 board
and solving it
"""

import time
import io
from enum import StrEnum

import flet as ft

from solver import Board, Solver

SPEED = 0.20    # in seconds


class COLORS(StrEnum):                # pylint: disable=missing-class-docstring
    HOLE = "#76453B"
    REGULAR = "#43766C"


class Puzzle8:
    """
    the pieces of the UI
    """

    def __init__(self, page):
        self.page = page
        self.solver = Solver()
        # start with the goal board
        goal_board = Board()
        # ----
        self.squares = [
            ft.TextField(
                value=str(i),
                border_radius=12,
                text_size=40,
                text_align=ft.TextAlign.CENTER,
                bgcolor=COLORS.REGULAR,
                content_padding=ft.padding.all(32),
                on_change=lambda e: self.changed(e),
                on_focus=lambda e: self.focused(e),
            )
            for i in goal_board.internal
        ]

        # header
        self.message_area = ft.TextField(
            disabled=True,
            bgcolor=ft.colors.WHITE,
            color=ft.colors.BLACK,
            expand=True)
        self.header = ft.Row([self.message_area, ])

        # footer
        self.shuffle_button = ft.IconButton(
            ft.icons.SHUFFLE, tooltip="shuffle", icon_size=50,
            autofocus=True,
            icon_color=ft.colors.RED,
            on_click=lambda e: self.shuffle())
        self.solve_button = ft.IconButton(
            ft.icons.START, tooltip="solve", icon_size=50,
            icon_color=ft.colors.GREEN,
            on_click=lambda e: self.solve())
        self.cache_button = ft.IconButton(
            ft.icons.MEMORY,
            tooltip="compute and cache all results", icon_size=50,
            icon_color=ft.colors.BLUE,
            on_click=lambda e: self.cache())
        self.reset_button = ft.IconButton(
            ft.icons.RESTART_ALT, tooltip="reset", icon_size=50,
            icon_color=ft.colors.RED,
            on_click=lambda e: self.reset())
        self.footer = ft.GridView([
            self.shuffle_button,
            self.solve_button,
            self.cache_button,
            self.reset_button,
        ], runs_count=4)

    def reset(self):
        """
        reset to the goal board
        """
        self.show_board(Board())

    def shuffle(self):
        """
        shuffle the board
        """
        self.show_board(Board.random())

    #
    def message(self, *args, **kwargs):
        """
        display a message - args are print-like
        """
        stream = io.StringIO()
        print(*args, **kwargs, file=stream)
        string = stream.getvalue()
        self.message_area.value = string
        # print("MESSAGE", string)
        self.page.update()

    def outline_hole(self):
        """
        outline the hole
        """
        for square in self.squares:
            square.bgcolor = (
                COLORS.HOLE if square.value == "0" else COLORS.REGULAR)
        self.page.update()

    #
    def spot_square(self, value, skip_square=None):
        """
        spot the square that has the given value
        skipping skip_square if provided
        """
        for square in self.squares:
            if square == skip_square:
                continue
            if square.value == value:
                return square

    def missing_value(self, square) -> str:
        """
        assuming all other squares are filled,
        returns the missing value
        """
        missing = set(map(str, range(9)))
        for other in self.squares:
            if other is not square:
                missing.remove(other.value)
        assert len(missing) == 1
        return missing.pop()

    #
    def convert_to_board(self):
        """
        build a board from the current state of the UI
        """
        return Board.from_string(" ".join(s.value for s in self.squares))

    def show_board(self, board):
        """
        update the UI to show the given board
        """
        for s, value in zip(self.squares, board.internal):
            s.value = str(value)
        self.outline_hole()

    def animate(self, path, delay):
        """
        animate the given path
        """
        # first element in path is the current board
        steps = len(path) - 1
        for index, board in enumerate(path[1:], 1):
            self.show_board(board)
            self.message(f"{index}/{steps}")
            self.page.update()
            if index < steps:
                time.sleep(delay)

    def cache(self):
        """
        callback for the cache button
        make sure the solver has cached the full results
        """
        self.message("solving all boards and caching ...")
        self.enable_ui(False)
        begin = time.time()
        self.solver.s_path_cache()
        elapsed = time.time() - begin
        self.message(f"in {elapsed:.3f} s: all results cached ")
        self.enable_ui(True)
        self.page.update()

    def solve(self, delay=SPEED):
        """
        callback for the solve button
        """
        self.message("solving ...")
        self.enable_ui(False)
        begin = time.time()
        board = self.convert_to_board()
        path = self.solver.s_path(board)
        elapsed = time.time() - begin
        if not path:
            self.message(f"in {elapsed:.3f} s: {board} unreachable")
        else:
            self.message(f"in {elapsed:.3f} s: {board} in {len(path)-1} hops")
            self.animate(path, delay)
        self.enable_ui(True)
        self.page.update()

    #
    def changed(self, event):
        """
        callback for when a user has typed some text
        """
        square = event.control
        new = square.value
        # allow to clear textfield
        if not new:
            # see also focus()
            return
        # compute previous content
        previous = self.missing_value(square)
        # validate
        try:
            assert 0 <= int(new) < 9
            # swap with sqaure that had this new value
            previous_square = self.spot_square(new, square)
            previous_square.value = previous
            self.message("")
        except (AssertionError, ValueError):
            self.message(f"invalid value: {new}")
            square.value = previous
        self.outline_hole()
        self.page.update()

    def focused(self, event):
        """
        callback for when a square receives the focus
        """
        # make sure all other squares are filled
        square = event.control
        for other in self.squares:
            if other is not square and not other.value:
                other.value = self.missing_value(other)
        self.outline_hole()
        self.page.update()

    def enable_ui(self, enable=True):
        """
        enable or disable the buttons and squares
        """
        for square in self.squares:
            square.disabled = not enable
        for button in (
                self.solve_button,
                self.shuffle_button,
                self.cache_button,
                self.reset_button):
            button.disabled = not enable
        self.page.update()


def main(page):
    """
    main entry point
    """
    page.title = "Puzzle 8"
    page.window_width = 400
    page.window_resizable = False

    puzzle8 = Puzzle8(page)

    page.add(
        ft.Column([
            puzzle8.header,
            ft.GridView(
                puzzle8.squares,
                runs_count=3),
            puzzle8.footer,
        ])
    )
    puzzle8.outline_hole()


if __name__ == "__main__":
    ft.app(main)
