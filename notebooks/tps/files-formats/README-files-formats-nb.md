---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  language_info:
    name: python
    nbconvert_exporter: python
    pygments_lexer: ipython3
---

# fichiers et formats

{download}`Commencez par télécharger le zip<./ARTEFACTS-files-formats.zip>`


## on va faire quoi ?

- les fichiers et l'OS; comment ouvrir, pourquoi fermer ?
- différents formats de fichier usuels
  - texte simple sans accent, typiquement en anglais (ASCII)
  - texte standard (utf-8)
  - pickle (ouille ça pique, c'est du binaire)
  - json (on se sent un peu mieux)
  - csv (ah là on parle)
  - yaml (de plus en plus populaire)
- comment parser un format de fichier *custom*


### modalités du TP

- on ouvre vs-code
- on participe


## les fichiers et l'OS

c'est quoi l'OS ? 

- votre code ne cause **jamais directement** au harware
- mais toujours au travers d'**abstractions exposées par l'OS**
- parmi lesquelles, entre autres, la **notion de "fichier"**

```{image} operating_system_placement.png
:align: right
:width: 250px
```


### questions préliminaires

- qu'est-ce qu'un fichier ?
- que contient un fichier ?
- quelles sont les étapes pour y accéder ?


## lire un fichier simple

(le fichier `hello.txt` fait partie du zip)


### ouverture d'un fichier

```python
f = open("hello.txt")
```

- que se passe-t-il ?
- pensez à consulter la documentation (comment on la trouve ?)
- que peut-on faire de `f` ?
- que pensez-vous de cette version alternative ?
  ```python
  # ça marche aussi; quelle différence ?
  
  f = open("hello.txt", encoding="utf-8")
  ```


### les types

- analyser les types des différents objets
  ```python
  type("hello.txt")
  type(f)
  ```
- avancer étape par étape


### il faut fermer !

que se passe-t-il si on oublie de fermer le fichier ?

> on va écrire un code qui ouvre `n` fichiers
> le faire tourner avec `n`= 10, 100, 1000, ...

pouvez-vous prédire ce qui va passer ?


## l'idiome pour lire un fichier: `with` & `for`

````{admonition} toujours utiliser with
:class: important

l'idiome à **toujours utiliser** pour lire un fichier texte

```python
# TOUJOURS lire ou écrire un fichier avec un with !

with open("hello.txt") as f:
    for line in f:
        print(line, end="")
```

quelles autres formules connaissiez-vous pour faire ça ?
````


````{admonition} pourquoi le end="" ?
:class: admonition-small

à chaque itération, vous allez trouver dans la variable `line`, eh bien la ligne suivante évidemment,  
sauf que ceci **contient un caractère de fin de ligne** - qu'on appelle aussi *newline*  
du coup si vous faites un `print(line)` (essayez..) vous allez avoir une ligne blanche sur deux !

une autre approche consisterait à utiliser `line.rstrip()` qui enlève l'éventuel *newline*;  
je dis éventuel car la dernière ligne ne contient pas toujours ce fameux *newline*; le monde est compliqué parfois...

**exercice**: dans *vs-code*, allez enlever le dernier *newline* (mettez vous à la fin du fichier et faites un *Delete*)  
et refaites tourner les 3 lignes ci-dessus; vous pouvez aussi regarder ce que donne `cat hello.txt` dans le terminal.
````

<!-- #region -->
## contenu des fichiers texte

on va regarder dans les yeux deux fichiers texte:


### ASCII

- installez l'extension vscode *Hex Editor*
- regarder le contenu de `hello.txt` avec vs-code
  - utilisez *clic droit* -> *Open With* -> *Hex Editor*
- comparez avec <https://www.rapidtables.com/code/text/ascii-table.html>


### Unicode

faites pareil avec `bonjour.txt`

- que constatez-vous ?
- voyez aussi <https://www.utf8-chartable.de/>  
<!-- #endregion -->

## un fichier binaire

faites pareil avec `tiny.pickle`

- ouvrez-le "normalement"
  (pour l'instant sans utiliser la librairie `pickle`)
- comment faut-il adapter le code ?
  *indice*: il faut utiliser le **mode d'ouverture** et spécifier **binaire**
- que constatez-vous ? (indice: les types !)

````{admonition} à retenir : texte ou binaire
:class: seealso

un fichier peut contenir 

- du texte (qu'il faut alors décoder, généralement avec `encoding='UTF-8'`), on obtient alors un `str`
- du binaire - on obtient alors des `bytes`; dans ce cas on n'a pas besoin de fournir un encodage pour lire le fichier *of course...* - par contre c'est souvent l'application, ou une librairie, qui va se taper le décodage, plus ou moins *à la main* selon les cas.
````


## les différents formats de fichier

Tout le monde ne crée pas sa propre structure (on dit aussi format) de fichier !  
Il existe des formats ***standard*** qui permettent une interaction entre les programmes, et même différents langages de programmation !


### le format pickle

c'est le format *intégré* de Python:

- c'est un format binaire: s'ouvre avec `open(name, 'rb')`
- permet de sérialiser notamment les types de base, c-a-d non seulement des atomes (nombres, chaines...)
- mais aussi des **structures plus complexes**, avec des containers etc...
- par contre, il ne va pas convenir pour échanger avec d'autres langages...

````{admonition} b pour binaire
:class: note admonition-small

dans `open(name, 'rb')` le `r` est pour *read* et le `b` pour *binary*
````

à faire:

- lisez la documentation du module `pickle`
- essayez de lire le fichier `tiny.pickle`
- inspectez les types des objets dans la donnée


#### pickle : écriture

- partez de ce que vous venez de lire
- modifiez certaines des données
- sauvegardez-les dans un nouveau fichier  
  `tiny-changed.pickle`
- et relisez-le pour vérifier que "ça marche"


### autre format: json

à vous de jouer

- on va refaire pareil à partir de `tiny.json`
- lisez-la doc et écrivez le code qui lit ce fichier
- modifiez la donnée lue, et sauvez-la
- est-ce qu'on peut y mettre un ensemble ? ou un tuple ?


### encore un: yaml

- trouvez la doc de `PyYAML`
- lisez le fichier `tiny.yaml`
- comment peut-on comparer avec JSON ?


### et aussi: les csv

on recommence (c'est optionnel, si vous savez déjà lire un csv avec pandas)...

- lisez la documentation du module `csv`  
  google `python module csv`
- essayez de lire le fichier `pokemon.csv`
- sauriez-vous créer une dataframe ?
  - version facile: avec `pd.read_csv()`
  - un peu moins simple: sans utiliser `pd.read_csv()`


## formats custom

comment peut-on lire (on dit *parse*) des formats de fichiers inconnus ?  
pour cela, 2 armes

* le type `str` fournit plein de méthodes - notamment `strip()`, `split()` et `join()`
* le module `re` (pour *regular expressions*) peut également être utile


### exercice: lisez `notes.txt`

* sans importer de module additionnel,
* lisez le fichier `notes.txt`
* créez et affichez un dictionnaire  
  *nom élève* → note

````{admonition} un mot sur print()

- c'est l'opération la plus simple pour sauver un résultat..  
  mais ce n'est pas très utile en réalité, car le plus souvent limitée à un lecteur humain
- il est souvent plus utile de sauver ses résultats dans un des formats qu'on vient de voir - typiquement json ou csv
- mais pour info, on peut écrire dans un fichier `f` (ouvert en écriture) avec `print(des, trucs, file=f)`
````

````{admonition} les redirections de bash (pour info)
:class: admonition-small

- quand il est lancé, votre programme a un `stdin` et un `stdout` (et un `stderr` mais c'est plus anecdotique)
- qui sont créés par bash (et sont branchés sur le terminal)
-  vous pouvez les rediriger en faisant
  ```bash
  python myhack.py < the-input > the-output
  ```
````


### exercice: écrivez un programme

* qui lit sans fin le texte entré dans le terminal
* regarde si le texte commence par un `q`
* si oui c'est la fin du programme
* sinon affiche le nombre de mots dans la ligne  
  et recommence

````{admonition} consigne

ne pas utiliser `input()`, mais plutôt `sys.stdin`
````

````{admonition} indices
:class: tip

* de quel type est `sys.stdin` ?
* si vous voulez ajouter un *prompt*  
  (un peu comme les `>>>` de python)  
  lancez votre programme avec `python -u mycode.py`
````

<!-- #region -->
## épilogue: les *regexps*, en deux mots

sans transition..

* l'idée est de décrire une *famille* de chaines
* à partir d'une autre chaine (la *regexp*)
* qui utilise des opérateurs
  * comme p.e. `*`
  * pour indiquer 'un nombre quelconque de fois' telle ou telle autre *regexp*


 exemple de *regexp*

`ab((cd)|(ef))*` décrit un ensemble qui

* ne contient que des mots qui commencent par `ab`
* contient `abcd` et aussi `abef`
* ou encore `abcdcdefcd`
* mais pas `abce` ni `abcde`

````{admonition} avertissement

> Some people, when confronted with a problem, think
“I know, I'll use regular expressions.”  Now they have two problems.

<http://regex.info/blog/2006-09-15/247>
````
<!-- #endregion -->
