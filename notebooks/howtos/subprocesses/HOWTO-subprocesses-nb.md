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
nbhosting:
  title: lancer un sous-process
---

# gestion de sous-processus

un aperçu ultra-rapide de: comment faire pour lancer un autre processus depuis Python

+++

## le module `subprocess`

il se trouve dans la librairie standard et permet de faire un peu tout ce qu'on veut (lire: très simple ou très compliqué)

````{admonition} ne plus utiliser le module os
il existe une fonction un peu similaire, mais très limitée, qui s'appelle `os.system()`  
je vous la déconseille car elle est beaucoup plus limitée 

````

```{code-cell} ipython3
# dans la librairie standard

import subprocess
```

## le plus simple

quand on veut juste lancer la commande, et savoir si elle s'est bien passé ou pas

+++

### `ls -l`

sur Unix on dispose d'une commande `ls` pour voir la liste des fichiers; ce n'est en général pas disponible sur Windows (sauf par exemple si vous avez installé un `bash`), dans ce cas remplacez par ce que vous voulez d'autre

ici on va faire comme si on avait tapé dans le terminal:

```bash
l'option -l c'est pour avoir des détails sur les fichiers
ls -l
```

```{code-cell} ipython3
completed = subprocess.run(['ls', '-l'])
```

on peut accéder au **code de retour** du programme qu'on vient de lancer:

- 0: tout s'est bien passé
- autre chose: une erreur (le code dépend alors du programme...)

```{code-cell} ipython3
# ici tout se passe bien

completed.returncode
```

````{admonition} différence avec le !
:class: dropdown

depuis le notebook on peut aussi invoquer un programme exterieur par une *magic* de IPython:  
essayez de mettre dans une cellule de code

```ipython
! ls -l
```

cette forme - qui ne marche que avec IPython ou les notebooks - est plus accessible, mais ne sert pas le même propos...

````

+++

## capture de stdout/stderr

pareil, mais cette fois-ci on veut aussi lire la sortie

````{admonition} voir aussi `glob`
on prend la commande comme exemple car c'est la plus élémentaire à laquelle on peut penser  
en lançant `ls` et en relisant sa sortie standard, on va obtenir .. la liste des fichiers dans le dossier courant  
on insiste bien pour dire que **ce n'est pas** comme ça qu'il faudrait s'y prendre si c'était notre objectif !  
il vaudrait mieux dans ce cas utiliser `pathlib` et `glob`, évidemment (ce serait beaucoup plus efficace)
````

```{code-cell} ipython3
# ls sans option renvoie juste la liste des fichiers
completed = subprocess.run(['ls'], stdout=subprocess.PIPE)
completed.returncode
```

```{code-cell} ipython3
# cette fois on a capturé la sortie standard
# sauf que ce sont des bytes...

type(completed.stdout)
```

```{code-cell} ipython3
# ... qu'il faut decoder comme du texte 

output = completed.stdout.decode()
print(output)
```

## rediriger la sortie

on peut aussi avoir besoin de rediriger la sortie directement dans un fichier, dans ce cas pas besoin de s'embarrasser de passer par un *pipe*, on peut le faire directement comme ceci:

```{code-cell} ipython3
with open('subprocess.stdout', 'w') as writer:
    completed = subprocess.run(command, stdout=writer)
```

```{code-cell} ipython3
# uniquement pour vérifier que ça a bien fait ce qu'on veut

with open("subprocess.stdout") as reader:
    for line in reader:
        print(line, end="")
```

## quelques astuces pratiques

+++

### shell=True

avec ce flag on indique à subprocess qu'on va lui passer une ligne de commande - par opposition à une liste: commande + arguments; dans ce cas il y a une première passe qui est effectuée sur la commande pour la découper en liste - en fait comme si la commande était tapée directement dans le terminal

```{code-cell} ipython3
# on peut passer la commande en une seule ligne
command_oneline = "ls -l"

completed = subprocess.run(
    command_oneline, stdout=subprocess.PIPE, shell=True)
print(f"{completed.returncode=}, {completed.stdout.decode()=}")
```

### text=True

si on sait que la sortie est du texte; comme ça on n'a pas besoin de decoder

```{code-cell} ipython3
completed = subprocess.run(
    command, stdout=subprocess.PIPE, text=True)
print(f"{completed.returncode=}, {completed.stdout=}")
```

## pour aller plus loin

dans le module `subprocess` - comme c'est souvent le cas - on nous expose aussi une API de plus bas niveau  
par exemple si maintenant on veut pouvoir contrôler plus finement le déroulement,
notamment lire les sorties en même temps que fournir les entrées,
et cela de manière intelligente, il faut avoir recours à `Popen.communicate()` https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate

+++

***
