# implementer une fonction basique qui demande une phrase et 
# retourne un message positif si la phrase contient 'bien', 
# un message negatif si la phrase contient 'mal', et un message
# "tu n'est pas bavard" si elle est vide

def watson():
    """
    demarre le docteur watson

    parameter
    ---------
    aucun

    return
    ------
    None
    """
    phrase = input("bonjour, à vous: ").lower()

    if "mal" in phrase:
        print("Ohhhh, c'est triste.")
    elif "bien" in phrase:
        print("C'est super.")
    elif not phrase:
        print("Tu n'es pas bavard.")
    else:
        print("je ne comprends pas...")

    print("C'est fini, au revoir !")

if __name__ == "__main__":
    watson()
