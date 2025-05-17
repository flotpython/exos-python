---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# fréquence des mots

+++

## le sujet

il s'agit d'écrire un programme qui lit un fichier texte, et calcule la fréquence
des mots présents dans ce fichier

par exemple ici nous allons afficher les <n> mots les plus fréquents, avec leur nombre d'apparitions  
par exemple avec (ce fichier est fourni)  

```bash
python frequency.py -n 5 frequency-sample.txt
the 65
he 62
a 52
to 52
it 45
```

+++

## un outil bien pratique

pour faire ça, on va utiliser un module de la librairie standard,
`collections.Counter`; entrainez-vous à trouver sa doc sur `docs.python.org`, et à chercher une méthode qui va nous aider à faire ce qui est demandé ici

````{admonition} une méthode en particulier
:class: dropdown

et notamment la méthode `most_common()`
````

+++

## solutions

### v0: très rustique (marche assez mal)

pour montrer comment on utilise `Counter`, on va couper les mots à la serpe avec
`split()`, et on va ignorer la ponctuation

````{admonition} pour voir la v0
:class: dropdown

```{literalinclude} frequency_v0.py
```
````

+++

### v1: un peu comme pour palindrom

ici on va remplacer tous les caractères de ponctuation par des espaces avant de
couper en morceaux avec `split()`; on montre 3 façons d'obtenir ces caractères
de ponctuation (et le mieux c'est d'importer ce qu'on avait fait pour le
palindrome)

````{admonition} la v1
:class: dropdown

```{literalinclude} frequency_v1.py
```
````

+++

### v2: avec les expressions régulières

enfin on montre comment on ferait en vrai; c'est moins lisible car ça utilise
les expressions régulières, un sujet disons un peu aride de prime abord, mais
comme vous pouvez le voir ça donne une solution beaucoup plus propre, et
globablement plus efficace aussi

````{admonition} la v2
:class: dropdown

```{literalinclude} frequency_v2.py
```
````
