---
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
  notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version, -jupytext.text_representation.format_version,
    -language_info.version, -language_info.codemirror_mode.version, -language_info.codemirror_mode,
    -language_info.file_extension, -language_info.mimetype, -toc
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
  title: "g\xE9n\xE9ration al\xE9atoire de dates"
---

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat &amp; Arnaud Legout</span>
</div>

+++

# random dates

+++

````{admonition} **Survol**

Dans ce TP, nous allons:

* écrire une fonction permettant de générer une date au hasard dans un intervalle
* produire un fichier contenant *n* échantillons 
* relire et trier le fichier

Dans le but de 

* pratiquer l'écriture et la lecture de fichiers
* manipuler des dates

````

+++

## étape 1: générer une date

+++ {"slideshow": {"slide_type": "slide"}}

````{admonition} to do
Écrivez une fonction qui se comporte comme `generate_random_date`

(lisez bien les indices avant de vous lancer)
````

```{code-cell} ipython3
from randomdate import generate_random_date

help(generate_random_date)
```

```{code-cell} ipython3
# that can be called like this
generate_random_date()
```

```{code-cell} ipython3
# or like this
generate_random_date("10/02/2020", "31/12/2021")
```

+++ {"tags": []}

### indices

+++

#### ne même pas essayer 

bien sûr, si vous essayez de générer les trois morceaux indépendamment

* vous n'avez aucune chance d'être uniforme
* en plus ça ne marche plus du tout si les bornes tombent comme ici au milieu de l'année et du mois

+++

#### le module `random`

```{code-cell} ipython3
# pour générer un entier dans un intervalle
# lisez la doc pour savoir si les bornes sont incluses ou pas

import random
random.randint(1000, 2000)
```

#### le module `datetime`

+++

pour représenter :

* les instants au cours du temps (dates, heures, ...): la classe `datetime`  
  que, juste pour être compatibles avec la PEP008, on va importer sous le nom de `DateTime`
* les durées - i.e. la différence entre deux instants: la classe `timedelta`  
  et idem ici on va l'appeler `TimeDelta``

voici quelques-uns des traits qu'on va utiliser

```{code-cell} ipython3
from datetime import datetime as DateTime, timedelta as TimeDelta
```

```{code-cell} ipython3
# to build a DateTime that describes a specific day
# one can do (among other methods)

day = DateTime.strptime("15/02/2017", "%d/%m/%Y")
day
```

ici le deuxième paramètre représente le **`format`** utilisé pour afficher les dates, voir la liste complète ici
<https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior>

```{code-cell} ipython3
# the interesting thing is that these objects
# know ho to do basic arithmetic

# le surlendemain de ce jour ce sera
day_after = day + TimeDelta(days=2)
day_after
```

```{code-cell} ipython3
# then to convert a DateTime object back to a string
# one can do (again there are other ways...)

f"{day_after:%d %m %Y}"
```

```{code-cell} ipython3
# ofor example, this works too

DateTime.strftime(day_after, "%Y/%m/%d")
```

## solution


````{admonition} ouvrez-moi
:class: dropdown
```{literalinclude} randomdate.py
:start-after: prune-start-step1
:end-before: prune-start-step2
```
````

+++

*****

+++

## étape 2: écrire *n* échantillons dans un fichier

mêmes modalités, récrivez la fonction suivante

```{code-cell} ipython3
from randomdate import write_random_data

help(write_random_data)
```

```{code-cell} ipython3
with open("randomdate.txt", 'w') as output:
    write_random_data(output, 5)
```

```{code-cell} ipython3
# this is just to see what is in the generated file
# if on Windows, it will likely not work, use vs-code instead..

%cat randomdate.txt
```

### indices

* le type `TextIO` représente un **fichier déjà ouvert** (et non pas un nom de fichier)
* regardez la valeur de `string.ascii_lowercase`
* regardez les fonctions `random.choice()` et `random.choices()`

+++

## solution


````{admonition} ouvrez-moi
:class: dropdown
```{literalinclude} randomdate.py
:start-after: prune-start-step2
:end-before: prune-start-step3
```
````

+++

## étape 3: relire le fichier et le trier

+++

mêmes modalités, récrivez la fonction suivante

```{code-cell} ipython3
from randomdate import sort_data
```

```{code-cell} ipython3
help(sort_data)
```

```{code-cell} ipython3
sort_data("randomdate.txt", "randomdate-sorted.txt")
```

```{code-cell} ipython3
!cat randomdate-sorted.txt
```

### indices

* on a le choix entre
  * la **fonction** `sorted()` qui fabrique une copie triée
  * le **méthode** `list.sort()` qui copie une liste en place

  du coup si on essaye d'optimiser l'utilisation de la mémoire, on va choisir laquelle ?
* ces fonctions pour trier acceptent un paramètre `key=`, regardez bien comment ça marche ce truc-là
* pas la peine d'essayer de finasser et de lire le fichier ligne par ligne, on n'a pas d'autre choix que de lire l'entrée en entier avant de trier

+++

## solution


````{admonition} ouvrez-moi
:class: dropdown
```{literalinclude} randomdate.py
:start-after: prune-start-step3
```
````

+++

## variantes

indépendantes les unes des autres:

* si vous vous sentez confortable avec les classes, vous pouvez écrire une classe `Sample` pour chaque élément dans le fichier

* écrivez un `if __name__ == '__main__'` pour rendre votre script exécutable
  et utilisez `ArgumentParser` pour paramétrer le nombre de lignes générées

+++

****
