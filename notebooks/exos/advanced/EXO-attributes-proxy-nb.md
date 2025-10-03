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
  title: recherche d'attributs avec __getattr__
---

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat &amp; Arnaud Legout</span>
</div>

+++

# attributs et `__getattr__`

* On vous demande d'écrire une classe `Echo`
* qui répond à toutes les méthodes dont le nom  fait 3 lettres
* et qui dans ce cas retourne le nom de la méthode concaténé 3 fois

+++

```
>>> echo = Echo()
>>> echo.foo()
'foofoofoo'
>>> echo.bar()
'barbarbar'
>>> echo.six()
'sixsixsix''
```

+++

## Indices

* une seule méthode `__getattr__` suffit
* elle doit renvoyer une méthode
* ou lever l'exception AttributeError

```{code-cell} ipython3
class Echo:
    def __getattr__(self, attrname):
        if len(attrname) == 3:
            # on pourrait écrire tripler()
            # mais pour inspecter ce qui nous est vraiment passé
            def tripler(*args, **kwds):
                # print("incoming", args, kwds)
                return attrname * 3
            return tripler
        else:
            raise AttributeError(f"No such method {attrname} length = {len(attrname)} != 3")
```

```{code-cell} ipython3
echo = Echo()
echo.foo()
```

```{code-cell} ipython3
echo.bar()
```

```{code-cell} ipython3
try:
    echo.foobar()
except AttributeError as e:
    print("OOPS", e)
```

# Deuxième partie

+++

* on veut maintenant une classe Proxy
* qu'on crée à partir d'une instance de `Echo`
* et d'une blacklist (une liste de mots de 3 lettres)
* et qui répond là encore à toutes les méthodes
* dont le nom fait 3 lettres
* en sous-traitant à son instance de `Echo`
* sauf pour les méthodes dans la blacklist

+++

## Indices

* très similaire au précédent
* attention à bien appeler la méthode de `echo` 
  * une fois que vous l'avez localisée

+++

```
>>> blacklist = [ 'six', 'two', 'four']
>>> echo2 = BlacklistEcho(blacklist)
>>> echo2.foo()
'foofoofoo'
>>> echo2.six()
... raise AttributeError

```

```{code-cell} ipython3
class BlacklistEcho(Echo):
    def __init__(self, blacklist):
        super().__init__()
        self.blacklist = blacklist
    def __getattr__(self, attrname):
        if attrname in self.blacklist:
            raise AttributeError("blacklisted method {attrname}")
        return super().__getattr__(attrname)
```

```{code-cell} ipython3
blacklist = [ 'six', 'two', 'four']

echo2 = BlacklistEcho(blacklist)

echo2.foo()
```

```{code-cell} ipython3
try:
    echo2.six()
except AttributeError as e:
    print("OOPS", e)
```

```{code-cell} ipython3
try:
    echo2.foobar()
except AttributeError as e:
    print("OOPS", e)
```
