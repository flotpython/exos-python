"""
le fond d'écran, et le serpent peut contenir plusieurs cases
"""

from random import randint
import pygame as pg

W, H = 20, 20
X, Y = 30, 30

WHITE = (240, 240, 240)
BLACK = (255, 255, 255)
SNAKE_COLOR = (128, 128, 0)

snake = [
    (10, 15),
    (11, 15),
    (12, 15),
]


pg.init()
screen = pg.display.set_mode((X*W, Y*H))
clock = pg.time.Clock()


def draw_tile(x, y, color):
    """
    x and y in tiles coordinates
    translate into pixel coordinates for painting
    """
    rect = pg.Rect(x*W, y*H, W, H)
    pg.draw.rect(screen, color, rect)


running = True
while running:

    clock.tick(1)
    # on itère sur tous les évênements qui ont eu lieu depuis le précédent appel
    # ici donc tous les évènements survenus durant la seconde précédente
    for event in pg.event.get():
        # chaque évênement à un type qui décrit la nature de l'évênement
        # un type de pg.QUIT signifie que l'on a cliqué sur la "croix" de la fenêtre
        if event.type == pg.QUIT:
            running = False
        # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
        elif event.type == pg.KEYDOWN:
            # si la touche est "Q" on veut quitter le programme
            if event.key == pg.K_q:
                running = False

    # on dessine le damier
    screen.fill(WHITE)
    for x in range(X):
        for y in range(Y):
            if (x+y) % 2 == 0:
                draw_tile(x, y, BLACK)

    for x, y in snake:
        draw_tile(x, y, SNAKE_COLOR)

    pg.display.update()


# Enfin on rajoute un appel à pg.quit()
# Cet appel va permettre à Pygame de "bien s'éteindre" et éviter des bugs sous Windows
pg.quit()
