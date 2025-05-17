"""
boucle sans fin jusqu'à ce qu'on entre le mot 'exit'
"""

def is_palindrom(word):
    return word.lower() == word.lower()[::-1]

def main():
    while True:
        mot = input("entrez le mot: ")
        if mot == 'exit':
            print("bye")
            # ici on a le choix: break ou return
            # ---- break
            # je suis dans une boucle, mais qu'il n'y a rien
            # à faire après le while, donc si je fais
            # break
            # je vais effectivement sortir de la boucle, et de la fonction
            # ---- return
            # mais le plus simple, comme je suis dans une fonction
            # c'est de faire tout simplement
            return
        print("oui" if is_palindrom(mot) else "non")


if __name__ == '__main__':
    main()
