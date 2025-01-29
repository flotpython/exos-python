---
jupytext:
  formats: md:myst
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
---

# ants: a genetic algorithm

+++ {"tags": ["prune-cell"]}

````{admonition} nothing to prune
:class: warning

there are no difference - apart from this very cell - between the teacher and the student version, but the notebook is duplicated in .teacher for consistency
````

+++ {"slideshow": {"slide_type": ""}, "tags": ["prune-cell"]}

```{admonition} grab the zip for starters

{download}`you will need the zipfile that you can find here<./ARTEFACTS-ants.zip>`
```

+++

## problem statement

our goal in this activity is to implement an optimization algorithm that is an example of a *genetic algorithm*  
it turns out this algorithm can solve two equivalent problems

### traveling salesman

specifically, we consider a famous problem, which is of great importance for everything logistics, and is known as **the *"traveling salesman"* problem**  
consider for example a truck that needs to deliver parcels in several locations  
the problem is to find **the shortest path** (or more accurately, a reasonably short path)

- that starts from the warehouse
- goes through all the locations
- and returns to the warehouse

### ants colony problem

the traveling salesman problem is in fact equivalent to the one known as the **the *"ants colony"* problem**, where the colony needs to find the best route from the ant hill and back, that goes through the spots where food has been found  

this latter metaphor is **a little more helpful** though in the context of the genetic algorithm, because the algorithm indeed mimicks the existence of several ants that concurrently walk the graph, and leave pheromons to keep track of the past

```{admonition} not *the* shortest path
is has been shown that finding *the* shortest path is an NP-problem, so it's untractable  
but as explained in the video, the genetic algorithm finds reasonable paths, in that they do not differ much from the optimal one
```

+++

## ACO: a super useful resource

the YouTube video below gives a 20' introduction on the algorithm known as *Ants Colony Optimization (ACO)*, and explains essentially all the logic and formulas needed to implement it  
```{iframe} https://www.youtube.com/embed/u7bQomllcJw?rel=0&amp;controls=1
```
so it is a **highly recommended** resource to get started with the details of the algorithm

```{admonition} not a video fan ?

[I found this one helpful too, in a totally different style](https://perso.liris.cnrs.fr/christine.solnon/publications/cpaior.pdf)

and there's plenty others around as well, google for 'ACO algorithm'
```

+++

## useful data

in the zip file you will find:

+++

### `data/*.csv`

we provide a few datafiles in the `data/` folder, made from some graphs that appear in the video  
these use a simple csv format that should be self explanatory (just forget the `radius` column)

| name | timestamp in video | # nodes |
|-|-|-|
| data/video-50.csv | 1:17 | 50 |
| data/video-30.csv | 3:14 | 30 |
| data/video-04.csv | 8:57 | 4 |
| data/video-10.csv | 11:25 | 10 |
| data/video-06.csv | 14:54 | 6 |
| data/video-66.csv | 17:44 | 66 |

plus for convenience some polygon-like shapes in `poly*.csv`

+++

### `data/*.path`

here we provide the results found by our own implementation; this in particular is used by the 'Cheat' button in `ui.py` - see below

+++

## problem.py

also provided in the zip, you can use `problem.py` like so:

```{code-cell} ipython3
from problem import Problem2D

problem = Problem2D("data/video-06.csv")
```

```{code-cell} ipython3
# how many nodes
len(problem)
```

```{code-cell} ipython3
# to iterate over nodes

for node in problem:
    print(node)
```

```{code-cell} ipython3
# or rather

for index, node in enumerate(problem):
    print(f"{index}-th node is {node}")
```

```{code-cell} ipython3
# get distance between 2 nodes

problem.distance(0, 2)
```

```{code-cell} ipython3
# what it says

problem.distance_along_path([0, 1, 2, 3, 0])
```

#### displaying the graphs

+++

we've also coded some display featured for your convenience

1st off, **provided that you have `graphviz` installed**

```{code-cell} ipython3
# you can do display it with graphviz like this

problem.to_graphviz()
```

```{code-cell} ipython3
# or this if you prefer

problem.to_graphviz(show_distances=False)
```

```{code-cell} ipython3
# prune-cell
# sub-optimal for big graphs though
Problem2D("data/video-50.csv").to_graphviz(show_distances=False)
```

#### if you prefer plotly

and there again, **provided that you have `plotly` installed** you could do

```{code-cell} ipython3
import plotly.io as pio

# Try one of these depending on your setup:
pio.renderers.default = "notebook"     # for classic Jupyter Notebook
```

```{code-cell} ipython3
problem.to_plotly()
```

```{code-cell} ipython3
# prune-cell 

Problem2D("data/video-50.csv").to_plotly(show_distances=False)
```

```{code-cell} ipython3
# prune-cell

p6 = Problem2D("data/video-06.csv")
p6.print_distances()
```

## `ui.py`

might come in handy too, it is a simple `flet` UI that lets you visualize your work; you might consider

- reading its code
- make sure your `solver.py` code fits the expected interface - or tweak `ui.py` according to your own interface
- run it with
```bash
flet run -d ui.py
```
so that the UI will hot reload upon any change you make in `solver.py`
