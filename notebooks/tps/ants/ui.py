# pylint: disable=missing-docstring

import itertools
from pathlib import Path

import flet as ft
import flet.canvas as cv

from problem import Problem2D
from solver import Solver

RIGHT_MARGIN, BOTTOM_MARGIN = 50, 250
START_SIZE = 100
INPUT_SIZE = 70

MIN_WIDTH, MIN_HEIGHT = 600, 300

class AntsUi(ft.Column):

    def __init__(self, page):

        # we need this so we can modify the app width / height
        self.page = page
        # the problem at hand
        self.problem = None
        self.filename = None
        # the path to draw
        self.solution = None

        # the UI
        pick_files_dialog = ft.FilePicker(on_result=self.pick_files_callback)
        load_button = ft.ElevatedButton(
            "Load file",
            on_click=lambda _: pick_files_dialog.pick_files(
                allow_multiple=False
            ))

        iteration_input = ft.TextField(
            label="Iters",
            # value="20",
            value="1",
            width=INPUT_SIZE,
            on_submit=lambda e: self.solve(),
        )
        alpha_input = ft.TextField(
            label="Alpha",
            value="1",
            width=INPUT_SIZE,
            on_submit=lambda e: self.solve(),
        )
        beta_input = ft.TextField(
            label="Beta",
            value="1",
            width=INPUT_SIZE,
            on_submit=lambda e: self.solve(),
        )
        solve_button = ft.ElevatedButton(
            "Solve",
            on_click=lambda e: self.solve(),
        )
        cheat_button = ft.ElevatedButton(
            "Cheat",
            on_click=lambda e: self.cheat(),
        )

        distance_area = ft.TextField(label="Distance", disabled=True)
        show_labels = ft.Checkbox(
            "Show labels",
            value=False,
            # value=True,
            on_change=lambda e: self.refresh(),
        )
        message_area = ft.Text()

        header = ft.Column([
            ft.Row([load_button, pick_files_dialog,
                    iteration_input, alpha_input, beta_input,
                    solve_button, cheat_button,
                    show_labels],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
            distance_area,
            message_area,
        ])

        canvas = cv.Canvas(expand=True)

        # this is a column and its children are:
        super().__init__([header, canvas])

        # keep references for further use in the other methods
        self.iteration_input = iteration_input
        self.alpha_input = alpha_input
        self.beta_input = beta_input
        self.solve_button = solve_button
        self.distance_area = distance_area
        self.show_labels = show_labels
        self.message_area = message_area
        self.canvas = canvas


    def message(self, message):
        self.message_area.value = message
        self.message_area.update()

    def pick_files_callback(self, e: ft.FilePickerResultEvent):
        match e.files:
            case []:
                print("empty selection")
                return
            case first, second, *_:
                print("multiple selection not supported")
                return
            case [single]:
                self.load_problem(single.path)

    def load_problem(self, filename):
        self.problem = Problem2D(filename)
        self.filename = filename
        self.solution = None
        self.distance_area.value = ""
        self.refresh()
        try:
            short_name = Path(filename).name
        except Exception:
            short_name = filename
        self.message(f"Loaded {len(self.problem)} nodes from {short_name}")

    def clear(self):
        self.canvas.shapes = []
        # self.page.update()

    def refresh(self):
        self.clear()
        # draw the path first so it's behind the nodes
        self.draw_path()
        self.draw_problem()
        try:
            path, distance = self.solution
            self.distance_area.value = f"{distance:.2f}"
        except TypeError:
            self.distance_area.value = "n/a"
        # do not forget to update the view
        self.page.update()

    def draw_problem(self):
        # the pencil to use
        paint = ft.Paint(style=ft.PaintingStyle.FILL, color=ft.Colors.RED)
        text_style = ft.TextStyle(font_family="Arial", size=10, color=ft.Colors.GREEN)

        for index, n in enumerate(self.problem):
            self.canvas.shapes.append(
                cv.Circle(n.x, n.y, 5, paint))
            if self.show_labels.value:
                self.canvas.shapes.append(
                    cv.Text(n.x+10, n.y - 10, n.name, style=text_style))
            else:
                self.canvas.shapes.append(
                    cv.Text(n.x+10, n.y - 10, str(index), style=text_style))
        self.page.window.width = max(max(n.x for n in self.problem) + RIGHT_MARGIN, MIN_WIDTH)
        self.page.window.height = max(max(n.y for n in self.problem) + BOTTOM_MARGIN, MIN_HEIGHT)
        # self.page.update()

    def draw_path(self):
        if not self.solution:
            return
        stroke_paint = ft.Paint(
            stroke_width=1, style=ft.PaintingStyle.STROKE, color=ft.Colors.BLUE)
        path, distance = self.solution
        chain = list(itertools.chain(path, [path[0]]))
        for i, j in zip(chain, chain[1:]):
            n1, n2 = self.problem[i], self.problem[j]
            self.canvas.shapes.append(
                cv.Line(n1.x, n1.y, n2.x, n2.y, stroke_paint))
        # self.page.update()

    def solve(self):
        if self.problem is None:
            self.message("No problem loaded")
            return
        self.solve_button.enabled = False
        self.iteration_input.enabled = False
        self.update()
        self.message("Solving...")
        self.page.update()
        solver = Solver(self.problem,
                        alpha=float(self.alpha_input.value),
                        beta=float(self.beta_input.value))
        try:
            iterations = int(self.iteration_input.value)
        except ValueError:
            self.message("Invalid number of iterations")
            self.solve_button.enabled = True
            self.iteration_input.enabled = True
            return
        self.solution = solver.solve(iterations)
        self.refresh()
        self.solve_button.enabled = True
        self.iteration_input.enabled = True
        self.message("done !")
        self.page.update()

    def cheat(self):
        if self.problem is None:
            self.message("No problem loaded")
            return
        if not self.filename:
            self.message("No file loaded")
            return
        cheated_filename = self.filename.replace(".csv", ".path")
        short_name = Path(cheated_filename).name
        self.message(f"Cheating: loading path from {short_name}...")
        path = []
        import json
        with open(cheated_filename) as f:
            cheat = json.load(f)
            path = cheat["path"]
        if len(path) != len(self.problem):
            self.message(f"Invalid path length found in {cheated_filename}")
            return
        distance = self.problem.distance_along_path(path)
        self.solution = path, distance
        self.message(f"Displaying Cheated path from {short_name}")
        self.refresh()


def main(page):
    page.window.width = START_SIZE + RIGHT_MARGIN
    page.window.height = START_SIZE + BOTTOM_MARGIN
    page.window.top = 10
    page.window.left = 800
    ants_ui = AntsUi(page)
    page.add(ants_ui)
    # for convenience during development
    ants_ui.load_problem("data/video-06.csv")
    page.update()
    # ants_ui.solve()

ft.app(main)
