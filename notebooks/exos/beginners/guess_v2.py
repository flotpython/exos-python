"""
un programme qui
- tire au sort un nombre entre 0 et 100
- demande de deviner le nombre n
- indique si la réponse est
  supérieure, inférieure, ou égale à n
- s'arrête lorsqu'on a trouvé
"""

import random
from argparse import ArgumentParser

from notebooks.exos.beginners.countdown_v0 import saisie_entier

parser = ArgumentParser()
parser.add_argument("-m", "--max", default=100, help="la borne maximum", type=int)
args = parser.parse_args()
borne_max = args.max

print(f"entre 0 et {borne_max}")
toguess = random.randint(0, borne_max)
# print(toguess)

while True:
    yourguess = saisie_entier("votre choix ")
    if yourguess > toguess:
        print("trop grand")
    elif yourguess < toguess:
        print("trop petit")
    else:
        print("Yes !!!")
        break
