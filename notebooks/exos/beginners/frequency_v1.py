"""
un programme qui calcule le nombre d'occurrences des mots dans un fichier texte
- on entre le nom du fichier par la ligne de commandes
- par défaut on montre les 3 mots les plus fréquents, on peut changer ce nombre
  également sur la ligne de commandes
"""

# v1: un peu mieux car on traite la ponctuation
# mais c'est clairement sous-optimal en termes de complexité
# (près d'un millier de caractères de ponctuation)

from collections import Counter
from argparse import ArgumentParser

# plusieurs options pour calculer une chaine
# qui contient les caractères de ponctuation

# option 0: on entre à la main les caractères de ponctuation
# dans notre texte; bon c'est sous-optimal mais en dernier recours..
# notez l'utilisation de """ comme délimiteur
# PONCTUATION = """,.;'"“”"""

# option 1: ne marche pas bien car seulement ASCII
# from string import punctuation

# option 2: voir le palindrome
from palindrom_v2 import unicode_punctuation
PUNCTUATION = unicode_punctuation()

def compute_counter(filename) -> Counter:
    try:
        with open(filename) as reader:
            text = reader.read().lower()
            # on remplace les caractères de ponctuation par un espace
            for char in PUNCTUATION:
                text = text.replace(char, " ")
            mots = text.split()
            counter = Counter(mots)
            return counter
    except FileNotFoundError:
        print(f"OOPS le fichier {filename} n'existe pas")
        return Counter()


def main():
    parser = ArgumentParser()
    # par défaut on montre les 3 mots les plus fréquents
    parser.add_argument(
        "-n", "--number", default=3, type=int,
        help="the number of words to show")
    parser.add_argument("filename")
    args = parser.parse_args()

    filename = args.filename
    n = args.number

    counter = compute_counter(filename)
    if len(counter) == 0:
        print("vide")
    else:
        for word, occurrences in counter.most_common(n):
            print(word, occurrences)


if __name__ == '__main__':
    main()
