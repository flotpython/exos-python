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
  title: comptages de mots
---

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat</span>
</div>

+++

# EXO: classe sortable et hashable


## hashable

lorsqu'on a vu les types prédéfinis, on a dit qu'on ne pouvait utiliser comme
clés de dictionnaire que des éléments **non mutables**

cela est vrai pour les types prédéfinis du langage, mais pour nos types à nous
(les classes, donc), c'est **plus subtil**:  
de manière générale, les éléments qui peuvent servir de clé dans un dictionnaire (ou être
mis dans un ensemble, c'est le même critère) sont appelés des objets
***hashables***  
et, comme pour tous les autres traits du langage, on peut assez facilement **rendre une classe *hashable***

## sortable

dans une veine similaire:  
pour trier une liste d'objets, on peut customiser l'ordre du tri en passant une fonction

`sorted(L, key=)`

**mais aussi**, il y a une autre façon  
si on veut trier des éléments homogènes - tous de la même classe - on peut assez
facilement **définir un ordre** sur les éléments de la classe

## notre prétexte

pour s'entrainer, nous allons simplement créer une classe `Student`:

- qui modélise un élève avec un nom, un prénom, et pour faire simple une note 
- cette note peut évoluer au cours du temps (par ex. une moyenne générale qui change au cours du trimestre)
- on suppose qu'il n'y a pas deux élèves avec le même nom **et** le même prénom

on veut pouvoir ensuite écrire une classe `Classe`:

- qui contient un **ensemble** (au sens `set` Python) d'élèves
- et/ou un **dictionnaire** (au sens `dict` Python) qui a les élèves comme clés
- et qui sache enfin trier cet ensemble d'élèves par moyenne générale

quelque chose dans le genre de (à compléter évidemment):

```{code-cell} ipython3
class Student:
    pass
```

```{code-cell} ipython3
class Class:

    def __init__(self):
        self._students = set()
    def add(self, student: Student):
        self._students.add(student)

    def ranked(self) -> list[Student]:
        return sorted(self._students)
    # etc..
```

## Indices

* voir le cours ici
  <https://ue12-p24-python.readthedocs.io/en/p24/4-2-dunder-specials-nb.html#classe-sortable-obj-obj2>
