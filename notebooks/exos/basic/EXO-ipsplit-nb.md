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
  title: manipulation simple sur une adresse IP
---

# analyse adresse IP

+++

## le problème

+++

Une adresse IP v4 se présente sous la forme d'une chaine contenant 4 octets (de 0 a 255 donc) en décimal séparés par des `.`

```{code-cell} ipython3
# exemples

IP_1 = "192.168.0.9"
IP_2 = "138.96.19.1"
```

```{code-cell} ipython3
from ipsplit import ip_v0, ip_v1
```

## v0

+++

On vous demande d'écrire une fonction qui transforme cette donnée (une chaine donc) en une liste de 4 entiers

```{code-cell} ipython3
# remarquez bien l'absence de quotes (') dans le résultat
ip_v0(IP_1)
```

```{code-cell} ipython3
# doit retourner True
ip_v0(IP_1) == [192, 168, 0, 9]
```

```{code-cell} ipython3
# doit retourner True
ip_v0(IP_2) == [138, 96, 19, 1]
```

## v1

+++

Même analyse, mais le retour est un entier dans l'espace $[0..2^{32}-1]$

Si j'appelle $b_0$, $b_1$, $b_2$, $b_3$ les 4 valeurs retournées par `ip_v0`, le résultat ici sera obtenu avec la formule

$I = b_0.2^{24} + b_1*2^{16} + b_2*2^8 + b_3$

```{code-cell} ipython3
# doit retourner True
ip_v1(IP_1) == 0xc0a80009
```

```{code-cell} ipython3
# doit retourner True
ip_v1(IP_2) == 0x8a601301
```

## astuce

+++

Comment faire ces calculs facilement de manière interactive ?

```{code-cell} ipython3
# les différents morceaux de ip_v0 valent ceci
hex(192), hex(168), hex(0), hex(9)
```

```{code-cell} ipython3
# ça veut dire que le résultat final doit être ceci
0xc0a80009
```

## solution

````{admonition} ouvrez-moi
:class: dropdown

```{literalinclude} ipsplit.py
```
````
