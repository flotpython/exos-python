# # a snake game

# on affiche le score (la taille du serpent) dans la bannière
# game over si le serpent se marche dessus
# game over si on sort du cadre

import pygame as pg
from random import randint


# the size of a tile, in pxels
W, H = 20, 20

# the game size, in tiles
X, Y = 30, 30

WHITE = (240, 240, 240)
BLACK = (255, 255, 255)
SNAKE_COLOR = (128, 128, 0)
FRUIT_COLOR = (192, 16, 16)

DIRECTIONS = {
    'DOWN':  (0, +1),
    'UP':    (0, -1),
    'RIGHT': (+1, 0),
    'LEFT':  (-1, 0),
}


# game state
# globals to keep it simple

direction = DIRECTIONS['RIGHT']

# tail first, head last
snake = [
    (10, 15),
    (11, 15),
    (12, 15),
]

fruit = (10, 10)


# initialize pygame
# need to do it early so screen and clock are defined
pg.init()
screen = pg.display.set_mode((X*W, Y*H))
clock = pg.time.Clock()


def draw_tile(x, y, color):
    """
    fill tile at coords x, y in given color

    x and y in tiles coordinates
    """
    # translate into pixel coordinates for painting
    rect = pg.Rect(x*W, y*H, W, H)
    pg.draw.rect(screen, color, rect)


def draw_background():
    screen.fill(WHITE)
    for x in range(X):
        for y in range(Y):
            if (x+y) % 2 == 0:
                draw_tile(x, y, BLACK)


def in_scope(tile) -> bool:
    """
    check if tile is within the game boundaries
    """
    x, y = tile
    return 0 <= x < X and 0 <= y < Y


def quit(snake, reason):
    print(f"Game over ({reason}) with a score of {len(snake)}")
    pg.quit()
    exit()

def move_snake(snake, direction):
    global fruit
    # the new first piece is based on the current first piece
    head = snake[-1]
    # compute it
    x, y = head
    dx, dy = direction
    new_head = (x+dx , y+dy)
    if new_head == fruit:
        snake.append(fruit)
        fruit = (randint(0, X-1), randint(0, Y-1))
        pg.display.set_caption(f"Score: {len(snake)}")
    elif new_head in snake:
        quit(snake, "self-bite")
    elif not in_scope(new_head):
        quit(snake, "out-of-board")
    else:
        # the last item in snake just vanishes
        _tail = snake.pop(0)
        # insert as the new head
        snake.append(new_head)


def main():

    global direction

    running = True
    while running:

        clock.tick(4)

        # iterating over all the events that occurred since the previous call to pg.event.get()
        for event in pg.event.get():
            #print(f"{event=}")  # debug
            # each event has a type that describes its kind
            # type == pg.QUIT means the user has clicked the red cross in the the window header
            if event.type == pg.QUIT:
                running = False
            # type == pg.KEYDOWN means a keyoard key was pressed
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    direction = DIRECTIONS['DOWN']
                elif event.key == pg.K_UP:
                    direction = DIRECTIONS['UP']
                elif event.key == pg.K_RIGHT:
                    direction = DIRECTIONS['RIGHT']
                elif event.key == pg.K_LEFT:
                    direction = DIRECTIONS['LEFT']
                # pressing the 'q' key also means quit the programm
                elif event.key == pg.K_q:
                    running = False

        move_snake(snake, direction)
        draw_background()
        for x, y in snake:
            draw_tile(x, y, SNAKE_COLOR)
        draw_tile(*fruit, FRUIT_COLOR)

        pg.display.update()


    # Enfin on rajoute un appel à pg.quit()
    # Cet appel va permettre à Pygame de "bien s'éteindre" et éviter des bugs sous Windows
    pg.quit()

main()