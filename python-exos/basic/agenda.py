"""
Ce module permet de créer un agenda simple pour pratiquer les dictionnaires.

Le but de l'exercice est de définir une fonction qui crée un agenda sous
forme d'un dictionnaire qui a la forme suivante
{ (marc, durant) : {'tel' : '0101010101', 'adresse' : '6 rue de la gare'} ,
  (eric, dupont) : {'tel' : '0101010101', 'adresse' : '18 avenue des oliviers'}}

et de définir une fonction qui lit une entrée de l'agenda et retourne
sur le terminal le contenu de cette entrée.
"""


# on utilise une globale (de module) pour ranger les données
# évidemment ça a des avantages et des inconvénients
agenda = {}

champs_valides = {'tel', 'adresse'}


def nouvelle_entree(nom, prenom, champ=None, valeur=None):
    """
    Crée une entrée dans un agenda
      avec comme clef: le tuple (nom, prenom)
      et comme valeur: valeur

    nom : le nom de la personne
    prenom : le prenom de la personne
    champ : le champ a entrer dans l'agenda (parmi la liste champs_valides)
    valeur : la valeur du champ
    """
    key = (nom, prenom)
    if champ == None and valeur == None:
        if key in agenda:
            print(f"efface l'entrée pour {key}")
            agenda[key] = {}
        else:
            agenda[key] = {}
            print(f"crée l'entrée pour {key}")
    elif valeur == None:
        if champ in agenda[key]:
            print(f"efface le champ {champ} de valeur {agenda[key][champ]} pour l'entrée {key}")
            agenda[key][champ] = ''
    else:
        if champ in champs_valides:
            if key not in agenda:
                agenda[key] = {champ: valeur}
            agenda[key][champ] = valeur


def trouver_entree(nom, prenom, champ=None):
    """
    si champ est None (ou si on ne passe pas de 3eme argument)
      * affiche l'agenda complet de (nom, prenom)
    sinon:
      * affiche l'entrée correspondant à champ

    Affiche par exemple pour trouver_entree('jean', 'dupond')
    Agenda pour jean dupond
      - adresse : 6 rue de la gare
      - tel : 04040404040

    Affiche par exemple pour trouver_entree('jean', 'dupond', 'tel')
    tel pour jean dupond : 04040404040
    """
    key = (nom, prenom)

    if champ:
        if key in agenda and champ in agenda[key]:
            print(f"{champ} pour {' '.join(key)} : {agenda[key][champ]}")
    else:
        print(f"Agenda pour {' '.join(key)}")
        for k, v in agenda[key].items():
            print(f"  - {k} : {v}")
