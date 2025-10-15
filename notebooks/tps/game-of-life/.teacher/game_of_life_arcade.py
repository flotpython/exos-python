"""
Conway's Game of Life implemented with the Arcade library.

Requirements:
    pip install arcade

Arcade provides a clean and modern API for educational visualization.
"""

import arcade
import random

CELL_SIZE = 15
GRID_WIDTH = 80
GRID_HEIGHT = 60
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 60

class GameOfLife(arcade.Window):
    def __init__(self):
        super().__init__(
            WINDOW_WIDTH, WINDOW_HEIGHT,
            "Conway's Game of Life",
            update_rate=1/FPS,
            # resizable=False,
            # antialiasing=False,
            # high_dpi=False,  # 👈 this disables automatic Retina scaling
        )
        arcade.set_background_color(arcade.color.BLACK)

        # Force consistent viewport and window size - avoid resolution being changed by OS scaling
        self.set_viewport(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        self.set_size(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.grid = self.create_grid()
        self.running = False
        self.sim_speed = 10  # steps per second
        self.accumulator = 0.0
        self.show_help = False

    def create_grid(self, randomize=False):
        grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        if randomize:
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    grid[y][x] = 1 if random.random() < 0.2 else 0
        return grid

    def count_neighbors(self, x, y):
        total = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % GRID_WIDTH
                ny = (y + dy) % GRID_HEIGHT
                total += self.grid[ny][nx]
        return total

    def step(self):
        new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                neighbors = self.count_neighbors(x, y)
                if self.grid[y][x] == 1:
                    new_grid[y][x] = 1 if neighbors in (2, 3) else 0
                else:
                    new_grid[y][x] = 1 if neighbors == 3 else 0
        self.grid = new_grid

    def randomize_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                self.grid[y][x] = 1 if random.random() < 0.2 else 0

    def on_draw(self):
        arcade.start_render()
        if self.show_help:
            self.draw_help()
            return

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    arcade.draw_rectangle_filled(
                        x * CELL_SIZE + CELL_SIZE / 2,
                        y * CELL_SIZE + CELL_SIZE / 2,
                        CELL_SIZE - 1,
                        CELL_SIZE - 1,
                        arcade.color.LIGHT_GRAY,
                    )

        text = f"Running: {self.running} | Speed: {self.sim_speed} steps/s | Alive: {sum(sum(r) for r in self.grid)}"
        arcade.draw_text(text, 10, 10, arcade.color.WHITE, 12)

    def draw_help(self):
        arcade.draw_lrtb_rectangle_filled(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0, (20, 20, 20, 230))
        lines = [
            "Conway's Game of Life — Help",
            "",
            "Space — start/pause simulation",
            "N — advance one step (when paused)",
            "C — clear grid",
            "R — randomize grid",
            "Up/Down — change simulation speed",
            "Left Click — toggle cell",
            "? — show this help",
            "Esc — exit",
            "",
            "Press any key to close help...",
        ]
        y = WINDOW_HEIGHT - 80
        for line in lines:
            arcade.draw_text(line, WINDOW_WIDTH / 2, y, arcade.color.WHITE, 16, anchor_x="center")
            y -= 25

    def on_update(self, delta_time):
        if self.show_help:
            return

        if self.running:
            self.accumulator += delta_time
            if self.accumulator >= 1 / self.sim_speed:
                self.step()
                self.accumulator = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if self.show_help:
            self.show_help = False
            return

        gx = int(x // CELL_SIZE)
        gy = int(y // CELL_SIZE)
        if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
            self.grid[gy][gx] = 0 if self.grid[gy][gx] else 1

    def on_key_press(self, key, modifiers):
        import arcade.key as k

        if self.show_help:
            self.show_help = False
            return

        if key == k.ESCAPE:
            arcade.close_window()
        elif key == k.SPACE:
            self.running = not self.running
        elif key == k.C:
            self.grid = self.create_grid(False)
        elif key == k.R:
            self.randomize_grid()
        elif key == k.N:
            self.step()
        elif key == k.UP:
            self.sim_speed = min(self.sim_speed + 1, 60)
        elif key == k.DOWN:
            self.sim_speed = max(self.sim_speed - 1, 1)
        elif key == k.SLASH or key == k.QUESTION:
            self.show_help = True


def main():
    GameOfLife()
    arcade.run()


if __name__ == "__main__":
    main()
