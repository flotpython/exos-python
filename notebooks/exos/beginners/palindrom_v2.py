"""
une version plus réaliste qui traite les accents et la ponctuation français
ça nous emmène un peu loin pour des débutants évidemment, mais si intérêt...
"""

import sys
import unicodedata

def to_ascii(text):
    """
    Normalize the Unicode string to decompose combined letters and diacritics
    """
    normalized = unicodedata.normalize('NFKD', text)
    # Encode to ASCII bytes, ignoring characters that can't be encoded (like emojis)
    ascii_bytes = normalized.encode('ASCII', 'ignore')
    # Convert back to string
    return ascii_bytes.decode('ASCII')


# on utilise les métadonnées de chaque caractère Unicode
# pour calculer la liste des caractères de ponctuation
def unicode_punctuation():
    """
    returns a set with ALL the punctuation characters (there are 842 !)
    """
    def qualifies(c):
        category = unicodedata.category(c)
        return (
            # P stands for punctuation
            category.startswith('P')
            # These ones are spaces
            or category == 'Zs')

    return {
        chr(i) for i in range(sys.maxunicode)
        if qualifies(chr(i))
    }


# on le range dans une variable, pas besoin de recalculer ça tout le temps
PUNCTUATION = unicode_punctuation()

def is_palindrom(word):
    # on le met en minuscules
    word = word.lower()
    # on enlève la ponctuation
    for sign in PUNCTUATION:
        word = word.replace(sign, '')
    # on remplace les accents par un équivalent
    word = to_ascii(word)

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
