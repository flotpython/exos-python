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
  title: "TP: ventes aux ench\xE8res"
---

# ventes aux enchères

+++

Licence CC BY-NC-ND, Thierry Parmentelat & Daniel Garnier-Moiroux

+++

```{admonition} commencez par télécharger le zip
{download}`vous aurez besoin du zip qui se trouve ici<./ARTEFACTS-auctions.zip>`
```

+++

OOP and inheritance ... in Python!

Les intérêts de ce TP

* utiliser l'héritage pour factoriser du code
* utiliser des tests automatisés  
  (c'est une pratique hyper-courante dans la vraie vie: 
   comme ça on détecte tout de suite les régressions sur le code)

+++

## Avant toute chose

+++

### Consignes générales

- Chacune des enchères a déjà un constructeur. Vous pouvez ajouter des choses dans ce constructeur, mais **pas en supprimer**.
- Pour intéragir avec la ligne de commande, vous devez **impérativement** utiliser l'utilitaire `self.cli` qui est dans les enchères.
  - Vous pouvez faire l'équivalent de `print()` en faisant `self.cli.display()`
  - Vous pouvez demander à l'utilisateur de saisir des choses sur la ligne de commande, l'équivalent de `value = input("Entrez une valeur")`, en faisant `value = self.cli.prompt("Entrez une valeur")`
  - L'usage direct de `print()` et `input()` est proscrit, sinon les tests ne marcheront pas
  - Cette classe nous sert à simuler `print` et `input` dans les tests automatisés
- Pour ce TP, vous pouvez estimer que les utilisateurs du programme ne font que des choses "légales"
  - Par exemple, quand on leur demande d'enchérir, ils tapent "10" ou "115", mais ils ne tapent pas "toto 1234 %&@# 💣💩🤮"
  - Par exemple, quand on leur demande de sur-enchérir sur une enchère de 30, ils tapent "45" ou une chaîne vide pour passer leur tour, mais pas "12"
  - Le but n'est pas de tester toutes les possibilités !

+++

### Comment exécuter les tests 

Dans ce TP on vous fournit des tests unitaires, ce qui vous permet de savoir rapidement si vous avez bien respecté les consignes ou non (enfin c'est l'idée, mais il se peut que les tests soient un peu superficiels ici..)

+++

#### depuis le terminal

Vous pouvez tester le code de `blind.py` (normalement le test est OK) en faisant depuis le terminal

```shell
$ python test_blind.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.306s

OK
```

ou encore, si vous avez installé avec `pip install pytest`

```shell
$ pytest test_blind.py
================================ test session starts ================================
platform darwin -- Python 3.10.8, pytest-7.2.0, pluggy-1.0.0
rootdir: /Users/tparment/git/flotpython-exos/python-tps/auctions
plugins: anyio-3.6.2
collected 3 items

test_blind.py ...                                                             [100%]

================================= 3 passed in 0.39s =================================
```

+++

#### depuis VSCode

1. Ouvrez tout le dossier dans VSCode
2. Choisissez sur la gauche l'onglet 'Testing', et configurez les tests Python pour utiliser `unittest`

```{image} media/vscode-test-configure.png
:align: center
```

et aux questions suivantes, répondez:

* Q: `Select the directory containing the tests:`  
  A: `. Root directory`
* Q: `Select the pattern to identify test files:`  
  A: `test_*.py` (vous devez avoir des fichiers de ce genre, comme `test_blind.py`)

3. À ce stade vous devriez voir les testeurs, toujours dans l'onglet gauche `Testing`

```{image} media/vscode-test-explore.png
:align: center
```

+++

---

Mais passons au TP, enfin !

+++

## 1. Blind auction: les règles

Voici les règles des enchères à l'aveugle, ou [Blind auction](https://en.wikipedia.org/wiki/First-price_sealed-bid_auction):

- Les enchères démarrent avec un prix minimum
- Les enchérisseurs doivent sur-enchérir par rapport au prix minimum
- Les enchérisseurs ne savent pas quel est la plus haute enchère (on estime qu'ils ne peuvent pas lire ce que les autres on saisi dans le terminal)
- Il n'y a qu'un seul tour
- Le gagnant est celui qui a proposé le prix le plus haut
- Le prix final est le prix le plus haut proposé

Exemple:

```shell
$ python blind.py
Started auction of type: Blind
Please enter the amount for the opening bid: 50
Opening bid is: 50
Enter name for bidder 1 (enter nothing to move on): alice
Enter name for bidder 2 (enter nothing to move on): bob
Enter name for bidder 3 (enter nothing to move on): carol
Enter name for bidder 4 (enter nothing to move on):

Bidders are: alice, bob, carol

Opening bid is 50. alice bids: 60
Opening bid is 50. bob bids: 80
Opening bid is 50. carol bids: 70

~~~~~~~~

Winner is bob. Winning bid is 80.
```

### 2. Blind auction: le code

🚀 Regardez le fichier `blind.py`, tout a déjà été implémenté pour vous. Lisez le code, exécutez le fichier, faites une partie d'enchères.

Vous pouvez également regarder `test_blind.py` pour avoir une idée de comment les tests sont écrits, si vous êtes curieux.

🚀 Exécutez `test_blind.py`, de préférence avec VS Code. C'est important, parce que vous allez, plus tard dans le TP, modifier `blind.py`.

+++

## 3. English auction: les règles

Vous allez maintenant implémenter des enchères anglaises, ou [English auction](https://en.wikipedia.org/wiki/English_auction). Voici les règles:

- Les enchères démarrent avec un prix minimum
- Les enchérisseurs voient cette fois la plus haute enchère en cours
- Les enchérisseurs doivent sur-enchérir par rapport à la meilleure enchère en cours
- Il y a plusieurs tours
- L'enchère est finie lorsque tous les participants passent leur tour (ne tapent rien dans le terminal)
- Le gagnant est celui qui a proposé le prix le plus haut
- Le prix final est le prix le plus haut proposé

**NOTES**

- un participant qui passe n'est pas éliminé, il peut encore parler au tour suivant s'il y en a un
- du coup la vente s'arrête sur un tour où tous les participants passent


Exemple:

```shell
$ python english.py
Started auction of type: English
Please enter the amount for the opening bid: 30
Opening bid is: 30
Enter name for bidder 1 (enter nothing to move on): alice
Enter name for bidder 2 (enter nothing to move on): bob
Enter name for bidder 3 (enter nothing to move on): carol
Enter name for bidder 4 (enter nothing to move on):

Bidders are: alice, bob, carol

Standing bid is 30. alice bids: 35
Standing bid is 35. bob bids: 40
Standing bid is 40. carol bids:
Standing bid is 40. alice bids: 45
Standing bid is 45. bob bids:
Standing bid is 45. carol bids:
Standing bid is 45. alice bids:
Standing bid is 45. bob bids:
Standing bid is 45. carol bids:

~~~~~~~~

Winner is alice. Winning bid is 45.
```

🚀 Implémentez l'English auction dans `english.py`. Vous avez le droit de tout copier-coller depuis `blind.py` pour commencer! Vous devez exécuter les tests jusqu'à ce que `test_english.py` fonctionne à 100%.

+++

## 4. Mise en commun: le facile

Remarquez maintenant les similitudes entre `blind` et `english`.

🚀 Introduisez une classe de base, par exemple `Auction` dans le fichier `auction.py`, et mutualisez les étapes en commun dans `blind` et `english`, par exemple en introduisant des méthodes ou fonctions spécifiques.

N'oubliez pas d'exécuter les tests de `blind` et `english` pour être sûrs que vous n'avez rien cassé!

+++

## 5. Mise en commun: un peu plus intéressant

🚀 Essayez de ne définir la méthode "play" que dans la classe de base, `auction`. Comment s'y prendre ?

Dans tous les cas, essayez de factoriser au maximum entre les deux modes que l'on a vus jusqu'ici, de façon à minimiser le code qui va être nécessaire pour la 3éme variante que nous allons voir tout de suite.

+++

## 6. Vickrey auction

Il devrait être facile d'implémenter une nouvelle enchère!

Voici les règles des enchères en plis cachetés à un tour au second prix, ou [Enchère de Vickrey](https://en.wikipedia.org/wiki/Vickrey_auction):

- Les enchères démarrent avec un prix minimum
- Les enchérisseurs doivent sur-enchérir par rapport au prix minimum
- Les enchérisseur ne savent pas quel est la plus haute enchère (on estime qu'ils ne peuvent pas lire ce que les autres ont saisi dans le terminal)
- Il n'y a qu'un seul tour
- Le gagnant est celui qui a proposé le prix le plus haut
- Le prix final est la _deuxième enchère la plus haute_

Exemple:

```
Started auction of type: Vickrey
Please enter the amount for the opening bid: 50
Opening bid is: 50
Enter name for bidder 1 (enter nothing to move on): alice
Enter name for bidder 2 (enter nothing to move on): bob
Enter name for bidder 3 (enter nothing to move on): carol
Enter name for bidder 4 (enter nothing to move on):

Bidders are: alice, bob, carol

Opening bid is 50. alice bids: 60
Opening bid is 50. bob bids: 80
Opening bid is 50. carol bids: 70

~~~~~~~~

Winner is bob. Winning bid is 70.
```

🚀 A vous de jouer, comme d'habitude vous avez un fichier de test `test_vickrey.py`. Le cas ci-dessus est intéressant pour votre implémentation.

+++

## 7. Jeu libre

Si vous avez encore le temps, n'hésitez pas à modifier votre programme pour mettre une méthode qui représente "un tour" d'enchères dans la classe de base, et voir comment modifier vos classes filles pour l'utiliser. Pas de test particulier pour ça, mais, comme d'habitude, il ne faut rien casser !

+++

***
