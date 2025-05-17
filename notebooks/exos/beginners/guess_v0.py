"""
un programme qui
- tire au sort un nombre entre 0 et 100
- demande de deviner le nombre n
- indique si la réponse est
  supérieure, inférieure, ou égale à n
- s'arrête lorsqu'on a trouvé
"""

import random

# de mon coté au lieu d'avoir un seul fichier guess.py
# j'ai plusieurs versions countdown_v0.py etc...
# du coup au lieu de faire simplement comme vous
# from countdown import saisie_entier
# je dois faire à la place:
from countdown_v1 import saisie_entier

borne_max = 100
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
