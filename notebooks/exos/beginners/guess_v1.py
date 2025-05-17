"""
par rapport à la v1, on peut changer la borne sur la ligne de commande
"""

import random
from argparse import ArgumentParser

from notebooks.exos.beginners.countdown_v0 import saisie_entier

# pour utiliser argparse, cette ligne est toujours la même
parser = ArgumentParser()
# ici on définit ce qu'on peut ajouter ou pas sur la ligne de commande
parser.add_argument("-m", "--max", default=100, help="la borne maximum", type=int)
# de nouveaux ces deux lignes sont toujours les mêmes
args = parser.parse_args()

# et à ce stade dans la variable args on a les informations
borne_max = args.max

print(f"entre 0 et {borne_max}")
toguess = random.randint(0, borne_max)

while True:
    yourguess = saisie_entier("votre choix ")
    if yourguess > toguess:
        print("trop grand")
    elif yourguess < toguess:
        print("trop petit")
    else:
        print("Yes !!!")
        break
