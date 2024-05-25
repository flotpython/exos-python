def countdown(n, step=1):
    """
    generateur qui produit des valeurs allant de n (inclus) à 0 (exclus) par pas de step
    """
    while n > 0:
        yield n
        n = n - step


def dichotomie(inconnue, a, b):
    """
    generator qui produit les étapes d'un algo de dichotomie pour trouver
    inconnue dans l'interval [a,b[
    """

    if inconnue < a or inconnue >= b:
        exit_str = f"{inconnue} not in [{a},{b}["
        print(exit_str)
        return exit_str
    while True:
        half = a + (b - a) // 2
        if inconnue == half:
            yield half
            break
        yield half
        if inconnue > half:
            a = half
        else:
            b = half



def monotonic_decrease(gen):
    """
    generator that takes a generator as parameter an yield only value decreasing monotonically
    """
    last = next(gen)
    yield last
    for val in gen:
        if val <= last:
            last = val
            yield val


for i in countdown(10, step=0.5):
    print(i)

inconnue = 333
min_val = 1
max_val = 1000000
dico_steps = [x for x in dichotomie(inconnue, min_val, max_val)]
print(f"{inconnue} in [{min_val},{max_val}]"
      f" found in {len(dico_steps)} steps."
      " All steps {dico_steps}")


dico = dichotomie(inconnue, min_val, max_val)
mono = monotonic_decrease(dico)
for i in mono:
    print(i)
