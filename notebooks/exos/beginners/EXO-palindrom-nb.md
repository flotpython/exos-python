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

# le palindrome

+++

## le sujet

+++

un palindrome est un mot qui se lit dans les deux sens, par exemple `non`, `radar` ou `kayak`

on vous demande d'écrire un programme `palindrom.py`  

- v0: lorsqu'on le lance avec

  ```bash
  python palindrom.py
  ```

  le programme commence par vous demander d'entrer un mot  
  puis il vous indique si oui ou non c'est un palindrome, et s'arrête

- v1: cette fois le programme continue cette logique jusqu'à ce qu'on entre le
  mot `exit` qui signifie qu'on veut s'arrêter

+++

## solutions

+++

### v0: on traite un seul mot

````{admonition} pour voir la v0
:class: dropdown

```{literalinclude} palindrom_v0.py
```
````

+++

### v1: jusqu'à ce qu'on tape le mot "exit"

````{admonition} la v1
:class: dropdown

```{literalinclude} palindrom_v1.py
```
````

+++

### pour aller plus loin

bien sûr vous pouvez sophistiquer comme vous le sentez; par exemple

- traiter des phrases complètes (enlever la ponctuation)
- accepter les équivalences comme `é` == `e`

+++

#### la ponctuation

si vous vouliez ignorer la ponctuation, la librairie standard vient avec ceci:

  ```python
  import string
  print(string.punctuation)
  ```

  **mais c'est souvent insuffisant** notamment avec le texte en français - par exemple pour les choses comme `«`  
  et pour traiter ces caractères-là vous allez faire plutôt (merci chatgpt :)

```bash
import unicodedata

def unicode_punctuation():
    # U+0000 to U+10FFFF is the full Unicode range
    return {
        chr(i) for i in range(sys.maxunicode)
        if unicodedata.category(chr(i)).startswith('P')
    }
```

+++

#### les accents

de même, si vous voulez admettre que, par exemple  
`Et la marine va venir à Malte` (Victor Hugo)  
est un palindrome, il va vous falloir "projeter" les caractères accentués (ici le `à`, mais aussi `ç`) sur les non-accentués (`a`, `c`, resp.)

  et pour faire ça de nouveau, `unicodedata` vient à notre secours

  ```python
  import unicodedata

  text = "cet été"
  normalized = unicodedata.normalize('NKFD', text)
  print(text)
  -> affiche 'cet ete'
  ```

+++

````{admonition} voici ma version avec ces deux ajouts
:class: dropdown

```{literalinclude} palindrom_v2.py
```
````
