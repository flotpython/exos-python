"""
un exercice très basique pour approfondir les formats de chaines
et notamment la méthode str.format()
"""


def percents_at_cg(dna):
    total = len(dna)
    at, cg = 0, 0
    for n in dna:
        if n in 'AT':
            at += 1
        else:
            cg += 1
    return at/total, cg/total


def nice_format(dna):
    print(f"Pourcentages pour le brin {dna}")
    at, cg = percents_at_cg(dna)
    print(f"AT = {at:.2%}")
    print(f"CG = {cg:.2%}")


def format_dna(dna, user_format):
    at, cg = percents_at_cg(dna)
    at, cg = [f"{x:.2%}" for x in (at, cg)]
    # à ce stade dans locals nous avons
    # dna, at et cg
    return user_format.format(**locals())


# dans la vraie vie, pour le décompte on utiliserait plutôt ceci
from collections import Counter

def percents_at_cg_bis(dna):
    total = len(dna)
    counts = Counter(dna)
    # Counter({'G': 25, 'C': 21, 'A': 16, 'T': 15})
    return (counts['A']+counts['T'])/total,\
        (counts['C']+counts['G'])/total
