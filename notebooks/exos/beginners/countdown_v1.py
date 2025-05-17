"""
on améliore la saisie, pour les cas où
- on se trompe
- on en a assez et on veut quitter le programme
"""

import time

def countdown(n):
    while n:
        print(n)
        time.sleep(1)
        n -= 1
    print(0)

def saisie_entier(message):
    while True:
        try:
            return int(input(message))
        # si on entre une valeur qui ne peut pas être traduite en entier
        except ValueError:
            print("je n'ai pas compris...")
        # si l'utilisateur en a assez, il tape Control-C
        except KeyboardInterrupt:
            print("bye")
            exit(1)

if __name__ == '__main__':
    countdown(saisie_entier("entrez le nombre de secondes: "))
