"""
on ajoute un carré fixe - le début du serpent
historique - ne correspond plus à aucune étape de l'énoncé
"""

from random import randint
import pygame as pg

pg.init()
screen = pg.display.set_mode((400, 300))
clock = pg.time.Clock()

random_color = (randint(0, 255), randint(0, 255), randint(0, 255))
screen.fill(random_color)

# on rajoute une condition à la boucle: si on la passe à False le programme s'arrête
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

    x = 100 # coordonnée x (colonnes) en pixels
    y = 100 # coordonnée y (lignes) en pixels
    width = 30 # largeur du rectangle en pixels
    height = 30 # hauteur du rectangle en pixels
    rect = pg.Rect(x, y, width, height)
    # appel à la méthode draw.rect()
    color = (255, 0, 0) # couleur rouge
    pg.draw.rect(screen, color, rect)

    pg.display.update()


# Enfin on rajoute un appel à pg.quit()
# Cet appel va permettre à Pygame de "bien s'éteindre" et éviter des bugs sous Windows
pg.quit()
