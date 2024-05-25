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
  title: "cr\xE9ation de facture"
---

# génération de facture

+++

## le problème

+++

on veut automatiser la rédaction de factures à partir d'une liste d'items et de prix

+++

exemple d'utilisation, imaginons qu'on a les données suivantes :

```{code-cell} ipython3
company_address = """Tribeca Inc.,
Somerset House – New Wing
Lancaster Place
London WC2R 1LA
"""

thanks_message = "Thanks for shopping with us today!"

currency = '€'

items = [
    ("Books", 25.0, 2),
    ("Monitor", 250.0, 1),
    ("Computer", 500.0, 1),
]
```

à partir de ces données on pourrait imaginer plusieurs APIs pour produire des factures comme ceci

+++

## v0 : une fonction

+++

l'API la plus simple évidemment ce serait tout simplement ceci

```{code-cell} ipython3
from invoice import generate_invoice
```

```{code-cell} ipython3
invoice = generate_invoice(
    items, company_address, thanks=thanks_message, currency='$')
print(invoice)
```

### suggestions / indices

* dans un premier temps, affichez le contenu de `company_address` tel quel
  * ensuite définissez une fontion - par exemple `center_address` qui se charge seulement de centrer l'adresse dans une certaine largeur
* les formats de f-string sont un trait très pratique ici

```{code-cell} ipython3
texte = "tutu"
largeur = 10
```

```{code-cell} ipython3
# on peut utiliser une variable AUSSI pour la largeur du format
# ici je prends 10 caractères, et je justifie mon texte à droite (le >)
#         ↓  ↓↓↓↓↓
f"X{texte:>{largeur}}X"
```

```{code-cell} ipython3
# et on peut aussi centrer (le ^) ou justifier à gauche (<)
#         ↓
f"X{texte:^{largeur}}X"
```

## v1 : une classe

+++

maintenant on peut aussi imaginer une autre façon d'implémenter ceci, en passant par une classe, comme par exemple

```{code-cell} ipython3
from invoice import InvoiceGenerator
```

```{code-cell} ipython3
generator = InvoiceGenerator(
    address=company_address, 
    thanks=thanks_message,
    currency='$')

print(generator.invoice(items))
```

## solution

Comme toujours, les annotations *type hints* sont totalement optionnelles

+++

### une solution v0

Dans une toute première version, on pourrait penser à faire des `print()` dans la fonction.

Toutefois cette approche **n'est pas recommandée**; il vaut beaucoup mieux construire et renvoyer une chaine; de cette façon l'appelant pourra toujours choisir d'utiliser `print()` de son coté


`````{admonition} ouvrez-moi
:class: dropdown

````{literalinclude} invoice.py
:start-after: prune-v0-start
:end-before: prune-v1-start
````
`````

+++

### une solution v1

`````{admonition} ouvrez-moi
:class: dropdown

````{literalinclude} invoice.py
:start-after: prune-v1-start
````
`````
