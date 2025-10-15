"""
Conway's Game of Life — interactive Python implementation using pygame.

Requirements: pygame (`pip install pygame`).
"""

import sys
import random
import pygame
from pygame.locals import (
    QUIT, KEYDOWN, K_ESCAPE, K_SPACE, K_c, K_r, K_n, K_UP, K_DOWN, K_SLASH, MOUSEBUTTONDOWN
)

### Configuration
# in pixels
CELL_SIZE = 15
# number of cells horizontally, and vertically
GRID_WIDTH, GRID_HEIGHT = 80, 60
# in pixels
WINDOW_WIDTH, WINDOW_HEIGHT = CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT
# colors in rgb
BG_COLOR = (10, 10, 10)
GRID_COLOR = (40, 40, 40)
CELL_COLOR = (200, 200, 200)
# frames per second for pygame
FPS = 60

# density of random grid
DENSITY = 0.15


def create_grid(randomize=False):
    """
    Return a GRID_HEIGHT x GRID_WIDTH grid of 0/1.
    """
    grid = [
        [0 for _ in range(GRID_WIDTH)]
        for _ in range(GRID_HEIGHT)
    ]
    if randomize:
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                # or grid[y][x] = 1 if random.random() < DENSITY else 0
                grid[y][x] = (random.random() < DENSITY)
    return grid


def draw_surface(surface, grid):
    surface.fill(BG_COLOR)
    # Draw cells
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, CELL_COLOR, rect)
    # Draw grid lines (optional — comment out for performance)
    for x in range(0, WINDOW_WIDTH+1, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT+1, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))


def count_neighbors(grid, x, y):
    """Count living neighbors for cell (x, y) with wrapping edges."""
    total = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx = (x + dx) % GRID_WIDTH
            ny = (y + dy) % GRID_HEIGHT
            total += grid[ny][nx]
    return total


def step(grid):
    """Compute one generation and return the new grid."""
    new = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            neighbors = count_neighbors(grid, x, y)
            if grid[y][x] == 1:
                # Any live cell with two or three live neighbours survives.
                new[y][x] = 1 if neighbors in (2, 3) else 0
            else:
                # Dead cell with exactly three live neighbours becomes a live cell.
                new[y][x] = 1 if neighbors == 3 else 0
    return new


def toggle_cell(grid, mouse_pos):
    mx, my = mouse_pos
    x = mx // CELL_SIZE
    y = my // CELL_SIZE
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        grid[y][x] = 0 if grid[y][x] else 1


def randomize_grid(grid, density=DENSITY):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            grid[y][x] = (random.random() < density)


def draw_help(surface, font):
    help_text = [
        "Conway's Game of Life — Help",
        "",
        "Controls:",
        "Space — start/pause simulation",
        "N — advance one step (when paused)",
        "C — clear grid",
        "R — randomize grid",
        "Up/Down — change simulation speed",
        "Left Click — toggle cell",
        "Right Click — randomize small area",
        "? — show this help",
        "Esc — exit",
        "",
        "Press any key to close this help screen...",
    ]


    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(230)
    overlay.fill((20, 20, 20))
    surface.blit(overlay, (0, 0))


    y_offset = 60
    for line in help_text:
        text = font.render(line, True, (240, 240, 240))
        rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
        surface.blit(text, rect)
        y_offset += 25

    pygame.display.flip()

    # Wait until any key is pressed
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                waiting = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 20)

    grid = create_grid(False)
    running = False
    sim_speed = 10  # steps per second when running
    step_timer = 0.0
    randomize_grid(grid)
    draw_help(screen, font)

    while True:
        dt = clock.tick(FPS) / 1000.0
        step_timer += dt

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    running = not running
                elif event.key == K_c:
                    grid = create_grid(False)
                elif event.key == K_r:
                    randomize_grid(grid)
                elif event.key == K_n:
                    grid = step(grid)
                elif event.key == K_UP:
                    sim_speed = min(sim_speed + 1, 60)
                elif event.key == K_DOWN:
                    sim_speed = max(sim_speed - 1, 1)
                elif event.key == K_SLASH: # '?' key
                    draw_help(screen, font)
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    toggle_cell(grid, event.pos)
                elif event.button == 3:  # right click -> randomize small neighborhood
                    mx, my = event.pos
                    cx = mx // CELL_SIZE
                    cy = my // CELL_SIZE
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            nx = (cx + dx) % GRID_WIDTH
                            ny = (cy + dy) % GRID_HEIGHT
                            grid[ny][nx] = 1 if random.random() < 0.8 else 0

        # Update simulation
        if running and step_timer >= 1.0 / sim_speed:
            grid = step(grid)
            step_timer = 0.0

        # Draw
        draw_surface(screen, grid)

        # HUD
        status = f"Running: {running}    Speed: {sim_speed} steps/s    Cells alive: {sum(sum(row) for row in grid)}"
        text = font.render(status, True, (180, 180, 180))
        screen.blit(text, (5, 5))

        pygame.display.flip()


if __name__ == '__main__':
    main()
