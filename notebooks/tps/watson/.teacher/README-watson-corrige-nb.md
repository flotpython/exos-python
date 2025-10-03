---
jupytext:
  encoding: '# -*- coding: utf-8 -*-'
  main_language: python
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
  show_up_down_buttons: true
  title: 'TP: Dr Watson'
---

# Dr Watson

+++

Licence CC BY-NC-ND, Thierry Parmentelat

+++ {"tags": ["prune-cell"]}

````{admonition} nothing to prune
:class: warning

there are no difference - apart from this very cell - between the teacher and the student version, but the notebook is duplicated in .teacher for consistency
````

+++

```{admonition} commencez par télécharger le zip
{download}`vous aurez besoin du zip qui se trouve ici<./ARTEFACTS-watson.zip>`
```

+++

## préparatifs

### `input()`
voyez la fonction `input()` pour poser une question et lire la réponse dans le terminal  
essayez vous-même

```python
# pour poser la question et avoir la réponse
reponse = input("une question: ")

# le retour de input(), c'est directement la chaine qu'on a tapée, sans newline ni rien
print(reponse)
```

### notebooks

si vous envisagez de faire ce TP dans un notebook, [assurez-vous de bien lire cette section](#label-autoreload)

+++

## v1: un coup, les mots-clé en dur

on veut écrire un programme qui

* pose une question, du genre `bonjour, à vous: `
* attend la réponse tapée par l'utilisateur
* puis:
  * selon que la réponse contient **le mot `bien`** ou **le mot `mal`**  
    on affiche un message positif ou négatif (par exemple `C'est super!` et `Ohhhh, c'est triste.`)

  * si la phrase est vide par contre, on affiche `Tu n'es pas bavard.`
  * enfin si rien de tout cela, on affiche `Je ne comprends pas`
* dans tous les cas après la première réponse le programme s'arrête


une session pourrait ressembler à ceci

```
>>> watson()
bonjour, à vous: j'ai mal dormi aujourd'hui
Ohhhh, c'est triste.
C'est fini, au revoir !
>>>
```

```{code-cell} ipython3
# pour ceux qui travaillent dans un notebook

def watson():
    ...

watson()
```

### solution v1

````{admonition} ouvrez-moi
:class: dropdown

une façon de faire la v1

```{literalinclude} watson1.py
```
````

+++

## v2 - les mots-clé dans une liste

on change un peu le code; on veut reconnaitre les phrases positives ou négatives sur la base de plusieurs mots; par exemple

```
NEGATIVE_WORDS = ["mal", "triste", "marre"]
POSITIVE_WORDS = ["bien", "super", "content", "contente"]
```

+++

````{admonition} indice
:class: tip admonition-small

toujours pour ceux qui travaillent dans un notebook:  
faites descendre votre cellule de code pour qu'elle soit toujours près de la consigne;  
pour cela sélectionner la cellule, assurez-vous d'être en mode 'commande' et tapez `Ctrl-Shift-↓`  
ou encore click-drag avec la souris, dans la zone à gauche de la cellule
````

+++

## v3 - meilleure idée ?

est-ce que de mettre les mots-clés dans une liste c'est une bonne idée ?
est-ce qu'on peut améliorer la performance du code du coup ?

+++

## v4 - les mots-clé dans un fichier

on veut pouvoir définir les mots-clé dans un fichier; on choisit le format suivant

```
$ cat watson.txt
POSITIVE bien super content contente
NEGATIVE mal triste marre
```

ajoutez dans votre code une fonction
`init_watson(filename)` qui retourne - par exemple - un tuple de deux ensembles de mots

+++

## v5 - boucle sans fin

au lieu de faire le traitement une seule fois, on va le faire indéfiniment; pour que tout de même on puisse sortir de là, on rajoute une nouvelle catégorie de mots dans le fichier de config:

```
$ cat watson-config.txt
POSITIVE bien super content contente
NEGATIVE mal triste marre
EXIT bye quit exit
```

et si un des mots de la phrase est contenu dans la nouvelle catégorie on arrête le programme complètement; c'est-à-dire qu'une session ressemblerait à ceci

```
>>> watson()
bonjour, à vous: j'ai bien dormi
C'est super, mais encore...
j'ai mal au dents
Ohhhh, c'est triste, mais encore...
c'est fini
je ne comprends pas...
je veux dire exit
C'est fini, au revoir !
>>>
```

+++

### solution v5

````{admonition} ouvrez-moi
:class: dropdown

une façon de faire la v5

```{literalinclude} watson5.py
```
````

+++

## v6 - rendre la fonction réglable

+++

* on veut pouvoir passerà la fonction `watson()`
  * un paramètre `config` (qui par défaut vaut `"watson-config.txt"`)
  * un paramètre `debug` (qui par défaut est `False`), et s'il est mis, on affiche un message qui montre où on a trouvé le mot

+++

```
# on utilise un autre fichier de config, et en mode debug
>>> watson("watson-config.en", True)
sdfsdf
je ne comprends pas...
awesome this morning
DEBUG: *awesome* this morning
C'est super, mais encore...
had a nice dream
DEBUG: had a *NICE* dream
C'est super, mais encore...
exit
C'est fini, au revoir !
```

+++

## v7 - refactoring

+++

on décide de refactorer le code en créant des classes; par exemple

* une classe `Feeling` correspondant à chacun des deux ensembles de mots
* une classe `Sentence` qui sera crée pour chaque réponse
* une classe `Watson` qui est l'application elle-même
* ... 

en option, on peut aussi en faire un vrai programme Python qui se lance depuis la ligne de commande (voir pour ça la librairie `argparse`)

+++

### solution v7

````{admonition} ouvrez-moi
:class: dropdown

une façon de faire la v7

```{literalinclude} watson7.py
```
````

+++

## etc..

c'est toujours améliorable... par exemple:

* on pourrait imaginer mettre les réponses aussi dans le fichier de config
  dans ce cas un autre format serait sans doute mieux adapté; que pensez-vous de yaml dans ce contexte ?

* ...
