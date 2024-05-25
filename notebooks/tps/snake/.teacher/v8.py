# on affiche le score (la taille du serpent) dans la bannière
# game over si le serpent se marche dessus
# game over si on sort du cadre

from random import randint
import pygame as pg

W, H = 20, 20
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

### en toute rigueur les variables
# DIRECTION et FRUIT devraient être en minuscules

DIRECTION = DIRECTIONS['RIGHT']

snake = [
    (10, 15),
    (11, 15),
    (12, 15),
]

FRUIT = (10, 10)


pg.init()
screen = pg.display.set_mode((X*W, Y*H))
clock = pg.time.Clock()


def draw_background():
    screen.fill(WHITE)
    for x in range(X):
        for y in range(Y):
            if (x+y) % 2 == 0:
                draw_tile(x, y, BLACK)


def draw_tile(x, y, color):
    """
    x and y in tiles coordinates
    translate into pixel coordinates for painting
    """
    rect = pg.Rect(x*W, y*H, W, H)
    pg.draw.rect(screen, color, rect)


def in_scope(tile):
    x, y = tile
    return 0 <= x < X and 0 <= y < Y

def quit(snake, reason):
    print(f"Game over ({reason}) with a score of {len(snake)}")
    pg.quit()
    exit()

def move_snake(snake, direction):
    global FRUIT
    # the new first piece is based on the current first piece
    head = snake[-1]
    # compute it
    x, y = head
    dx, dy = direction
    new_head = (x+dx , y+dy)
    if new_head == FRUIT:
        snake.append(FRUIT)
        FRUIT = (randint(0, X-1), randint(0, Y-1))
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

running = True
while running:

    clock.tick(4)

    # on itère sur tous les évênements qui ont eu lieu depuis le précédent appel
    # ici donc tous les évènements survenus durant la seconde précédente
    for event in pg.event.get():
        #print(f"{event=}")
        # chaque évênement à un type qui décrit la nature de l'évênement
        # un type de pg.QUIT signifie que l'on a cliqué sur la "croix" de la fenêtre
        if event.type == pg.QUIT:
            running = False
        # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                DIRECTION = DIRECTIONS['DOWN']
            elif event.key == pg.K_UP:
                DIRECTION = DIRECTIONS['UP']
            elif event.key == pg.K_RIGHT:
                DIRECTION = DIRECTIONS['RIGHT']
            elif event.key == pg.K_LEFT:
                DIRECTION = DIRECTIONS['LEFT']
            # si la touche est "Q" on veut quitter le programme
            elif event.key == pg.K_q:
                running = False

    move_snake(snake, DIRECTION)
    draw_background()
    for x, y in snake:
        draw_tile(x, y, SNAKE_COLOR)
    draw_tile(*FRUIT, FRUIT_COLOR)

    pg.display.update()


# Enfin on rajoute un appel à pg.quit()
# Cet appel va permettre à Pygame de "bien s'éteindre" et éviter des bugs sous Windows
pg.quit()
