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

# les anagrammes

+++

## le sujet

+++

très similaires au palindrome, sauf que cette fois-ci:

- on travaille sur deux mots
- et on regarde s'ils sont l'anagramme l'un de l'autre

deux mots sont des anagrammes si ils sont composés des mêmes lettres, mais dans un ordre différent  
on vous demande d'écrire un programme `anagrams.py`  

- v0: lorsqu'on le lance avec

  ```bash
  python anagrams.py
  ```

  le programme commence par vous demander d'entrer deux mots  
  puis il vous indique si oui ou non ce sont des anagrammes, et s'arrête

- v1: cette fois le programme continue cette logique jusqu'à ce qu'on entre le
  mot `exit` qui signifie qu'on veut s'arrêter

+++

## solutions

+++

### v0: on traite un seul couple de mots

````{admonition} pour voir la v0
:class: dropdown

```{literalinclude} anagrams_v0.py
```
````

+++

### v1: jusqu'à ce qu'on tape `exit`

````{admonition} la v1
:class: dropdown

```{literalinclude} anagrams_v1.py
```
````
