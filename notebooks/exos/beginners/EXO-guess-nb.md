---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# deviner un nombre

+++

## le sujet

+++

on vous demande d'écrire un programme `guess.py`  

- v0: lorsqu'on le lance avec

  ```bash
  python guess.py
  ```

  le programme commence par tirer au sort un nombre entre 0 et 100;  
  puis il vous propose de deviner ce nombre; pour cela il vous demande quel
  nombre vous choississez, et vous indique si vous avez trouvé, ou si vous
  choisi trop grand, ou trop petit;   
  le programme continue jusqu'à ce que vous trouviez le bon nombre

- v1: on veut pouvoir fixer cette borne max sur la ligne de commande, en faisant

  ```bash
  python --max 1000 guess.py
  ```

bien sûr vous pouvez sophistiquer comme vous le sentez; par exemple ajouter un
compteur pour dire combien d'essais il a fallu pour trouver, etc...

+++

## comment tirer au sort

pour cela on utilise le module `random`  
allez sur la page de la documentation officielle et cherchez la bonne fonction
pour faire ça  

le plus simple pour trouver cette page est de
- partir de google
- et de chercher `python module random`  
- choisissez bien la page de `docs.python.org` (elle existe en français si vous
  préferez à l'anglais)

````{admonition} la réponse
:class: dropdown
```python
import random
aleatoire = random.randint(0, 100)
```
````

+++

## comment poser une question à l'utilisateur

plutôt que de récrire le même code que dans `countdown.py` (on a vu que c'était
non trivial si on veut le faire proprement) on va **réutiliser** la fonction
`saisie_entier()` qu'on avait fait à ce moment-là:

```python
# pour pouvoir réutiliser la fonction saisie_entier
# qui se trouve dans le fichier countdown
from countdown import saisie_entier

borne = saisie_entier("borne max: ")
print(f"le nombre à deviner est entre 0 et {borne}")
```

+++

## comment utiliser la ligne de commandes

ça se fait avec un module spécialisé qui s'appelle `argparse`  
vous pouvez chercher de votre coté pour trouver des exemples d'utilisation, ou
simplement aller voir la solution ci-dessous  
(et oui, c'est un peu du charabia, mais c'est tellement utile qu'on s'habitue
assez vite si on en a besoin 🙂)

+++

## solutions

+++

### une version v0

le nombre est entre 0 et 100, on ne peut pas changer la borne

````{admonition} pour voir la v0
:class: dropdown

```{literalinclude} guess_v0.py
```
````

+++

### v1: on peut changer la borne sur la ligne de commande

````{admonition} la v1
:class: dropdown

```{literalinclude} guess_v1.py
```
````
