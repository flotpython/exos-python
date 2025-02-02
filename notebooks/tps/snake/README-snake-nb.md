---
jupytext:
  main_language: bash
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

# Le snake

+++ {"tags": [], "slideshow": {"slide_type": ""}}

Licence CC BY-NC-ND, Thierry Parmentelat & Aurélien Noce

+++

````{admonition} pas besoin de zip
pour faire ce TP, vous avez seulement besoin de cet énoncé en HTML, qui contient le code de démarrage
````

+++

Le but de ce TP est de réaliser un petit jeu en Python. L'objectif est de vous
apprendre à concevoir et réaliser un programme complet, et non de réaliser le
nouveau best-seller.

Gardez en tête que votre objectif est de réaliser un **programme qui marche**, et
pas un programme parfait.

+++

## Objectifs et démarche

on va commencer par se créer un dossier vierge

````bash
$ mkdir mysnake
$ cd mysnake
````

````{admonition} un dépôt git

si vous êtes déjà dans un dépôt git (par exemple le dépôt pour rendre vos devoirs), pas de souci;  
dans le cas contraire (ou si vous êtes dans un dépôt de cours), il vous faut
initialiser le dossier `mysnake` **comme un dépôt `git`** (on fait comment déjà ?)
````

+++

## Mode d'emploi

Votre travail se passe exclusivement **dans un seul fichier `snake.py`**,
que vous allez d'abord créer avec vs-code - à partir du code de démarrage -
puis modifier (et le moins possible d'ailleurs) à chaque étape

````{admonition} pas de Jupyter
:class: warning

le code ne va pas fonctionner dans un notebook Jupyter !  
vous êtes invités à travailler directement dans vs-code - et c'est l'occasion d'apprendre à s'en servir un peu mieux
````

Et ensuite, on va bien faire attention de **committer chaque fois** qu'on aura **une version qui marche**  
c'est-à-dire dans ce TP très guidé, **un commit par étape** en gros !

Et comme ça quand on aura un bug on pourra se concentrer sur **ce qui a changé** depuis la version qui marchait

Enfin si vous créez votre dépôt à l'intérieur d'un autre dépôt (de cours par
exemple), reportez-vous à la toute dernière section pour comprendre comment ça
fonctionne.

Mais avant de pouvoir commencer, un peu de préparation...

+++

## On s'installe (optionnel)

_Ce qui suit suppose que vous avez installé Python avec `conda` et que vous avez
un terminal `bash` fonctionnel sur votre ordinateur._

Commencez par créer et activer un environnement dédié au TP:

````bash
# on commence par créer un environnement "snake"
(base) $ conda create -n snake python=3.12

# puis on l'active
(base) $ conda activate snake

# votre terminal doit indiquer le nom d'environnement:
(snake) $
````

````{admonition} le prompt doit vous montrer l'environnement actif
:class: danger

si vous ne voyez pas, comme montré ici, le `(snake)` affiché dans le
*prompt* de bash pour vous rappeler en permanence dans quel environnement on se
trouve, il vous faut taper ceci avant de relancer un terminal

```bash
$ conda init bash
```

Reportez-vous plus bas pour une liste des commandes qui nous permettent de gérer
les environnements virtuels conda.
````

+++

## Prérequis

Installez ensuite la dernière version du module `pygame` avec `pip`:

````bash
(snake) $ pip install pygame
````

Pour tester votre installation, vous pouvez lancer le programme d'exemple comme suit:

````bash
(snake) $ python -m pygame.examples.aliens
````

soyez patient lors du premier lancement, la librairie initialise des tas de choses...

Sachez aussi que vous pouvez aussi voir la version installée d'une librairie avec

````bash
(snake) pip show pygame
````

+++

## v01: Code de démarrage

Un premier code très simple est le suivant, écrivez-le dans un fichier
`snake.py`

````{literalinclude} snake-01.py
````

et lancez-le avec la commande `python` :

````bash
(snake) $ python snake.py
````

````{admonition} on ne peut pas fermer la fenêtre !
:class: error

c'est normal, le code de démarrage est simpliste  
du coup à ce stade vous ne pouvez **pas _fermer_ la fenêtre**
normalement (par exemple en cliquant sur la croix qui d'habitude ferme la fenêtre)  
pour quitter le programme vous devez saisir **CONTROL+C** dans
le terminal.
````

````{admonition} pas depuis un notebook !
:class: dropdown warning

**ATTENTION** il **ne faut PAS** essayer d'exécuter ce code **depuis
un notebook**, ça ne fonctionne pas  
vous allez rencontrer des problèmes mystérieux de kernel qui
meurt, si vous essayez.
````

Nous avons une version qui marchouille; du coup on en fait quoi ?
> un commit bien sûr

+++

## Astuces vs-code

**Astuce #1** : il est **fortement recommandé** d'installer l'extension de
vs-code pour Python

**Astuce #2** : on a créé un environnement virtuel;
du coup il est opportun d'indiquer à vs-code qu'il faut utiliser l'environnement conda `snake` -
plutôt que `base`
pour cela cliquer dans la bannière du bas la zone qui indique le Python courant

`````{admonition} un screenshot
:class: dropdown

````{div}
```{image} media/vscode-which-python.png
:align: center
:width: 600px
```
````
`````

**Astuce #3** : une fois que c'est fait, pour lancer le programme directement
depuis vs-code :

- ouvrir la palette
  * `⇧ ⌘ P` Shift-Command-P (mac)
  * `⇧ ⌃ P` Shift-Control-P (windows)
- chercher la fonction *Toggle Terminal*
  - mémoriser le raccourci clavier
  - qui est Control-backtick sur Mac (le backtick c'est `)

**Astuce #4** : si vous voulez avoir en permanence une indication
sur la qualité de votre code, regardez la zone en bas à gauche


`````{admonition} un screenshot
:class: dropdown

````{div}
```{image} media/vscode-problems.png
:align: center
```
````
`````

+++

## Un petit détail: update()

Il faut savoir que c'est l'appel à `pg.display.update()` qui produit réellement
l'affichage.

En fait, tous les autres calculs se produisent en mémoire (c'est très rapide),
mais à un moment il faut bien parler à la carte vidéo pour l'affichage, et ça
c'est **beaucoup plus lent** (+ieurs centaines de fois plus lent).

Du coup, même si ce `display.update()` reste dans l'ordre de grandeur de la
milliseconde, il faut s'efforcer, pour une bonne fluidité du jeu, de n'appeler
`update()` que le minimum, pour nous ici **une fois par itération de la
boucle** (une fois par frame, quoi)

+++

## v02: Continuons

Afin d'avoir un comportement plus "normal", nous devons instruire Pygame en lui
disant comment réagir aux clicks sur le clavier ou sur la fenêtre:

```{literalinclude} snake-02.py
```

- lisez bien ce code
- éventuellement regardez la différence avec la v0
  - pour cela dans vs-code il y a la fonction *File: Compare active file with ...*
- et faites-le tourner pour voir le changement de comportement

et on n'oublie pas de faire un commit...

+++

## v03: Le damier

Nous allons commencer par construire notre plateau de jeu ainsi:

- le plateau de jeu est découpé en 30x30 cases
- chaque case fait 20 pixels de côté

pour la v3 vous devez remplacer dans la v2 le code qui affiche (la couleur random)
pour obtenir le damier ci-dessous (vous pouvez bien sûr choisir d'autres couleurs):

`````{admonition} un screenshot
:class: dropdown

````{div}
```{image} media/damier.png
:align: center
:width: 600px
```
````
`````

pour cela, vous pouvez utiliser la méthode
[`pg.draw.rect()`](https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect)
qui dessine un rectangle:

````python
# une recette pour dessiner un rectangle:

# les coordonnées de rectangle que l'on dessine
x, y = 100, 200            # les coordonnées du coin du rectangle (en pixels)

# la taille du rectangle
width, height = 20, 20     # largeur et hauteur du rectangle, toujours en pixels

# on crée un objet 'Rect'
rect = pg.Rect(x, y, width, height)

# la couleur de remplissage
color = (255, 0, 0)        # couleur rouge

# et on le dessine comme ceci dans l'écran virtuel
pg.draw.rect(screen, color, rect)
````

````{admonition} conseils
- il peut être utile d'écrire une fonction qui afficher tout le damier
- il peut être utile de se définir des variables pour le nombre de tuiles et les dimensions des tuiles
````

une fois que ça marche, vous faites quoi ?

+++

## v04: Un serpent fixe

À partir de maintenant, on va garder le damier comme fond d'écran (même si les
illustrations ne le montrent pas)

L'étape suivante est de dessiner le serpent. Le serpent est simplement une suite
de blocs de couleurs. On veut dessiner le serpent aux coordonnées suivantes:

````python
# les coordonnées du corps du serpent
snake = [
    (10, 15),
    (11, 15),
    (12, 15),
]
````

pour obtenir un schéma comme suit; disons pour fixer les idées que dans ce cas
de figure `(10,15)` est la queue, et `(12, 15)` est la tête (mais c'est
totalement arbitraire et pas du tout imposé) :

`````{admonition} un screenshot
:class: dropdown

````{div}
```{image} media/serpent-fixe.png
:align: center
:width: 600px
```
````
`````

+++

## v05: Un serpent qui bouge

Ensuite, nous allons faire bouger le serpent. C'est en fait très simple:

- nous créons un vecteur de "direction"
  ```python
  direction = (1, 0)
  ```
- à chaque itération de la boucle, nous pouvons déplacer le serpent dans cette
  direction en "ajoutant" ce vecteur à la position de la tête du serpent

dans la v5 donc, le serpent avance vers la droite à chaque itération, mais on ne peut pas encore le controler

n'oubliez pas de *commit*

+++

## v06: On peut contrôler la direction

Une fois que le serpent bouge, ajouter les commandes pour se déplacer dans les 4
directions, en cliquant sur les flèches (par exemple le code renvoyé par la
flêche vers le haut est `pg.K_UP`)

Aussi on peut commencer à envisager d'accélérer un peu le jeu à ce stade...

**BONUS** faites en sorte que le serpent ne puisse pas faire "demi tour"

`````{admonition} un gif animé
:class: dropdown

````{div}
```{image} media/serpent-bouge.gif
:align: center
:width: 600px
```
````
`````

+++

## v07: Le fruit

Il faut maintenant faire manger notre serpent.
On va procéder comme suit:

- on a toujours la position du serpent dans une variable `snake` :
- on génère un "fruit", dans une position aléatoire
  ```python
  # exemple de fruit en position 10, 10 sur le plateau
  fruit = (10, 10)
  ```
- quand la tête du serpent mange le fruit, on place un nouveau fruit à une
  position aléatoire et on allonge le serpent d'une case

`````{admonition} un gif animé
:class: dropdown

````{div}
```{image} media/manger.gif
:align: center
:width: 600px
```
````
`````

+++

## v08: Épilogue

Il nous reste deux petits changements pour avoir un serpent complètement fonctionnel:

- tout d'abord il faut détecter si le serpent se mord la queue, ce qui est une
  condition d'échec
- enfin on peut afficher le score. La façon la plus simple de procéder est de
  changer le titre de la fenêtre, avec la fonction `set_caption()`:
  ```python
  score = 0
  pg.display.set_caption(f"Score: {score}")
  ```

`````{admonition} un screenshot
:class: dropdown

````{div}
```{image} media/score.png
:align: center
:width: 600px
```
````
`````


***
Fin de la partie obligatoire
***

+++

## Options

Pour les rapides, je vous invite à aborder les sujets suivants (dans l'ordre qui
vous inspire le plus):

+++

### Variables globales

De manière générale, les variables globales sont considérées comme néfastes à la
réutilisabilité du code; retouchez votre code pour minimiser le nombre de
variables globales.

+++

### Ligne de commande

On aimerait pouvoir passer sur la ligne de commande les paramètres du jeu; par
exemple, le nombre de cases du tableau en hauteur et largeur, la taille d'une
case en pixels, ...

Indice: cherchez le module `argparse` dans la documentation Python.

+++

### Vitesse de réaction

Ralentissez le jeu à 4 images/secondes; êtes-vous satisfait de la vitesse de
réaction ? dit autrement, est-ce qu'il arrive que le serpent tourne trop tard ?
si oui modifiez votre code pour une bonne synchronisation

De la même façon, si vous revenez artificiellement à une image par seconde ou
moins, et que vous quittez le jeu avec 'q', est-ce que ça fonctionne
immédiatement ? si non, comment améliorer le code pour que ce soit plus réactif ?

Toujours à cette vitesse lente, que constatez-vous au tout début du jeu ? est-ce
que c'est grave ? si on voulait vraiment le corriger (pas forcément utile en
pratique hein), comment on pourrait faire ?

+++

### Asynchronisme

À ce stade nous avons un jeu à une seule vitesse; la boucle principale est
entièrement cadencée par le `clock.tick(n)`, et la vitesse du serpent est
entièrement fixée par ce moyen-là.

Mais en fait on triche complètement; que se passerait-il si on avait par exemple
deux objets à animer à des vitesses différentes ?

Modifiez votre code pour pouvoir paramétrer deux fréquences séparément :

* la fréquence de rafraichissement de l'écran (en frame / seconde)
* la fréquence de déplacement du serpent (en case / seconde)

+++

## Notes à propos des environnements virtuels

Voici un très rapide résumé des commandes pour gérer ses environnements virtuels

* pour voir la liste

  ```bash
  conda env list
  ```

* pour entrer dans un environnement

  ```bash
  conda activate snake
  ```

* pour sortir de l'environnement

  ```bash
  conda deactivate
  ```

* pour voir dans quel environnement on se trouve (normalement vous avez ça aussi dans le *prompt*)

  ```bash
  echo $CONDA_DEFAULT_ENV
  ```

* pour créer un nouvel environnement

  ```bash
  conda create -n un-nouveau python=3.12
  ```

  (le fait de spécifier la version de Python est optionnel, mais recommandé)

* pour détruire un environnement

  ```bash
  conda env remove -n un-nouveau
  ```

  **remarquez** comment il n'y a pas de `env` pour `create`, mais il en faut un pour `remove` ...


## Note à propos des dépôts git imbriqués

Si vous avez reçu ce TP depuis un dépôt git (celui de votre cours d'info), ce
qu'on vous invite à faire c'est finalement de créer un dépôt git ... à
l'intérieur d'un autre dépôt git.

Sachez que ça marche sans aucun souci (et en pratique on finit par avoir ce
genre de tricotage avec une profondeur non triviale, 3 voire même parfois 4 dépôts les
uns dans les autres)

La seule chose à savoir c'est que, lorsque vous tapez une commande `git`, pour
trouver le "bon" dépôt, on utilise assez naturellement l'algo suivant:

> on regarde si le dossier courant est un dépôt git, si oui on a trouvé, sinon on
  regarde dans le dossier parent, et ainsi de suite

Donc c'est assez simple, mais faites juste **attention à ne pas ajouter vos fichiers dans le mauvais dépôt**

Dernière astuce pour les *geeks*: si vous voulez savoir où se trouve la racine
de votre dépôt courant:

```bash
git config --global alias.root "rev-parse --show-toplevel"
```

après quoi vous pourrez taper n'importe où `git root` pour voir s'afficher le
(chemin complet du) dossier racine de votre dépôt.
