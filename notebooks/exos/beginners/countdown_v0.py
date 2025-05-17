"""
un programme qui:
demande à l'utilisateur un nombre
puis affiche le nombre, attend une seconde, affiche le nombre -1, ...
jusqu'à zéro O et le programme s'arrête
"""

import time

def countdown(n):
    # en Python on écrirait ceci
    while n:
    # qui en fait veut dire ceci
    # while n != 0:
        print(n)
        time.sleep(1)
        n -= 1
    print(0)

if __name__ == '__main__':
    timeout = int(input("entrez le nombre de secondes: "))
    countdown(timeout)
