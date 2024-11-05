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
  title: 'TP: les boids'
---

Licence CC BY-NC-ND, Thierry Parmentelat

+++

# TP - un chatbot avec `flet`

+++

## introduction

dans ce TP nous allons

* découvrir (très superficiellement) la librairie `flet`
* et l'utiliser pour implémenter un début de simulation de *chatbot*

+++

### contenu

vous êtes censé travailler en local sur votre ordi;
commencez par {download}`télécharger le zip<./ARTEFACTS-chatbot.zip>` qui contient

* le starter code dans `chatbot-01.py`
* les illustrations dans un dossier `media/`

+++

### contexte

on met à votre disposition **deux serveurs** `ollama`:

- chacun des deux sait mettre en oeuvre plusieurs modèles d'IA (notamment `mistral`, mais pas que...)
- l'un des deux ne possède qu'un CPU; du coup il est relativement lent mais on peut y accéder sans login/password
- par contre l'autre possède un GPU, il est plus rapide pour notre application, mais le code pour s'en servir est un peu plus compliqué car il faut lui fournir un login/password
- les détails de ces deux serveurs sont dans le *starter code*

- pour les utiliser, essentiellement on `POST` une requête http au serveur avec le chemin
  `/api/generate`
  en lui passant une donnée qui contient
  - `model`: le nom du modèle
  - `prompt`: la question

  les détails se trouvent ici <https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion>

+++

## objectif

ce qu'on veut faire, c'est fabriquer une UI sommaire qui permet de choisir le serveur, le modèle, et de poser ensuite des questions comme avec chatGPT

```{image} media/chatbot-sample.png
:align: center
:width: 500px
```

sur cette implémentation on a également un bouton qui permet d'enabler le *streaming*, l'idée consiste à afficher les résultats "au fur et à mesure" plutôt qu'en une seule fois à la fin de l'échange avec le serveur, on en reparlera...

+++

## v01: starter code

```{literalinclude} chatbot-01.py
```

* installez la librairie
* copiez le code ci-dessus dans un fichier `chatbot.py`
* et lancez-le depuis le terminal avec

```
flet run chatbot.py
```

vous devez voir une UI un peu tristoune, avec seulement

- un checkbox pour choisir le mode *streaming* ou pas
- un dropdown pour choisir entre 3 modèles
- un dropdown pour choisir entre 2 serveurs
- un bouton 'send'

à ce stade, cette UI est totalement inerte, on va la construire pas à pas

+++

### ce qu'on découvre dans la v01

dans ce code, on utilise le fait que

* le module `flet` vient avec son propre modèle de programmation; vous remarquez qu'on ne lance pas le programme comme d'habitude
* en fait c'est pour offrir un mode de développement dit de *hot reload*, c'est-à-dire qu'il suffit de modifier un des fichiers sources, le programme s'en rend compte et recharge tout seul le nouveau code; c'est *extrêmement pratique* à l'usage !
* et ça se concrétise aussi par le point d'entrée dans le programme, qui est `ft.app(main)`

ce qu'on voit également dans ce code:

* les différents morceaux de l'interface sont construits à base d'objets de la librairie; vous en voyez déjà quelques spécimens
  * `ft.Checkbox`, `ft.Dropdown`, `ft.ElevatedButton` pour les objets visibles
  * `ft.Row` pour la logique d'assemblage

vous aurez envie de *bookmark* ces entrées dans la doc, pour plus d'info:

* <https://flet.dev> le point d'entrée principal
* <https://flet.dev/docs/controls> pour les détails des objets disponibles

+++

## pour les forts

si cet énoncé vous inspire, vous pouvez simplement suivre votre voie pour développer l'application

sinon pour les autres, voici un chemin possible pour y arriver; évidemment je vous donne ces étapes **entièrement à titre indicatif**

bref, dans tous les cas, n'hésitez pas à faire comme vous le sentez...

+++

## v02: ajoutons un titre

pour vous familiariser avec le modèle de lignes et colonnes de `flet`, **ajoutez un titre principal**, comme sur l'illustration

- regardez `ft.Column`
- et `flet.Text`
- et à chaque fois les différents attributs disponibles pour contrôler le look et le comportement de l'UI

+++ {"slideshow": {"slide_type": ""}, "tags": []}

## v03: avec un peu de classe

ceci est une étape **totalement optionnelle**, mais je vous recommande de **créer une classe**, qui pourrait s'appeler **`ChatbotApp`**, pour regrouper la logique de notre application, et éviter de mettre tout notre code en vrac dans le `main`

- on pourrait envisager par exemple que `ChatbotApp` hérite de `ft.Column`
- de cette façon on se retrouverait avec un `main` qui ne fait plus que
  ```{literalinclude} chatbot-10.py
  :start-after: def main
  ```
  ````{admonition} page.update()
  :class: tip
  on choisit de passer `page` au constructeur de l'objet, car avec *flet* il faut penser à *flush* les changements avec un `page.update()` - sinon les changements que l'on fait en mémoire ne sont pas répercutés dans l'affichage
  ````

+++

## v04: une classe `History`

toujours pour éviter de finir avec un gros paquet de spaguettis, on pourrait imaginer à ce stade **écrire une classe `History`** (tout ceci est totalement indicatif...) qui:

- hérite, là encore de `ft.Column`
- et est responsable de la partie "dialogue" entre humain et robot
- et qui du coup crée la zone de prompt,
- et possède une méthode `current_prompt()` qui renvoie le prompt tapé par l'utilisateur
- et une méthode `add_message` pour insérer les questions et les réponses au fur et à mesure
  (à ce stade on ne fait pas encore la différence entre prompt et réponse)

pour être bien clair, à ce stade on ne fait pas encore usage du réseau pour quoi que ce soit

+++

## v05: un peu de réseau

c'est seulement maintenant que l'on va effectivement **interagir via le réseau avec les serveurs** ollama  
je vous propose pour commencer de simplement fabriquer la requête, et pour commencer de simplement afficher la réponse sur le terminal  

quelques indices:

- la librairie qu'on va utiliser pour cela s'appelle `requests`;
- vous pouvez commencer par regarder ceci pour quelques exemples <https://requests.readthedocs.io/en/latest/user/quickstart/>
- je vous recommande de vous concentrer pour l'instant sur le serveur CPU, ce qui vous évite pour l'instant de vous embêter avec les authentifications
- notre objectif ici et de bien comprendre la structure de la réponse
  posez-vous notamment la question de savoir quand est-ce que c'est terminé, et regardez bien la fin de la réponse
- pour l'instant aussi, on ignore le flag *streaming*: on poste une requête et on attend le retour

+++

## v06: on affiche la réponse

dans cette version, on utilise la réponse du serveur pour **afficher le dialogue** dans notre application  
pour cela on va devoir faire quelques modifications à la classe `History`; en effet vous devez avoir observé à ce stade que la réponse vient "en petits morceaux", ce qui fait qu'on pourrait avoir envie de modifier un peu la classe `History` de sorte qu'elle expose à présent les méthodes

- `add_prompt()` et `add_answer()` pour distinguer entre les deux types d'entrée
- et surtout `add_chunk()` qui permet d'ajouter *juste un mot* dans la réponse du robot, pour nous ajuster avec le format de la réponse

+++

## v07: pas de multiples requêtes

à ce stade il est utile d'ajouter un peu de logique pour éviter que l'on puisse poster deux requêtes "en même temps": on **rend l'UI inactive** jusqu'à réception de la réponse  
pour cela voyez dans `flet` l'attribut `disabled`

+++

## v08: supporter le mode *streaming*

une requête HTTP "classique" est d'une grande simplicité: on envoie une requête, on reçoit une réponse  
dans notre cas toutefois, ce modèle n'est pas tout à fait adapté, car l'IA met du temps à élaborer sa réponse, et on aimerait mieux **voir la réponse au fur et à mesure**, plutôt que de devoir attendre la fin, qui est le comportement que vous obeservez si vous avez suivi mes indications jusqu'ici  
c'est ce à quoi on va s'attacher maintenant  
il se trouve que le serveur `ollama` retourne ce qu'on appelle une réponse HTTP qui est un *stream*  

du coup on peut facilement modifier notre code pour en tirer parti en écrivant quelque chose comme:

```
    with requests.post(url, json=data, stream=True) as answer:
        print("HTTP status code:", answer.status_code)
        for line in answer.iter_lines():
            # do something with the line...
```

````{admonition} ne gardez qu'un seul mode

dans mon code j'ai conservé les deux modes (streaming et non-streaming) pour pouvoir montrer la différence de comportement, mais honnêtement le mode *non-streaming* ne présente pas d'intérêt en pratique, donc n'hésitez pas à ne garder **que** le mode non-streaming, ce sera plus lisible
````

+++

## v09: authentification

à ce stade il est temps d'ajouter du code pour pouvoir s'**authentifier avec le login/password** auprès du serveur qui en a besoin  
c'est juste une question d'ajouter, dans l'appel à `requests.post`, un paramètre `auth=(user, password)`

+++

## v10 (optionnel): acquérir la liste des modèles

plutôt que de proposer une liste de modèles "en dur" comme dans le *starter code*, on pourrait à ce stade **acquérir**, auprès du serveur choisi, la **liste des modèles** connus; pour cela `ollama` met à notre disposition l'API `/api/tags`

dans mon implémentation j'ai choisi de "cacher" ce résultat, pour ne pas redemander plusieurs fois cette liste à un même serveur (cette liste bouge très très peu...); mais c'est optionnel; par contre ce serait sympa pour les utilisateurs de conserver, lorsque c'est possible, le modèle choisi lorsqu'on change de serveur...

+++

## pour aller plus loin

* je vous signale une page pleine de tutoriels intéressants, et un peu du même genre, à propos de la librairie `flet`:
  <https://flet.dev/docs/tutorials>
