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
  title: "aller chercher de la donn\xE9e sur Internet"
---

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat &amp; Arnaud Legout</span>
</div>

+++

# fetch the Internet

+++

## JSON

+++

commençons par une donnée en JSON; par exemple ceci <https://github.com/samayo/country-json/blob/master/src/country-by-population.json>  
pour trouver le bon lien, je clique sur 'Raw' et je copie ici

```{code-cell} ipython3
URL1 = "https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-population.json"
```

Il s'agit pour nous d'écrire un code qui **va chercher cette donnée** et les traduit en une **structure Python** 
(à base de `list` et `dict`) -  
la structure en question est déjà présente dans le JSON.

+++

### Indices sur la librairie `requests`

ce module ne fait pas partie de la librairie standard, il faut l'installer avec .. *wait for it*  

```bash
pip install requests
```

(il y a des fonctions de ce genre dans la librairie standard, mais c'est celle-ci qui est le plus souvent utilisée)

+++

#### poster la requête

```{code-cell} ipython3
import json

import requests
```

```{code-cell} ipython3
# il faut être un peu patient, surtout si votre réseau est un peu lent

response = requests.get(URL1)
```

#### les attributs de l'objet response

```{code-cell} ipython3
# dans ce genre de cas dir() est utile
# sauf que c'est un peu trop bavard
# dir(response)
```

```{code-cell} ipython3
# du coup ça vaut le coup de filter un peu

[symbol for symbol in dir(response) if not symbol.startswith('_')]
```

```{code-cell} ipython3
# si tout s'est bien passé ici on doit avoir 200
# (pour être précis: entre 200 et 299)
# c'est un des codes de retours de HTTP
# si c'est par exemple 404 ça signifie que cette URL n'existe plus

response.status_code
```

```{code-cell} ipython3
# si on était curieux on pourrait aussi faire

response.headers
```

```{code-cell} ipython3
# pour voir par exemple la taille de notre donnée

response.headers['Content-Length']
```

```{code-cell} ipython3
# mais bon, bien sûr ce qu'on veut surtout c'est le contenu
# c'est une chaine, regardons les 100 premiers caractères

print(type(response.text))
print(response.text[:100], '...')
```

### indices sur la librairie `json`

pour le coup, elle est dans la stdlib; les deux méthodes intéressantes sont 

* `json.loads(json_string)` qui décode une chaine JSON en un objet Python, et
* `json.dumps(object)` qui encode un object Python en une chaine JSON

+++

### le code

du coup le code que je dois écrire pour faire le job est simplement

```{code-cell} ipython3
def get_url_as_json(url):
    """
    Fetch a URL and decode its result as JSON
    """

    with requests.get(url) as response:
        return json.loads(response.text)
```

```{code-cell} ipython3
python_friendly = get_url_as_json(URL1)

# on obtient quoi comme type ?
type(python_friendly)
```

```{code-cell} ipython3
python_friendly[:3]
```

```{code-cell} ipython3
python_friendly[-3:]
```

```{code-cell} ipython3
len(python_friendly)
```

### option: transformer la structure

```{code-cell} ipython3
# et ici par exemple je pourrais décider que c'est plus pratique
# sous la forme d'un dictionnaire name -> population

population = {d['country']: d['population'] for d in python_friendly}
```

```{code-cell} ipython3
# de sorte que je peux faire simplement
population['France']
```

## CSV

Vous trouverez à cette URL un accès aux données de population par pays 
<https://github.com/datasets/population/blob/main/data/population.csv>  

````{admonition} Attention
ce ne sont pas les mêmes données exactement, celles-ci sont beaucoup plus détaillées...
````

```{code-cell} ipython3
# pareil, on clique sur 'Raw' pour obtenir le lien vers la donnée 'crue'

URL2 = "https://raw.githubusercontent.com/datasets/population/main/data/population.csv"
```

```{code-cell} ipython3
:tags: [raises-exception]

# il faut être un peu patient car c'est bcp + gros que tout à l'heure

response = requests.get(URL2)
response.headers['Content-Length']
```

### indices sur la librairie csv

```{code-cell} ipython3
# il semble donc qu'on ait affaire à un csv classique
# qu'on peut décortiquer avec object csv.reader
# https://docs.python.org/3/library/csv.html

import csv
```

il se trouve que la librairie `csv` fournit un objet `csv.reader` qui prend **un paramètre de type `file`**  
c'est-à-dire comme par exemple le résultat de `open()`  

ça demande une petite gymnastique, car nous avons le texte en mémoire, et pas dans un fichier...

+++

### option 1 - pas beau !

**très inélégant**, mais qui peut marcher à la rigueur:  
j'ai une chaine, je l'écris dans un fichier, que je peux ensuite rouvrir en lecture pour le passer à `csv.reader` ...  
une option viable en dernier recours, mais on ne va pas le faire, car c'est très vilain, et il y a une astuce pour s'en sortir autrement:

+++

### option 2 - mieux

exactement pour contourner ce genre de cas, il y a une classe `io.StringIO` qui, en partant d'une chaine en mémoire, se comporte comme un fichier ! et donc on va utiliser cela :

```{code-cell} ipython3
# pour utiliser csv.reader, il nous faut un objet de type fichier (file-like object)
# et c'est là que StringIO est super pratique

from io import StringIO

with (StringIO(response.text)) as file_like:
    reader = csv.reader(file_like, delimiter=',')
    # on regarde juste les 3 premiers enregistrements
    for i, row in enumerate(reader, 1):
        print(i, row)
        if i >= 3:
            break
```

À ce stade, on voit comment on peut transformer nos données en listes Python;
mais on va s'arrêter là, parce qu'en pratique ça c'est vraiment un exercice qu'on ferait en pandas...

+++

## un aperçu de `pandas`

`pandas` est une librairie externe aussi, qu'il faut absolument connaitre un peu, dès qu'on manipule de la data  
et pour commencer il y a une fonction `read_csv` qui va faire le job complet (acquisition et chargement) en un seul appel:

```{code-cell} ipython3
import pandas as pd
```

```{code-cell} ipython3
# en vrai on fait comme ça: être patient .. à nouveau

df = pd.read_csv(URL2)
```

```{code-cell} ipython3
# on regarde un peu ce qu'il y a dedans

df.head(3)

# on peut aussi regarder la fin avec df.tail(3)
```

```{code-cell} ipython3
# conversion en date

df['time'] = pd.to_datetime(df.Year, format="%Y")
```

```{code-cell} ipython3
df.head(3)
```

```{code-cell} ipython3
# on nettoie / renomme

del df['Year']

df = df.rename(columns = {
    'Country Name': 'country',
    'Country Code': 'code',
    'Value': 'population',
})
```

```{code-cell} ipython3
df.head(2)
```

```{code-cell} ipython3
# on choisit un index un peu plus parlant

df = df.set_index('time')
```

```{code-cell} ipython3
df.head(2)
```

```{code-cell} ipython3
# on se définit arbitrairement une période qui nous intéresse

begin = pd.to_datetime('1980', format='%Y')
end = pd.to_datetime('2010', format='%Y')
```

```{code-cell} ipython3
:scrolled: true

# on filtre ce qui nous intéresse

df_france = df[(df.country == 'France') & (df.index >= begin) & (df.index <= end)]
df_france.head
```

```{code-cell} ipython3
# on peut maintenant dessiner

df_france[['population']].plot();
```
