---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
language_info:
  name: python
  nbconvert_exporter: python
  pygments_lexer: ipython3
nbhosting:
  title: un agenda tout simple
---

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat &amp; Arnaud Legout</span>
</div>

+++

# agenda

+++

## problème

Il s'agit d'écrire

* un module `agenda.py`
* qui implémente deux fonctions
  * `trouver_entree`
  * `nouvelle_entree`

+++

* `trouver_entree(nom, prenom, champ=None)`

        Cherche l'entrée attachée à (nom, prenom) dans l'agenda, et affiche
        l'agenda complet de (nom, prenom) si champ est None
        ou si le champ est passé à la fonction, seulement ce champ-là
        fonction

        Affiche par exemple pour trouver_entree('jean', 'dupond')
        Agenda pour jean dupond
          - adresse : 6 rue de la gare
          - tel : 04040404040

        Affiche par exemple pour trouver_entree('jean', 'dupond', 'tel')
        tel pour jean dupond : 04040404040

* `nouvelle_entree(nom, prenom, champ=None, valeur=None)`

        Cree une entree dans un agenda avec comme clef le tuple (nom, prenom)
        et comme valeur de dictionnaire {champ:valeur}

        nom : le nom de la personne
        prenom : le prenom de la personne
        champ : le champ a entrer dans l'agenda (parmi la liste les champs_valides)
        valeur : la valeur du champ

+++

Que l'on peut utiliser comme ceci

```{code-cell} ipython3
from agenda import nouvelle_entree, trouver_entree

nouvelle_entree('jean', 'dupond')
```

```{code-cell} ipython3
nouvelle_entree('jean', 'dupond', 'tel', '04040404040')
nouvelle_entree('jean', 'dupond', 'adresse', '6 rue de la gare')
```

```{code-cell} ipython3
nouvelle_entree('jean', 'francois', 'tel', '060606060')
nouvelle_entree('jean', 'francois', 'fax', '060606061')
```

```{code-cell} ipython3
nouvelle_entree('eric', 'dupont', 'mail', 'eric.dupont@google.com')
```

```{code-cell} ipython3
trouver_entree('jean', 'dupond')
trouver_entree('jean', 'dupond', 'tel')
```

```{code-cell} ipython3
try:
    trouver_entree('eric', 'françois')
except KeyError as e:
    print("OOPS pas trouvé", e, type(e))
```

## solution

````{admonition} ouvrez-moi
:class: dropdown

```{literalinclude} agenda.py
```
````
