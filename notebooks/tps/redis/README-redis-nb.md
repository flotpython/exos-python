---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# un jeu multi-joueur

+++

on se propose de réaliser un petit jeu multi joueur, et pour cela nous aurons besoin de

* [redis](https://redis.io/), un système de base de données *light* et rapide, où les données sont stockées en mémoire; il ne s'agit pas d'un système traditionnel, ici pas de SQL ni de stockage sur le disque
  ```{admonition} **attendez avant de l'installer** !
  :class: warning

  les modalités ne sont pas les mêmes sur tous les OS
  ```

* [pygame](www.pygame.org), pour le graphisme et autres interactions avec le jeu

+++

## architecture

+++

### *process* et isolation

un jeu multi-joueur pose des défis qui vont au-delà de ce qu'on apprend dans un cours de programmation de base  
en effet on apprend pour commencer à programmer dans un monde fini et isolé - l'OS appelle ça un *process* - qui **par définition** ne partage aucune donnée avec les autres programmes qui tournent dans le même ordinateur  
typiquement quand vous écrivez un programme Python et que vous le lancez avec `python mon_code.py`, tout le code tourne **dans un seul process**  
(sauf si vous faites exprès d'en créer d'autres bien entendu)

+++

### comment partager

du coup lorsqu'on veut faire jouer ensemble, disons deux personnes, on aurait en théorie le choix entre

* faire tourner tout le jeu, c'est-à-dire les deux joueurs, dans un seul process; mais ça impose de jouer tous les deux sur le même ordi, pas glop du tout
* du coup ça n'est pas une solution en général, donc c'est beaucoup mieux que **chaque joueur lance son propre process**,  
  qui pourront même du coup tourner sur des ordinateurs différents pourvu qu'on s'y prenne correctement

mais avec cette deuxième approche il faut trouver **un moyen d'échanger des informations**:  
chaque process a le contrôle sur la position de son joueur, mais a besoin d'obtenir les positions des autres joueurs

on va voir comment on peut s'y prendre

+++

### une solution centralisée

+++

l'architecture la plus simple pour établir la communication entre tous les joueurs consiste à créer un **processus serveur**, auquel les joueurs sont connectés, selon un diagramme dit en étoile (terme qui prend tout son sens avec plusieurs joueurs: le serveur est au centre du diagramme) :

+++

```{image} processes.svg
:align: center
```

+++

## prototype

+++

ici se trouve un **prototype** hyper simple; il est multi-joueur mais sur un seul ordinateur (car il manque la possibilité d'indiquer où trouver le serveur central)

pour le mettre en oeuvre :

+++

### requirements

```shell
pip install -r requirements.txt
```

+++

### serveur

il faut pour commencer lancer un serveur redis
(après avoir installé [l'outil redis](https://redis.io/), bien entendu)

```bash
redis-server --protected-mode no
```

bien sûr ce process **ne termine pas** (vous remarquez que le shell ne vous affiche pas le *prompt* avec le `$`)

il faut le laisser tourner pendant tout le temps du jeu; donc ce terminal va
être monopolisé pour ça, créez-en un autre pour lancer les autres morceaux

+++

### un premier jeu

```shell
python game.py pierre
```

pareil ici, ce process ne se terminera que lorque pierre aura fini de jouer;
donc pendant tout ce temps le terminal va être occupé...

### un second

```shell
python game.py paul
```

Pierre voit Paul apparaitre sur son écran, et Paul également;

### etc...

on peut lancer d'autres jeux en même temps, mais bien sûr l'espace libre sur l'écran devient rapidement

+++

### défauts

+++

bien sûr ce prototype a des zillions de défauts :

* les joueurs ne jouent pas vraiment, le jeu choisit des les déplacer de manière aléatoire
* on ne gère pas les conflits, si deux joueurs veulent se rendre au même endroit c'est possible
* tout est fait en une seule boucle à la cadence du rafraichissement; la vitesse de déplacement d'un joueur n'est pas forcément la vitesse de rafraichissement
* il manque un moyen de dire où est le serveur redis; du coup les joueurs doivent forcément être sur le même ordi (et donc + ou - le même écran)...
* etc…

+++

## plusieurs ordinateurs

jusqu'ici on a fait tourner tous les processus dans le même ordinateur

en vraie grandeur bien sûr, on veut faire tourner ça sur plusieurs ordinateurs

```{image} ip-address.svg
:align: center
```

pour que ça puisse fonctionner dans ce type de configuration il faut que Jacques
lance le jeu en lui indiquant sur quel ordinateur se trouve le serveur redis

+++

### trouver son addresse IP

selon les systèmes, lancez dans un terminal la commande suivante
* Windows `ipconfig`
* MacOS `ifconfig`
* LInux `ip address show`

et cherchez une adresse parmi les intervalles réservés aux adresses privées

+++

```{image} private-ranges.png
:align: center
```

+++

### pour lancer le jeu

dans notre configuration, si Pierre est sur l'adresse disons `192.168.200.20`,
il suffit aux autres joueurs qui veulent le rejoindre de lancer par exemple

```
game.py --server 192.168.200.20 Jacques
```

+++

## Notes / précisions multi-OS

### Windows

* pas supporté par le site principal, installer redis avec `conda install redis`
* firewall : compliqué

* autre option: memurai
* dont l'installation se charge de créer un service microsoft

### MacOS

* `brew install redis`

### linux / fedora

* `dnf install redis`
* si firewalld est actif: `sudo firewall-cmd --zone=public --permanent --add-port=6379/tcp`

### pour lancer redis

* lancer `redis-server --protected-mode no`
* lancer `redis-server --bind 0.0.0.0`
* ouvrir le firewall si activé, sinon pas moyen de communiquer entre ordis
