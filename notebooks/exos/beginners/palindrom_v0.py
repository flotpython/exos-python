"""
un programme qui demande un mot et dit si c'est un palindrome
"""

def is_palindrom(word):
    # c'est plus robuste de projeter le mot en minuscule
    word = word.lower()
    # on tire simplement profit du slicing
    return word == word[::-1]

def main():
    mot = input("entrez le mot: ")
    # maintenant je dois afficher le résultat
    # ---- on pourrait faire ceci
    # if is_palindrom(mot):
    #     print("oui")
    # else:
    #     print("non")
    # ---- en Python on fait plutôt comme ceci
    # d'abord je décompose pour qu'on comprenne bien
    # message = "oui" if is_palindrom(mot) else "non"
    # print(message)
    # ---- ce qui fait qu'à la fin comme je n'ai pas vraiment
    # besoin de la variable message, j'écris juste ceci
    print("oui" if is_palindrom(mot) else "non")


if __name__ == '__main__':
    main()
