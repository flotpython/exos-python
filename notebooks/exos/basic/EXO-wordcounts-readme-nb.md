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
  title: comptages de mots
---

# classe `WordCounts`

on veut calculer la fréquence d'apparition des mots dans un texte  
pour cela on vous demande d'écrire une classe qui s'utilise comme ceci  


````{admonition} données
le fichier texte contient le premier chapitre du *Hitch-Hiker's Guide to the Galaxy* - alias hhgg  
{download}`vous pouvez le télécharger ici<./wordcounts-data.txt>`  
vous pouvez aussi utiliser n'importe quel autre document au format text brut
````

```{code-cell} ipython3
from wordcounts import WordCounts

wc = WordCounts("wordcounts-data.txt")

# on choisit arbitrairement d'afficher les 5 mots les + fréquents
print(wc)
```

```{code-cell} ipython3
# ensuite on peut chercher le nombre d'occurences comme ceci

for word in ['arthur', 'people']:
    print(f"word {word} was found {wc.counter[word]} times")
```

```{code-cell} ipython3
# et voir si un mot apparait ou pas

for word in ['arthur', 'armageddon']:
    present = word in wc.vocabulary()
    print(f"is word '{word}' present ? : {present} ")
```

## Indices

* il est raisonnable de tout mettre en minuscule une bonne fois au tout début du traitement
* voyez éventuellement le module standard `string`, et `string.punctuation`
* sachez aussi que le texte en question contient des apostrophes non-ASCII `“”`
* voyez aussi la classe `collections.Counter`, qui va vous rendre la vie bien plus facile

+++

## variantes

* comment trouveriez-vous tous les mots qui apparaissent entre 30 et 40 fois dans le texte ?
* si vous vous sentez confortable (il faut faire de la surcharge d'opérateur),
  faites en sorte qu'on puisse aussi écrire:

```{code-cell} ipython3
for word in ['arthur', 'people']:
    # here we can index the WordCount instance directly
    print(f"word {word} was found {wc[word]} times")
```

## solution

````{admonition} la classe
:class: dropdown

```{literalinclude} wordcounts.py
```
````

````{admonition} les recherches
:class: dropdown

```python
# les mots apparassant entre 30 et 40 fois

{word for word, count in wc.counter.items() if 30 <= count <= 40}

-> {'and', 'it', 'was'}

```
````
