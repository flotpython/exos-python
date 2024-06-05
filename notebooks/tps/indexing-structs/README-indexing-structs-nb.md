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

+++

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

+++

## accélération des recherches

* utilisez `%%timeit` pour mesurer le temps moyen qu'il faut pour chercher
  une personne dans la liste à partir de son nom et prénom
* on prévoit ue notre code aura besoin de faire cette recherche plusieurs millions de fois;
  comment pourrait-on faire pour accélérer cette recherche ? 
* écrivez le code qui va bien et mesurez le gain de performance pour la recherche

+++

## calcul du nombre de prénoms distincts

+++

* calculez le nombre de prénoms distincts présents dans les données

+++

***
