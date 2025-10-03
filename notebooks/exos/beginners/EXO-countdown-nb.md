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

# compte à rebours

+++

## le sujet

+++

on vous demande d'écrire un programme `countdown.py`  
lorsqu'on le lance avec

```bash
python countdown.py
```

il commence par vous demander de taper le nombre de secondes que vous voulez
attendre, et les décompte, et s'arrête une fois arrivé à 0

+++

## comment poser une question à l'utilisateur

pour faire ça on utilise la fonction *builtin* `input()`  
ça se présente comme ceci

```bash
reponse = input("vous avez quel âge ? ")
### ici dans la variable `reponse` on a **une chaine**
print(f"vous avez répondu {reponse}")
```

```{admonition} ça retourne une chaine
du coup pensez bien à convertir cette réponse en entier !
```

+++

## comment attendre

pour attendre un certain temps, on utilise en Python la fonction `sleep` dans le
module `time`  
ça se présente comme ceci

```python
import time
# pour attendre une demie-seconde
time.sleep(0.5)
```

+++

## solutions

+++

### une version v0 un peu naïve

ça fonctionne, mais on ne contrôle pas l'entrée de l'utilisateur:
si on entre autre chose qu'un entier positif ça se passe mal

````{admonition} pour voir la v0
:class: dropdown

```{literalinclude} countdown_v0.py
```
````

+++

### v1: un peu mieux

cette fois on continue de poser la question jusqu'à ce qu'on reçoive un entier

````{admonition} la v1
:class: dropdown

```{literalinclude} countdown_v1.py
```
````

+++

### quelques remarques

* dans un premier temps on avait écrit la fonction `saisie_entier()` et le texte
  de la question était *cablé* à l'intérieur;  
  mais dans un exercice suivant, on a voulu réutiliser cette fonction, d'où le paramètre

* il reste un défaut ici; pouvez-vous voir lequel ?
  ```{admonition} réponse
  :class: dropdown
  que se passe-t-il si on entre un entier négatif ?
  ```
