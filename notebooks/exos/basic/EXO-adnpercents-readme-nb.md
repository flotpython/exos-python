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
  title: calcul de % dans un brin d'ADN
---

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat &amp; Arnaud Legout</span>
</div>

+++

# pourcentages

+++

## problème (simple)

En partant d'un string qui représente un brin d'ADN

```{code-cell} ipython3
dna = "GGCGCGCCATCGCCGGCTGGCGGAAATT"
```

Calculer les deux pourcentages de nucleotides 

 * les `C` ou `G`
 * les `A` ou `T`

et imprimez le résultat comme ceci

```{code-cell} ipython3
from adnpercents import nice_format

nice_format(dna)
```

### * Indices

* Entraînez-vous à utiliser les f-strings lorsque c'est possible
* `"{:2f}"` pour écrire un flottant avec deux chiffres significatifs
* il existe aussi un format `%` ou lieu de `f` qui peut être utile dans ce cas également

```{code-cell} ipython3
# remember to use f-strings

f"le brin {dna}"
```

```{code-cell} ipython3
# for formatting numbers

pi = 3.1415916
f"pi={pi:.2f}"
```

## un peu plus compliqué

À faire peu plus tard (cf. aussi f-strings):  
Écrire une fonction `format_dna` qui permet à son appelant de spécifier le format de présentation

```{code-cell} ipython3
from adnpercents import format_dna
```

```{code-cell} ipython3
format_dna(dna, "la chaine {dna} a\n {at} de (A ou T)")
```

### indices

voyez la méthode `str.format()`

+++

## solution

à noter: dans `percents_at_cg_bis`, l'utilisation de `collections.Counter` pour faire les calculs

````{admonition} ouvrez-moi
:class: dropdown

```{literalinclude} adnpercents.py
```
````
