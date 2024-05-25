def all_integers(iterable):
    """
    retourne la liste des éléments entiers de iterable
    iterable n'est pas modifié
    """
    # la compréhension fabrique une nouvelle liste
    return [x for x in iterable if isinstance(x, int)]


def keep_only_integers(liste):
    """
    cette fois on suppose que l'entrée est une liste
    et on **modifie** la liste pour ne garder que les entiers
    """
    # attention à ne pas modifier le sujet du for dans le for
    for x in liste[:]:
        if not isinstance(x, int):
            liste.remove(x)
    # on ne retourne rien pour bien montrer à l'appelant
    # qu'on a fait un effet de bord
