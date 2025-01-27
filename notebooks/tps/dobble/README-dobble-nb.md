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
---

# le jeu de dobble

+++

Licence CC BY-NC-ND, Thierry Parmentelat

+++

```{admonition} commencez par télécharger le zip
{download}`vous aurez besoin du zip qui se trouve ici<./ARTEFACTS-dobble.zip>`
```

+++ {"cell_style": "split"}

Le sujet ici consiste à analyser le contenu du jeu 'dobble'.

Pour ceux qui ne connaissent pas c'est un jeu de cartes visuel où il faut trouver l'objet commun à deux cartes.

Dans sa version la plus classique, chaque carte contient 8 symboles; il existe aussi une version "team" où toutes les cartes ont 10 symboles.

Et ce qui est un peu étonnant, c'est que **pour tout couple de cartes** il y a **exactement un objet commun**, et comme ça naïvement on ne voit pas forcément tout de suite comment sont construits les ensembles pour que ça fonctionne.

+++ {"cell_style": "split"}

![dobble](media/dobble.png)

+++

L'idée ici consiste donc à rétro-concevoir le mécanisme de fabrication des cartes:

On se fixe un nombre **N** de symboles par carte:
* quelle est la logique qui permet de construire un jeu de cartes qui vérifie la bonne propriété  ?
* combien de cartes peut-on construire ?
* combien de symboles faut-il utiliser ?

C'est sans doute autant des maths que de l'info; cet exercice vise principalement à vous entrainer à utiliser les deux modes de raisonnement de manière complémentaire: n'essayez pas de tout faire avec l'ordi, il faut que votre cerveau continue à réfléchir !

+++

## à la main, pour *N* petit

c'est sans doute utile d'essayer de résoudre le problème "à la main" avec un papier et un crayon pour les petites valeurs de N, i.e. pour N de 2 à 4

+++

### vérifier vos conjectures

une fois que vous avez construit vos solutions pour ces 3 valeurs de N, écrivez un code qui vous permet de vérifier que vos solutions sont correctes

**notes**

* je vous impose de créer 3 classes pour représenter respectivement un symbole, une carte, et le paquet de cartes
* il vous faut imaginer un format pour entrer vos solutions; allez au + simple, je vous recommande quelque chose dans le genre de une ligne par carte
* pour ces premiers essais, je vous conseille de prendre des nombres comme symboles
* par exemple, voici une façon possible de représenter, dans un fichier texte, une solution pour N=3  
  votre code est censé *parser* un fichier de ce genre (attention, dans la suite on utilisera du texte plutôt que des nombres)
  ```{literalinclude} data/cards03.txt
  ```

```{code-cell} ipython3
# quelque chose comme ça
# à vous de rendre ceci utilisable

from pathlib import Path


class Symbol:
    """
    chacun des symboles dessinés sur les cartes
    """
    pass


class Card:
    """
    le modèle pour chaque carte du jeu
    """
    pass


class Deck:
    """
    le paquet de cartes
    """
    def __init__(self, filename):
        pass
    def check_unique(self):
        """
        returns True if all cards have exactly one common symbol
        and if not, display a message so one can spot the mistake 
        in the file (line numbers, or otherwise the contents 
                     of the 2 cards that don't comply)
        """
        pass
```

```{code-cell} ipython3
# should return True

Deck("data/cards02.txt").check_unique()
```

```{code-cell} ipython3
# should return True

Deck("data/cards03.txt").check_unique()
```

```{code-cell} ipython3
# should return False and print an error message

Deck("data/cards03-broken.txt").check_unique()
```

### combien de symboles et de cartes

+++

combien trouvez-vous de cartes et de symboles pour ces petites valeurs de N ?

ajoutez les méthodes qui vont bien dans vos classes

+++

pouvez-vous émettre des conjectures par rapport à ces nombres ?  
vérifiez-les sur vos premiers exemples

```{code-cell} ipython3
# à vous

def conjecture(deck):
    """
    retourne True ou False selon que la conjecture est vérifiée
    dans le cas False, on peut imprimer un message pour 
    expliciter le souci
    """
    pass
```

```{code-cell} ipython3
# 
```

## des jeux + réalistes

+++

vous trouverez dans le dossier `data/` deux fichiers `game08.txt` et `game10.txt` qui vous donnent le contenu de deux jeux

* ouvrez ces fichiers dans vscode
* faites tourner votre code sur ces jeux, (en s'adaptant si nécessaire au format de ces fichiers)
* que constatez-vous sur ces jeux par rapport à la conjecture précédente ?
* sauriez-vous proposer d'aménager ces deux jeux pour qu'ils satisfassent la conjecture ?

+++

**indice** observez-vous une sorte de symétrie entre les symboles et les cartes ? pourrait-on même parler de dualité ?

```{code-cell} ipython3
GAMES = G8, G10 = (Deck(f"data/game{i:02}.txt") for i in (8, 10))
```

## construire des jeux *from scratch*

+++

regardez maintenant les fichiers suivants

* `data/cards05.txt`
* `data/cards06.txt`

+++

en partant du premier de ces fichiers, on a produit le diagramme suivant

```{image} media/cards05.svg
:align: center
```

+++

### dessiner

sauriez-vous aménager votre code pour produire un diagramme similaire avec `data06.txt` (qui par ailleurs a été construit selon la même logique)

```{code-cell} ipython3
import matplotlib.pyplot as plt
# with ipympl (which needs to be pip install'ed) 
# we can run on jupyter or vscode
# %matplotlib ipympl
```

```{code-cell} ipython3
# ajoutez dans la classe Deck une méthode draw_map()
```

```{code-cell} ipython3
# une fois que c'est fait vous pouvez appeler

# Deck("data/cards04.txt").draw_map()
```

```{code-cell} ipython3
# ou encore

# Deck("data/cards06.txt").draw_map()
```

pour information vous devriez obtenir quelque chose comme ceci

```{image} media/cards04.svg
:align: center
:width: 300px
```

```{image} media/cards06.svg
:align: center
:width: 400px
```
