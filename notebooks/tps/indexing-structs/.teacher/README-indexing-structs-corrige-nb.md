---
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
  notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version, -jupytext.text_representation.format_version,
    -jupytext.custom_cell_magics, -language_info.version, -language_info.codemirror_mode.version,
    -language_info.codemirror_mode, -language_info.file_extension, -language_info.mimetype,
    -toc, -vscode
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
  title: un index de structs
---

# le dict: struct ou index

dans ce petit exercice on va utiliser
* le dict pour gérer des enregistrements (en C on dirait des *structs*)
* le dict pour indexer un grand nombre de données pour accélérer les recherches
* et l'ensemble pour détecter les collisions et calculer le nombre d'entrées uniques dans une collection

pour faire cet exercice, {download}`commencez par télécharger le zip<./ARTEFACTS-indexing-structs.zip>`

***disclaimer***: gardez à l'esprit le caractère pédagogique de l'exercice,  
car pour ce genre de choses, dans la vraie vie, on pourrait aussi utiliser une dataframe pandas...

+++

## parsing

on veut pouvoir lire des fichiers texte qui ressemblent à celui-ci (`data-small.txt`)
```{literalinclude} data-small.txt
```

on suppose dans tout ce TP qu'il y a **unicité du (nom x prénom)**  
i.e. on n'est pas confronté au cas où deux personnes ont le même nom et le même prénom


* écrivez une fonction qui lit ce genre de fichiers et qui retourne les données sous la forme d'une liste de dictionnaires;  
* quelles seraient les clés à utiliser pour ces dictionnaires ?
* testez votre fonction sur ce fichier

```{code-cell} ipython3
# prune-cell

# 3 clés 'first_name' 'last_name' 'birthday'
# ce n'est pas une bonne idée de garder 
# les 3 bouts de la date dans des clés différentes
```

```{code-cell} ipython3
# prune-cell

# v1 

def parse_text(filename):
    persons = []
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
            first_name, last_name, day, month, year = line.split()
            person = {
                'first_name': first_name,
                'last_name': last_name,
                'birthday': f"{day} {month} {year}",                
            }
            persons.append(person)
    return persons

parse_text("data-small.txt")
```

```{code-cell} ipython3
# prune-cell

# v2 avec une compréhension de liste
# et extended unpacking 

def parse_text(filename):
    def line_to_person(line):
        first_name, last_name, *date = line.rstrip().split()
        return dict(first_name=first_name, 
                    last_name=last_name,
                    birthday=" ".join(date))
    with open(filename) as f:
        return [line_to_person(line) for line in f]

parse_text("data-small.txt")
```

```{code-cell} ipython3
### prune-cell

# on pourrait bien sûr envisager une v3 
# où les dates sont des instances de datetime.date
# mais ce n'est pas trop notre sujet...
```

## génération de données de test

à partir des deux fichiers joints:

* `last_names.txt`  
  (dérivé de <https://fr.wikipedia.org/wiki/Liste_des_noms_de_famille_les_plus_courants_en_France>)
* `first_names.txt`  
  (dérivé de <https://fr.wikipedia.org/wiki/Liste_des_pr%C3%A9noms_les_plus_donn%C3%A9s_en_France>)

ce qu'il faut faire:

* fabriquez un jeu de données aléatoires contenant 10000 personnes  
  avec la contrainte qu'il y ait en sortie **unicité du nom x prénom**  
* pour les dates de naissance tirez au sort une date entre le 01/01/2000 et le 31/12/2004
* rangez cela dans le fichier `data-big.txt`
* vous devez produire ce fichier dans un temps de l'ordre de 50-100ms

```{code-cell} ipython3
# prune-begin
```

```{code-cell} ipython3
from random import randrange, choice
from datetime import date as Date, timedelta as TimeDelta

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    # compute number of seconds between the 2
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + TimeDelta(seconds=random_second)

BEG = Date(year=2000, month=1, day=1)
END = Date(year=2004, month=12, day=31)

with open("last_names.txt") as last, open("first_names.txt") as first:
    LAST_NAMES = [x for line in last for x in line.strip().split()]
    FIRST_NAMES = [x for line in first for x in line.strip().split()]
    
def random_person():
    # we could return a dict here too
    # or more simply a 5-tuple
    birthday = random_date(BEG, END)
    return (choice(FIRST_NAMES), choice(LAST_NAMES),
            birthday.year, birthday.month, birthday.day)

def generate_data(filename, how_many):
    counter = 0
    seen = set()
    with open(filename, 'w') as w:
        while counter < how_many:
            f, l, y, m, d = random_person()
            if (f, l) in seen:
                continue
            w.write(f"{f} {l} {y} {m} {d}\n")
            counter += 1
```

```{code-cell} ipython3
%%timeit
generate_data("data-big.txt", 10_000)
```

```{code-cell} ipython3
# prune-end
```

## accélération des recherches

* utilisez `%%timeit` pour mesurer le temps moyen qu'il faut pour chercher
  une personne dans la liste à partir de son nom et prénom
* on prévoit ue notre code aura besoin de faire cette recherche plusieurs millions de fois;
  comment pourrait-on faire pour accélérer cette recherche ? 
* écrivez le code qui va bien et mesurez le gain de performance pour la recherche

```{code-cell} ipython3
# prune-begin
```

```{code-cell} ipython3
L = parse_text("data-big.txt")
```

```{code-cell} ipython3
%timeit ('Henri', 'Vincent') in L
```

```{code-cell} ipython3
# v1
index = {}
for p in L:
    index[(p['first_name'], p['last_name'])] = p
```

```{code-cell} ipython3
# v2
index = { (p['first_name'], p['last_name']): p for p in L}
```

```{code-cell} ipython3
%timeit ('Henri', 'Vincent') in index
```

```{code-cell} ipython3
# prune-end
```

## calcul du nombre de prénoms distincts

+++

* calculez le nombre de prénoms distincts présents dans les données

```{code-cell} ipython3
# prune-begin
```

```{code-cell} ipython3
# v1

S = set()
for (f, l) in index:
    S.add(f)
print(len(S))
```

```{code-cell} ipython3
# v2
print(len({f for (f, l) in index}))
```

```{code-cell} ipython3
# prune-end
```

***
