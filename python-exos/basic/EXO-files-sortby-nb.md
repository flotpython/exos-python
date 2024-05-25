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
  title: trier tous les fichiers dans un dossier
---

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat</span>
</div>

+++

# parcours de dossier

en 2024 tous les calculs/parcours sur le contenu du disque, dossiers, fichiers, et métadonnées telles que tailles, dates, etc... se font avec le couteau suisse `pathlib`

**lisez-bien tout le notebook, et surtout les indices, avant de commencer**

```{code-cell} ipython3
from pathlib import Path
```

(et non plus avec `os.path` et autres `glob` comme on aurait pu le faire dans le passé)

+++

## initialisation

on va partir d'un dossier avec un peu de contenu; c'est pour simuler par exemple un dossier avec des logs

```{code-cell} ipython3
# on nettoie bien tout pour être sûr
!rm -rf pathlib-foo
```

```{code-cell} ipython3
from files_sortby import init
init()
```

````{admonition} pour faire la même chose sur votre ordi:
:class: dropdown

```{literalinclude} files_sortby.py
:end-before: prune-end-init
```
````

+++

## pb1: parcours de dossier

on veut parcourir tout un dossier, c'est-à-dire calculer la liste des fichiers qui se trouvent dans un dossier;
et cela récursivement ou pas (en parcourant ou non les sous-dossiers)

on vous demande d'écrire une fonction `scan_dir` qui prend en paramètres:

- `root` (le nom d')un dossier racine
- `relative`: un chemin relatif (en dessous de cette racine; peut être vide ou '.') 
- un booléen `recursive`

et qui renvoie une liste d'objets de type `Path`, qui correspondent aux fichiers (pas les dossiers) qui se situent en dessous de `root`/`relative`


````{admonition} paramètres keyword-only

dans la correction, nous allons utiliser un trait qui s'appelle les paramètres *keyword-only*  
car autant le premier paramètre a un rôle parfaitement clair, autant les deux autres sont relativement accessoires; aussi pour être sûr de ne pas se tromper, on va **imposer à l'appelant de les nommer**  
cela signifie qu'on ne pourra pas appeler

  ```python
  # ceci ne sera pas légal
  scan_dir("/Users/Jean Mineur", "git", True)

  # il faudra toujours nommer comme ceci
  scan_dir("/Users/Jean Mineur", relative="git", recursive=True)
  ```
````

````{admonition} générateur ?
:class: admonition-small seealso

pour les avancés, plutôt que de renvoyer une liste vous pouvez sans souci écrire un générateur
````

+++

### exemples

```{code-cell} ipython3
from files_sortby import scan_dir

for p in scan_dir("pathlib-foo/", relative="logs/dir1", recursive=False):
    print(p)
```

```{code-cell} ipython3
for p in scan_dir("pathlib-foo/", relative="logs", recursive=True):
    print(p)
```

## pb2: idem mais en triant

on veut maintenant pouvoir trier cette information  

on veut écrire une fonction `sort_dir` qui prend les **mêmes paramètres**, et **en plus**
- un paramètre `by` (une chaine) qui vaut
  1. `name` pour trier selon le nom du fichier
  1. `namelen` pour trier par la longueur du nom du fichier
  1. `size` pour trier selon la taille du fichier
  1. `mtime` pour trier selon la date de modification du fichier

+++

### exemples

```{code-cell} ipython3
from files_sortby import sort_dir

sort_dir("pathlib-foo", relative="logs", recursive=True, by='size')
```

```{code-cell} ipython3
from files_sortby import sort_dir

sort_dir("pathlib-foo", relative="logs", recursive=True, by='namelen')
```

## Indices

```{code-cell} ipython3
# on utilise ici quelques traits de `pathlib.Path`

from pathlib import Path

# pour construire un Path
root = Path("pathlib-foo")
root
```

```{code-cell} ipython3
# on peut utiliser l'opérateur `/` pour construire des chemins
# mais ça ne marche pas (évidemment) entre deux chaines
# par contre dès qu'un des deux opérandes est un Path:

path = root / "logs/dir100/filecxx"
path
```

```{code-cell} ipython3
# ou encore, donne le même résultat

path = root / "logs" / "dir100" / "filecxx"
```

```{code-cell} ipython3
# pour avoir la taille
path.stat().st_size
```

```{code-cell} ipython3
# pour chercher les fichiers on peut utiliser la méthode glob
# 2 remarques:
# - ici j'appelle list(), c'est juste pour avoir un affichage correct (essayez de l'enlever...)

logs = root / "logs"

list(logs.glob("*"))
```

```{code-cell} ipython3
# et pour les recherches récursives on fait comme ceci
# le **/ va matcher tous les dossiers en dessous de 'logs'

list(logs.glob("**"))
```

```{code-cell} ipython3
# du coup pour trouver tous les fichiers on fait

list(logs.glob("**/*"))
```

```{code-cell} ipython3
# pas utilisé dans cet exercice, mais on peut facilement
# faire des calculs du genre de:

path = root / "logs" / "dir100" / "filecxx"

path.parts
```

```{code-cell} ipython3
# ou encore 

list(path.parents)
```

```{code-cell} ipython3
# ou encore

path.absolute()
```

```{code-cell} ipython3
path.relative_to(root)
```

```{code-cell} ipython3
# etc etc..
```

## solution

````{admonition} ouvrez-moi
:class: dropdown
```{literalinclude} files_sortby.py
:start-after: prune-end-init
```
````

+++

## variantes possibles

- passer en paramètre les extensions de fichier qui sont intéressantes; par exemple on pourrait accepter pour ce paramètre
  - `None`: le défaut, comme on vient de faire
  - une chaine unique, e.g. `"py"` pour ne regarder que les `*.py`
  - une liste d'extensions
- afficher la première ligne de chaque fichier - pour cela il est sans doute idoine de se définir une nouvelle fonction
- en faire un script qui puisse se lancer depuis le terminal
- etc...
