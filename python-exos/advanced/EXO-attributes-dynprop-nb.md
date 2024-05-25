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
  title: "cr\xE9ation dynamique de propri\xE9t\xE9s"
---

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat &amp; Arnaud Legout</span>
</div>

+++

# création de propriétés à la volée

+++

## en s'inspirant du code:

```{code-cell} ipython3
class Person(object):
    def __init__(self):
        self._name = ''

    def fget(self):
        print(f"Getting: {self._name}")
        return self._name

    def fset(self, value):
        print(f"Setting: {value}")
        self._name = value.title()

    name = property(fget=fget, fset=fset, doc="I'm the property.")
```

```{code-cell} ipython3
user = Person()
user.name = 'john smith'
```

```{code-cell} ipython3
# remarquez d'ailleurs - sans rapport avec l'exercice
# qu'ici on ne spécifie pas de deleter
try:
    del user.name
except AttributeError as e:
    print("OOPS", e)
```

## écrivez 

* une nouvelle version `DynamicPerson` de cette classe 
* qui ne possède plus les 2 méthodes `fget/fset`
* mais en remplacement une méthode `addProperty`
  * et autres méthodes privées si nécessaire
* de façon à ce qu'on puisse l'utiliser comme ceci

+++

```
>>> user = DynamicPerson()
>>> user.addProperty('name')
>>> user.addProperty('phone')
>>> user.name = 'john smith'
Setting: name = john smith
>>> user.phone = '12345'
Setting: phone = 12345
>>> user.name
Getting: name
'John Smith'
>>> user.__dict__
{'_phone': '12345', '_name': 'John Smith'}
```

+++

## indices

* pour cet exercice il semble plus naturel 
  * d'utiliser la *builtin* `property`
  * plutôt que la version avec décorateur
* remarquez que le récepteur de addProperty
  * est l'instance `user` 
  * et non la classe `Person`

```{code-cell} ipython3
# une façon possible de faire

class DynamicPerson(object):

    def addProperty(self, attribute):
        # avec une clôture on capture attribute
        # dans les getter et setter
        def setter(self, value):
            print(f"Setting: {attribute} = {value}")
            setattr(self, '_' + attribute, value)
        def getter(self):
            value = getattr(self, '_' + attribute)
            print(f"Getting: {attribute} = {value}")
            return value
        # on attache la property à la classe et pas à l'instance
        setattr(self.__class__,
                attribute,
                # le descriptor fabriqué par property
                property(fget=getter,
                         fset=setter,
                         doc=f"Auto-generated {attribute} method"))
```

```{code-cell} ipython3
user = DynamicPerson()
user.addProperty('name')
user.addProperty('phone')
user.name = 'john smith'
user.phone = '12345'
user.name
user.__dict__
```

## pour les rapides

* ajoutez du code de sorte que
  * `addProperty()`
  * crée l'attribut à une valeur `None`
  * ou encore mieux, à une valeur passée à `addProperty`
