---
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
  cell_metadata_json: true
  encoding: '# -*- coding: utf-8 -*-'
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
  title: students and groups
---

# parsing people and groups

parsing text files, and building structures using builtin types

in order to work on this exercise from your laptop, {download}`start with downloading the zip<./ARTEFACTS-parse-peo.zip>`

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

+++

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

+++

## dataframe (optional)

* **works on**: dataframes
* **todo**: build a pandas dataframe to hold all the data
* **tip**: see [the documentation of
  `pd.DataFrame()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
  and observe that there are multiple interfaces to build a dataframe

+++

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

+++

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

+++

***
