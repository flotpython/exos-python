---
jupytext:
  cell_metadata_json: true
  encoding: '# -*- coding: utf-8 -*-'
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
  title: students and groups
---

# parsing people and groups

+++

Licence CC BY-NC-ND, Thierry Parmentelat

+++

```{admonition} grab the zip for starters

{download}`you will need the zipfile that you can find here<./ARTEFACTS-parse-people.zip>`
```

+++

This activity is about parsing text files, and building structures using builtin types.

+++

## read a file

* **works on**: `list` `file` `tuple`
* **the input**: file contains lines like
  ```
  first_name last_name email phone
  ```
  fields are separated by any number (but at least one) of spaces/tabs, like e.g. in file `people-simple-03`
  ```{literalinclude} people-simple-03
  ```
* **todo**: write a function for parsing this format; it should return a list of 4-tuples
  ```python
  def parse(filename) -> list[tuple[str, str, str, str]]:
      ... 
  ```

```{code-cell} ipython3
# prune-cell

def parse(filename):
    """
    parse the file and returns a list of 4-tuples
    """
    result = []
    with open(filename, encoding="utf-8") as f:
        for line in f:
            first, last, email, phone = line.strip().split()
            result.append((first, last, email, phone))
    return result

L = parse("data-simple-03"); L
```

```{code-cell} ipython3
# prune-cell

def parse_bis(filename):
    """
    almost the same
    shorter, but no control that each line has exactly 4 fields
    """
    result = []
    with open(filename, encoding="utf-8") as f:
        for line in f:
            result.append(line.strip().split())
    return result

parse_bis("data-simple-03")
```

```{code-cell} ipython3
# prune-cell

def parse_ter(filename):
    """
    even shorter
    is that really more readable ?
    """
    with open(filename, encoding="utf-8") as f:
        return [line.strip().split() for line in f]
    
parse_ter("data-simple-03")
```

````{admonition} discussion

in the whole TP we will model a person as a 4-tuple  
however we could just as well have decided to use instead a dictionary with 4 keys  
discuss the pros and cons of each approach
````

+++

## indexing

* **works on**: hash-based types, comprehensions
* **what we need**: a fast way to
  * check whether an email is in the file
  * quickly retrieve the details that go with a given email
* **question**: what is the right data structure to implement that ?
* **todo**:
  * write a function
    ```python
    def index(list_of_tuples):
    ```
    that builds and returns that data structure
  * write a function
    ```python
    def initial(list_of_tuples):
    ```
    that indexes the data on the initial of the first name (what changes do we need to do on the resulting data
    structure ?)

```{code-cell} ipython3
# prune-cell

# first_name, last_name, email, phone = tup
# 0           1          2      3

def index(list_of_tuples):
    """
    build a dictionary of those tuples, keyed on the email
    the tedious but safe way
    """
    result = {}
    for tup in list_of_tuples:
        first, last, email, phone = tup
        result[email] = tup
    return result

D = index(L); D
```

```{code-cell} ipython3
# prune-cell

def index_bis(list_of_tuples):
    """
    a little more pythonic
    use unpacking to separate fields
    """
    result = {}
    for tup in list_of_tuples:
        # unpacking
        *_, email, _ = tup
        result[email] = tup
    return result

index_bis(L)
```

```{code-cell} ipython3
# prune-cell

def index_ter(list_of_tuples):
    """
    with a comprehension
    no unpacking means we need to use
    a constant index in t[2]
    """
    return {t[2]: t for t in list_of_tuples}

index_ter(L)
```

```{code-cell} ipython3
# prune-cell

def index_quater(list_of_tuples):
    """
    comprehension and unpacking
    """
    return {email: (*start, email, end)
            for *start, email, end in list_of_tuples}

index_quater(L)
```

```{code-cell} ipython3
# prune-cell

def initial(list_of_tuples):
    """
    indexing on the first name's initial letter

    so this time the values in the output dict
    must be LISTS
    """
    result = {}
    for tup in list_of_tuples:
        first, last, email, phone = tup
        # note that it's a little dangerous to
        # override 'initial' here
        # this is NOT a recommended pratice !
        # fortunately we do not need to
        # refer to the function in the function body
        # (not a recursive function)
        initial = first[0]
        # beware that we need to check for the presence
        # of the key before we can refer to the value
        if initial not in result:
            result[initial] = []
        # now it's OK
        result[initial].append(tup)
    return result

DI = initial(L); DI
```

```{code-cell} ipython3
# prune-cell

from collections import defaultdict
def initial_bis(list_of_tuples):
    """
    thanks to defaultdict we can spare
    the existence of the key in the dict
    """
    result = defaultdict(list)
    for tup in list_of_tuples:
        # unpacking
        first, *_ = tup
        result[first[0]].append(tup)
    return result

initial_bis(L)
```

## dataframe (optional)

* **works on**: dataframes
* **todo**: build a pandas dataframe to hold all the data
* **tip**: see [the documentation of
  `pd.DataFrame()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
  and observe that there are multiple interfaces to build a dataframe

```{code-cell} ipython3
# prune-cell

import pandas as pd

def dataframe(list_of_tuples):
    """
    clearly that's the way to go with this kind of data...
    """
    return pd.DataFrame(
        list_of_tuples,
        columns=['first_name', 'last_name', 'email', 'phone']
    )

dataframe(L)
```

## groups

* **works on**: `set`
* **a more elaborate input**  
  the file now contains optional fields
  ```
  first_name last_name email phone [group1 .. groupn]
  ```
  where the part between `[]` is **optional**, i.e there can be **0 or more** groupnames mentioned on each student line; like e.g. from `people-groups-10`:
  ```{literalinclude} people-groups-10
  ```
* **todo** duplicate and tweak the `parse` function, so as to write
  ```python
  def group_parse(filename):
  ```
  so it now returns a 2-tuple with
  * the list of tuples as before
  * a dictionary of sets
    * the keys here will be the **group names**,
    * and the corresponding value is **a set of tuples** corresponding to the students in that group

```{code-cell} ipython3
# prune-cell

def group_parse(filename):
    """
    returns a tuple with
    * a list of tuples, like what parse() returns
    * the groups as a dictionary
      groupname -> set of tuples
    """
    persons = []
    groups_by_name = defaultdict(set)
    with open(filename, encoding="utf-8") as feed:
        for line in feed:
            fi, la, em, ph, *groups = line.strip().split()
            person = (fi, la, em, ph)
            persons.append(person)
            for group in groups:
                groups_by_name[group].add(person)
    return persons, groups_by_name

G = group_parse("data-groups-10"); G
```

```{code-cell} ipython3
# prune-cell

# same using type hints to describe the types
def group_parse_bis(filename) -> tuple[
    list[tuple],
    dict[str, set[tuple]]
]:
    return group_parse(filename)

group_parse_bis("data-groups-10")
```

## regexps (optional)

* **works on**: regexps
* **what we need**: be able to *check the format* for the input file:
  * first_name and last_name may contain letters and `-` and `_`
  * email may contain letters, numbers, dots (.), hyphens (-) and must contain exactly one `@`
  * phone numbers may contain 10 digits, or `+33` followed by 9 digits
* **todo**: write a function
  ```python
  def check_values(L: list[tuple]) -> None:
  ```
  that expects as an input the output of `parse`, and that outlines ill-formed input
* **note** on ASCII *vs* Unicode input: 
  * in a first approximation, use patterns like `a-z` to check for letters;  
  * how does this behave with respect to names with accents and cedillas
  * then play with `\w` to see if you can overcome this problem

```{code-cell} ipython3
# prune-begin
```

```{code-cell} ipython3
import re

# let's consider several variants that all share the same structure

def _check_values(L, re_n, re_e, re_p):
    for first_name, last_name, email, phone in L:
        if not re_n.match(first_name):
            print(f"incorrect first_name {first_name}")
        if not re_n.match(last_name):
            print(f"incorrect last_name {last_name}")
        if not re_e.match(email):
            print(f"incorrect email {email}")
        if not re_p.match(phone):
            print(f"incorrect phone {phone}")
```

```{code-cell} ipython3
# first rough approx.
re_names = re.compile("^[-_a-zA-Z]+$")
re_email = re.compile("^[-a-zA-Z0-9.]+@[-a-zA-Z0-9.]+$")
# we need to escape the + because otherwise it means repetition
re_phone = re.compile("^(0|\+33)[0-9]{9}$")


def check_values(L: list) -> None:
    return _check_values(L, re_names, re_email, re_phone)

L120 = group_parse("data-groups-120")[0]
check_values(L120)
```

```{code-cell} ipython3
# using \w is tempting, but it will allow for _
# and we dont want that...

re_names_bis = re.compile("^[-_\w]+$")
re_email_bis = re.compile("^[-\w0-9.]+@[-\w0-9.]+$")

def check_values_bis(L: list) -> None:
    return _check_values(L, re_names_bis, re_email_bis, re_phone)

check_values_bis(L120)
```

```{code-cell} ipython3
# the safe way imho
letters = "a-zàâçéèêëîïôûùüÿæœ"
re_names_ter = re.compile(f"^[-_{letters}]+$", re.IGNORECASE)
re_email_ter = re.compile(f"^[-{letters}0-9.]+@[-{letters}0-9.]+$", re.IGNORECASE)


def check_values_ter(L: list[tuple]) -> None:
    return _check_values(L, re_names_ter, re_email_ter, re_phone)

check_values_ter(L120)
```

```{code-cell} ipython3
# prune-end
```

***
