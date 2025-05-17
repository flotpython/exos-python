"""
un programme qui calcule le nombre d'occurrences des mots dans un fichier texte
- on entre le nom du fichier par la ligne de commandes
- par défaut on montre les 3 mots les plus fréquents, on peut changer ce nombre
  également sur la ligne de commandes
"""

# une deuxième version en utilisant les expressions régulières

from collections import Counter
from argparse import ArgumentParser

import re

def compute_counter(filename) -> Counter:
    try:
        # ici le fait de lire tout le fichier d'un coup
        # simplifie le code
        with open(filename) as reader:
            text = reader.read().lower()
            words_stream = re.findall(r'\w+', text)
            counter = Counter(words_stream)
            return counter
            # on aurait pu raccourcir ces 4 lignes en une seule:
            # return Counter(re.findall(r'\w+', reader.read().lower()))
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
