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

lorsqu'on a vu les types prédéfinis, on a dit qu'on ne pouvait utiliser comme clés de dictionnaire que des éléments **non mutables**

en réalité, les éléments qui peuvent servir de clé dans un dictionnaire (ou être mis dans un ensemble, c'est le même critère) sont appelés des objets ***hashables***

et, comme pour tous les autres traits du langage, on peut assez facilement rendre une classe *hashable**

## sortable

pour trier une liste d'objets, on peut customiser l'ordre du tri en passant une fonction

`sorted(L, key=)`

**mais aussi**, il y a une autre façon  
si on veut trier des éléments homogènes - tous de la même classe - il suffit de définir un ordre sur les éléments de la classe

## notre prétexte

pour s'entrainer, nous allons simplement créer une classe

- qui modélise un élève avec un nom, un prénom, et pour faire simple une note 
- cette note peut évoluer au cours du temps (par ex. une moyenne générale qui change au cours du trimestre)
- on suppose qu'il n'y a pas deux élèves avec le même nom **et** le même prénom
- on veut pouvoir, pour écrire la classe `Classe`, créer un ensemble d'élèves
- et trier cet ensemble d'élèves par moyenne générale
- et pouvoir créer un dictionnaire qui a les élèves comme clés

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
  https://ue12-p24-python.readthedocs.io/en/p24/4-2-dunder-specials-nb.html#classe-sortable-obj-obj2
