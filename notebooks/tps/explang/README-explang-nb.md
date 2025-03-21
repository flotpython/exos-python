---
jupytext:
  encoding: '# -*- coding: utf-8 -*-'
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
  title: 'TP: langage d''expressions'
---

# un petit langage d'expressions

+++

Licence CC BY-NC-ND, Thierry Parmentelat

+++

```{admonition} commencez par télécharger le zip
{download}`vous aurez besoin du zip qui se trouve ici<./ARTEFACTS-explang.zip>`
```

+++

## rappel

On rappelle qu'en programmation, on distingue entre :

* les expressions, qui sont des fragments de programme qui **s'évaluent** et qui retournent un résultat,
* et les instructions, qui **s'exécutent**, ayant pour résultat de changer l'état du programme, sans pour autant retourner une valeur.

+++

## état de l'art

Traditionnellement (l'implémentation d')un langage est vu comme une suite d'opérations :

* analyse lexicale et syntaxique :  
  on manipule le code sous forme de texte, pour le transformer en une structure de données qui soit plus adaptée à toute la série de calculs qu'on doit faire dans les parties suivantes, puis
* l'interprétation / compilation propremement dite.

+++

On se propose d'implémenter un petit langage d'expressions; 
en fait, seulement la seconde moitié, c'est-à-dire qu'on veut :

* concevoir et implémenter cette structure de données intermédiaire qui représente le programme,
* et partant de là on pourra effectivement évaluer les expressions.

+++

## AST (abstract syntax trees)

Une façon de représenter un programme consiste à définir ce qu'on appelle une syntaxe abstraite, c'est à dire un ensemble de symboles qui permettent d'étiqueter les noeuds d'un arbre, lui même représentant fidèlement le programme.

Quelques exemples :

+++

### v1 : nombres et 4 opérations

Pour les expressions simples faisant intervenir les 4 opérations, on peut s'en sortir avec disons 7 symboles : *Plus*, *Minus*, *Multiply* et *Divide*, pour les 4 opérations, *Integer* et *Float* pour modéliser les opérandes qui apparaissent en clair dans le code, et *Negative* pour l'opération unaire qui calcule l'opposé.

Dans ce monde-là, on représentera par exemple
  
* le fragment `(30 + 40 + 50) * (20 - 15)`  
  par l'arbre 
  
  ```
  Multiply(
      Plus(Integer(30), Integer(40), Integer(50)),
      Minus(Integer(20), Integer(15)))
  ```
                     
* et le fragment `(4 + 1.) / -(4. + 12)`  
  par l'arbre 
  
  ```
  Divide(
      Plus(Integer(4), Float(1)),
      Negative(
          Plus(Float(4.), Integer(12))))
  ```

+++

###  v2 : variables et affectations
    
Si on souhaite sophistiquer un peu davantage, on peut introduire l'affectation comme une expression  
(ce qui rappelons-le n'est pas le cas en Python, ou plutôt c'est seulement le cas avec le *walrus* operator `:=`)  

Nous nous écartons donc ici légèrement de la sémantique de Python, en décidant que dans notre langage une affectation est une expression, comme c'est le cas dans de nombreux langages réels (C, C++, Javascript,…)
  
Dans ce monde-ci, on ajoute 3 opérateurs : *Expressions*, *Assign* et *Variable*  
et munis de ce vocabulaire on peut maintenant représenter
  
* le fragment  
  ```
  a := 20
  a + 1
  ```  
* par l'arbre  
  ```
  Expressions(
      Assign(Variable(a), Int(20)),
      Plus(Variable(a), Int(1)))
  ```

+++

## objectif

À nouveau, dans cet exercice on ne souhaite pas adresser l'analyse syntaxique, mais on vous demande

* d'implémenter les classes correspondant aux opérateurs de la syntaxe abstraite,
* qui permettent à la fois de construire l'AST,
* et de l'évaluer.

Cela signifie qu'on doit pouvoir écrire par exemple :

```python
# construire un arbre comme ceci
expression = Multiply(
                Plus(Integer(30), Integer(40), Integer(50)),
                Minus(Integer(20), Integer(15)))
# puis l'évaluer
expression.eval()
-> 600
```

+++

Parmi ce qui est attendu:
* on s'efforcera de **factoriser au maximum le code**, et d'éviter dans toute la mesure du possible les répétitions fastidieuses  
  c'est tout l'objectif de cet exercice, on veut produire un code maintenable (pas de répétition),
  et dans lequel on puisse facilement ajouter des *features* (nouveaux opérateurs notamment).
* on vous demande à la construction des objets de vérifier qu'on **appelle** le **constructeur** avec un **nombre d'arguments correct**,  
  et de lancer une **exception `TypeError` sinon** (comme le fait Python lorsqu'on appelle une fonction avec un mauvais nombre d'arguments)  
  voyez tout à la fin du notebook un tableau récapitulatif des nombres d'arguments

+++

## modalités

+++

Pour vous convaincre que vous avez bien répondu à la question, et vous aider à debugger, nous fournissons quelques cellules de test directement dans le notebook.

Une fois que vous êtes satisfait de votre code, vous pouvez optionnellement:
- mettre votre dans un fichier `explangv1.py`
- et importer son contenu dans le notebook en faisant
  `from explangv1 import (Plus, Multiply, ...)
- de façon à pouvoir le tester automatiquement avec `pytest` en faisant
  ```bash
  pytest test_explangv1.py
  ```

```{admonition} autoreload
cette approche fonctionne très bien mais il est crucial d'avoir **mis en place l'*autoreload*** pour que le notebook recharge votre code lorsque vous le modifiez par l'éditeur
```

+++

*****

```{code-cell} ipython3
# vous écrivez votre code ici

class Integer:
    pass

class Float:
    pass

class Negative:
    pass

class Plus:
    pass

class Minus:
    pass

class Multiply:
    pass

class Divide:
    pass
```

### quelques tests

+++

et ensuite vous évaluez ces cellules pour tester votre code

```{code-cell} ipython3
# should print 10
tree = Integer(10); print(tree.eval())
```

```{code-cell} ipython3
# -10
tree = Negative(Integer(10)); print(tree.eval())
```

```{code-cell} ipython3
# 30
tree = Plus(Integer(10), Integer(20)); print(tree.eval())
```

```{code-cell} ipython3
# 60
tree = Plus(Integer(10), Integer(20), Integer(30)); print(tree.eval())
```

```{code-cell} ipython3
# 24
tree = Multiply(Integer(2), Integer(3), Integer(4)); print(tree.eval())
```

```{code-cell} ipython3
# 0.5
tree = Divide(Integer(10), Integer(20)); print(tree.eval())
```

```{code-cell} ipython3
# 200
tree = Multiply(Integer(10), Integer(20)); print(tree.eval())
```

```{code-cell} ipython3
# 6000
tree = Multiply(Integer(10), Integer(20), Integer(30)); print(tree.eval())
```

```{code-cell} ipython3
tree = Multiply(
    Plus(Multiply(Integer(10), Integer(2)), Integer(30)),
    Multiply(Negative(Integer(4)), Integer(25)))

assert tree.eval() == -5000
```

```{code-cell} ipython3
tree = Plus(Multiply(Integer(10), Integer(2)), 
            Negative(Negative(Integer(30))),
            Minus(Integer(100), Integer(50)))

assert tree.eval() == 100
```

```{code-cell} ipython3
tree = Multiply(
    Plus(Integer(30), Integer(40), Integer(50)),
        Minus(Integer(20), Integer(15)))

assert tree.eval() == 600
```

```{code-cell} ipython3
tree = Negative(
    Plus(Float(10), Negative(Integer(20))))

assert tree.eval() == 10.
```

```{code-cell} ipython3
tree = Divide(Integer(10), Integer(4))
assert tree.eval() == 2.5
```

```{code-cell} ipython3
# ces cellules devraient toutes afficher OK
try:
    Plus()
except TypeError:
    print("OK")
```

```{code-cell} ipython3
try:
    Divide()
except TypeError:
    print("OK")
```

```{code-cell} ipython3
try:
    Negative(Integer(1), Integer(1))
except TypeError:
    print("OK")
```

```{code-cell} ipython3
# ces cellules devraient toutes afficher OK
try:
    Multiply(Integer(1))
except TypeError:
    print("OK")
```

```{code-cell} ipython3
try:
    Plus(Integer(1))
except TypeError:
    print("OK")
```

```{code-cell} ipython3
try:
    Divide(Integer(10), Integer(20), Integer(30))
except TypeError:
    print("OK")
```

```{code-cell} ipython3
try:
    Negative(Integer(10), Integer(20))
except TypeError:
    print("OK")
```

****

+++

## v2

+++

une fois que vous avez fait ce premier noyau, vous pouvez étendre votre langage pour y ajouter l'affectation et les variables; la seule différence de taille par rapport au premier exercice est qu'il va nous falloir propager l'environnement (les valeurs des variables).

pour cela je vous recommande d'envisager une méthode d'évaluation

`expression.eval(env)`  plutôt que `expression.eval()` 

dans laquelle `env` est un dictionnaire qui associe le nom d'une variable avec sa valeur.

+++

pour réaliser cette deuxième partie:
* dupliquez votre code de la v1, et modifiez le a minima pour que `eval` puisse s'appeler avec la bonne signature
* ajoutez les 3 nouvelles classes
  * `Variable`: qui correspond à l'utilisation d'une variable dans une formule
  * `Assignment`: qui fait dans notre langage office à la fois de déclaration et d'affectation d'une variable
  * `Expressions`: qui va nous permettre de grouper plusieurs expressions en une suite logique
  
voyez les quelques exemples ci-dessous pour une illustration

```{code-cell} ipython3
# copiez votre code de la v1 ici, et modifiez-le 
```

```{code-cell} ipython3
# définissez les nouvelles classes ici
class Variable:
    pass

class Assignment:
    pass

class Expressions:
    pass
```

et si tout marche bien vous pouvez exécuter la suite sans erreur:

```{code-cell} ipython3
program1 = Expressions(
    Assignment("a", Integer(10)),
    Assignment("b", Integer(20)),
    Plus(Variable("a"), Variable("b")),
)

assert program1.eval({}) == 30
```

```{code-cell} ipython3
"""
a = 2 + (b := 2) # env = {'a': 4, 'b': 2}
b = a * b        # env = {'a': 4, 'b': 8}
b * b            # env - unchanged
"""
program2 = Expressions(
    Assignment("a", Plus(Integer(2),
                         Assignment("b", Integer(2)))),
    Assignment("b", Multiply(Variable("a"), Variable("b"))),
    Multiply(Variable("b"), Variable("b")),
)

assert program2.eval({}) == 64
```

## annexe

+++

un résumé des opérateurs et de leurs arités respectives

+++ {"cell_style": "split"}

### v1

| Opérateur | arité |
|-----------|-------|
| Integer   | 1     |
| Float     | 1     |
| Negative  | 1     |
| Plus      | n>=2  |
| Minus     | 2     |
| Multiply  | n>=2  |
| Divide    | 2     |

+++ {"cell_style": "split"}

### v2

| Opérateur   | arité |
|-------------|-------|
| Expressions | n>=1  |
| Variable    | 1     |
| Assignment  | 2     |
