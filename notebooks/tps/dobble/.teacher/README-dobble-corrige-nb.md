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

+++ {"tags": ["prune-cell"]}

````{admonition} nothing to prune
:class: warning

there are no difference - apart from this very cell - between the teacher and the student version, but the notebook is duplicated in .teacher for consistency
````

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
:tags: [level_basic]

# prune-begin
```

```{code-cell} ipython3
:tags: [level_basic]

SHOW_FREQUENCIES = False

# un symbole est représenté par une chaine
# et un compte d'occurrences
class Symbol:
    """
    chacun des symboles dessinés sur les cartes
    """
    def __init__(self, string):
        self.string = string
        self.frequency = 0
        self.cards = set()
        # for drawing
        self.X = -1

    def __repr__(self):
        text = f"{self.string}"
        if SHOW_FREQUENCIES and self.frequency != 0:
            text += f" ({self.frequency})"
        return text
    def __format__(self, spec):
        return format(self.__repr__(), spec)

    def __lt__(self, other):
        return (self.frequency, self.string) < (other.frequency, other.string)
    
    def seen_on_card(self, card):
        self.cards.add(card)
        self.frequency += 1
```

```{code-cell} ipython3
:tags: [level_basic]

# une carte est un ensemble de symboles
class Card(set):
    """
    le modèle pour chaque carte du jeu
    """
    
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        # for drawing
        self.Y = -1
        
    def _contents(self):
        return " ".join(sorted(s.string for s in self))
    def __repr__(self):
        return set.__repr__(self) 
    def __hash__(self):
        return hash(self._contents)
    def __eq__(self, other):
        return self._contents() == other._contents()
```

```{code-cell} ipython3
:tags: [level_basic]

from itertools import combinations

class Deck:
    
    def __init__(self, filename):
        symbols_dict = {}
        cards = []
        symbols_per_card = None
        with Path(filename).open() as f:
            for line in f:
                # convenience: allow for comments
                if '#' in line:
                    continue
                # the symbols (strings) in that line
                line_symbols = []
                for x in line.split():
                    if x not in symbols_dict:
                        symbol = symbols_dict[x] = Symbol(x)
                    else:
                        symbol = symbols_dict[x]
                    # convenience: spot duplicate if any
                    if symbol in line_symbols:
                        print(f"ignoring duplicate {symbol}")
                    else:
                        line_symbols.append(symbol)
                # initialize N from the first line
                if symbols_per_card is None:
                    symbols_per_card = len(line_symbols)
                card = Card(line_symbols)
                # ignore cards with wrong number of symbols
                if len(card) != symbols_per_card:
                    print(f"ignoring inconsistent card with "
                          f"{len(card)} != {symbols_per_card} items {card}")
                    continue
                cards.append(card)
                # update symbols
                for symbol in line_symbols:
                    symbol.seen_on_card(card)

        symbols = list(symbols_dict.values())
        self.symbols_per_card = symbols_per_card
        self.cards = cards
        self.symbols = symbols
        self.filename = filename
    
    
    def check_unique(self):
        def compare(c1, c2):
            common = len(c1&c2)
            if common != 1:
                print(f"OOPS, {c1} and {c2} have {common} symbols in common")
            return common == 1
        return all(compare(c1, c2) for c1, c2 in combinations(self.cards, r=2))    
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-end
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

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# of course it's simpler to just edit the classes above
# but for the sake of incrementality...

def number_cards(deck):
    return len(deck.cards)
Deck.number_cards = number_cards

def number_symbols(deck):
    return len(deck.symbols)
Deck.number_symbols = number_symbols
```

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

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# n + (n-1)**2 = n**2 -n +1

def conjecture(deck):
    result = True
    n = deck.symbols_per_card
    expected = (n**2 - n + 1)
    if deck.number_cards() != expected:
        print(f"unexpected number of cards {deck.number_cards()} vs {expected}")
        result = False
    if deck.number_symbols() != expected:
        print(f"unexpected number of symbols {deck.number_symbols()} vs {expected}")
        result = False
    return result

DECKS = D2, D3, D4, D5, D6 = (Deck(f"data/cards{i:02}.txt") for i in (2, 3, 4, 5, 6))

print(all(conjecture(deck) for deck in DECKS))
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

```{code-cell} ipython3
:tags: [level_basic]

# prune-begin
```

```{code-cell} ipython3
:tags: [level_basic]

conjecture(G8)
```

```{code-cell} ipython3
:tags: [level_basic]

conjecture(G10)
```

+++ {"tags": ["level_basic"]}

s'il y a effectivement dualité, la propriété de départ:

> entre deux cartes il y a exactement un symbole

se traduit dans le dual en

> un couple de symboles se trouve sur exactement une carte

(dans tous les cas, il ne peut pas être sur deux cartes)

```{code-cell} ipython3
:tags: [level_basic]

# on cherche les couples de symboles qui n'apparaissent pas du tout
def missing_symbol_pairs(deck):
    for (s1, s2) in combinations(deck.symbols, r=2):
        c1s = {card for card in deck.cards if s1 in card}
        c2s = {card for card in deck.cards if s2 in card}
        if len(c1s&c2s) != 1:
            print(f"({s1}, {s2}) is missing")
Deck.missing_symbol_pairs = missing_symbol_pairs
```

+++ {"tags": ["level_basic"]}

### game 08 has 2 missing cards

```{code-cell} ipython3
:tags: [level_basic]

Deck("data/game08.txt").missing_symbol_pairs()
```

```{code-cell} ipython3
:tags: [level_basic]

# which allows us to fill the game with 2 new cards
G8_complete = Deck("data/game08-complete.txt")
G8_complete.missing_symbol_pairs()
conjecture(G8_complete)
```

+++ {"tags": ["level_basic"]}

### game 10 has 3 missing cards

```{code-cell} ipython3
:tags: [level_basic]

Deck("data/game10.txt").missing_symbol_pairs()
```

```{code-cell} ipython3
:tags: [level_basic]

# which allows us to fill the game with 3 new cards
G10_complete = Deck("data/game10-complete.txt")
G10_complete.missing_symbol_pairs()
conjecture(G10_complete)
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-end
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
:tags: [level_basic]

# prune-begin
```

```{code-cell} ipython3
:tags: [level_basic]

# would need to be extended if n > 6

def is_in(n, card):
    for s in card:
        if s.string == str(n):
            return True
        
COLORS = ['blue', 'green', 'pink', 'lightblue', 'red', 'orange']

def color(deck, x, y, debug=False):
    """
    computes the color to use for symbol x and card y
    """
    N = deck.symbols_per_card
    # coordinates of the square
    qx = (x-1)//(N-1)
    qy = (y-1)//(N-1)
    # coordinates in that square
    rx, ry = (x-1)%(N-1), (y-1)%(N-1)
    # the first line or column: return blue
    if (qx <= 0) or (qy <= 0):
        return COLORS[0]
    # otherwise, the second line or column: return green
    elif (qx == 1) or (qy == 1):
        return COLORS[1]
    # the rest of the grid
    # in the square, pick the first line
    # in which there is exactly one box ticked
    # the index of that box (in the square) is [1 .. N-1[
    # (because 0 would be the diagonal and it is not there)
    # this index is used in COLORS, with 1=pink and counting
    else:
        debug and print(f"{x=} {rx=}")
        first_line = x - rx
        card = deck.cards[first_line]
        # what is the offset on that line
        first_column = y - ry + 1
        debug and print(f"{first_column=}, {first_line=}", card)
        for i in range(N-1):
            debug and print("trying", first_column + i)
            if is_in(first_column + i, card):
                debug and print(f"bingo {i=}")
                return COLORS[2+(i-1)]
        return 'black'
```

```{code-cell} ipython3
:tags: [level_basic]

# here again we are just adding methods in the Deck class

def expected(self):
    return self.symbols_per_card**2 - self.symbols_per_card + 1
Deck.expected = expected

def number_items(self):
    """
    set the X attribute on symbols and the Y attribute on cards
    from the order in the file
    """
    for index, symbol in enumerate(self.symbols):
        symbol.X = index
    for index, card in enumerate(self.cards):
        card.Y = index
Deck.number_items = number_items

def draw_map(self, figsize=(8, 8)):
    
    self.number_items()
    
    # from north to south, not the other way around
    def x(n):
        return n
    def xs(L):
        return [x(_) for _ in L]
    def y(n):
        return self.expected()-n
    def ys(L):
        return [y(_) for _ in L]

    N = self.symbols_per_card
    y_labels = [str(s) for s in self.symbols]

    X, Y, colors = [], [], []
    for card in self.cards:
        for symbol in card:
            X.append(x(symbol.X))
            Y.append(y(card.Y))
            colors.append(color(self, card.Y, symbol.X))

    fig, ax = plt.subplots(figsize=figsize)
    plt.title(f"N={self.symbols_per_card} "
              f"X={len(self.cards)} cards, "
              f"Y={len(self.symbols)} symbols")
    if y_labels:
        ax.set_yticklabels(y_labels)
        ax.set_yticks(ys(range(self.expected())))
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.tick_params(axis='both', which='minor', labelsize=6)

    # the dots
    plt.scatter(X, Y, marker='o', c=colors)
    # la grille
    for i in range(1, N):
        # the separation lines
        step = 1+i*(N-1)-0.5
        plt.plot(xs([-0.5, self.expected()-0.5]),
                 ys([step, step]),
                 'k-', linewidth=0.5)
        plt.plot(xs([step, step]),
                 ys([-0.5, self.expected()-0.5]),
                 'k-', linewidth=0.5)
    # save as svg, but in the media/ folder
    output = path(self.filename.replace("data/", "media/")).with_suffix('.svg'))
    plt.savefig(output)
    
Deck.draw_map = draw_map    
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-end
```

```{code-cell} ipython3
# une fois que c'est fait vous pouvez appeler

# Deck("data/cards04.txt").draw_map()
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

Deck("data/cards04.txt").draw_map()
```

```{code-cell} ipython3
# ou encore

# Deck("data/cards06.txt").draw_map()
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

Deck("data/cards06.txt").draw_map()
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

```{code-cell} ipython3
:tags: [level_basic]

# prune-begin

# à terminer un jour...
```

+++ {"tags": ["level_basic"]}

## produire automatiquement un jeu

+++ {"tags": ["level_basic"]}

TODO

écrire un code qui produise automatiquement un jeu pour N=7, soit de 43 cartes

+++ {"tags": ["level_basic"]}

## retrouver l'ordre

+++ {"tags": ["level_basic"]}

TODO

est-ce que c'est faisable de prendre un jeu dans le désordre (genre les deux `game*.txt`) et de réordonner les cartes et symboles pour que le dessin ressemble à ce qu'on vient de voir pour N=5 ou N=6

```{code-cell} ipython3
:tags: [level_basic]

# prune-end
```
