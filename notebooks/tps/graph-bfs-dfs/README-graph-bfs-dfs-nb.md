---
jupytext:
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
---

# walking a graph: BFS - DFS

+++

Licence CC BY-NC-ND, Thierry Parmentelat

+++

```{admonition} just a HOWTO
:class: tip

this notebook contains running code, there is no exercise attached
```

+++

## depth-first or breadth-first

given a non-valued directed graph G, and a start vertex V, there are 2 famous algorithms to walk the graph from V

* depth-first (DF) browsing, and
* breadth-first (BF) browsing

intuitively, considering for example from the following tree

```{code-cell} ipython3
import graphviz

tree = graphviz.Digraph(engine='dot')
tree.edge('v', 'v1')
tree.edge('v1', 'v11')
tree.edge('v1', 'v12')
tree.edge('v11', 'v111')
tree.edge('v11', 'v112')
tree.edge('v12', 'v121')
tree.edge('v12', 'v122')
tree.edge('v', 'v2')
tree.edge('v2', 'v21')
tree.edge('v2', 'v22')
tree.edge('v21', 'v211')
tree.edge('v21', 'v212')
tree.edge('v22', 'v221')
tree.edge('v22', 'v222')

tree
```

these 2 algorithms would yield the nodes in the following orders

+++ {"cell_style": "split"}

DF browsing **from `v`** would scan (the newlines are only cosmetic)

```text
v v1 v11 v111 v112
v12 v121 v122
v2 v21 v211 v212
v22 v221 v222
```

+++ {"cell_style": "split"}

BF browsing **from `v`** would scan (ditto)
```
v
v1 v2
v11 v12 v21 v22
v111 v112 v121 v122 v211 v212 v221 v222
```

+++

## objectives

+++

we want to write a **generator** that implements these 2 browsing policies from a graph and vertex.  
of course, only the nodes reachable from the entry vertex will be browsed by this method

+++

## algorithms

the 2 algorithms used to perform these scans are, interestingly, **very close** to one another  
in both cases we need a STORAGE object, where we can `store()` things and `retrieve()` them later on

+++

### FIFO / FILO

+++

Let us consider the following 2 storage implementations:

* `Fifo` implements a *first-in-first-out* policy
* `Filo` does the exact opposite and has a *first-in-last-out* policy

```{admonition} list or deque

Remember the regular `list` class is more optimized for a `append()/pop()` usage

So to work around that, we're using a `deque` class, instead of a simple list; it is actually useful only in the `Filo` case, but this way we have a more homogeneous code
```

**Exercise**: you may wish to factorize both into a single class...

But let's get to it:

```{code-cell} ipython3
:cell_style: split

from collections import deque

class Fifo:
    def __init__(self):
        self.line = deque()
    def store(self, item):
        self.line.append(item)
    def retrieve(self):
        if self.line:
            return self.line.popleft()
    def __len__(self):
        return len(self.line)
```

```{code-cell} ipython3
:cell_style: split

from collections import deque

class Filo:
    def __init__(self):
        self.line = deque()
    def store(self, item):
        self.line.append(item)
    def retrieve(self):
        if self.line:
            return self.line.pop()
    def __len__(self):
        return len(self.line)
```

```{code-cell} ipython3
:cell_style: split

# let's check it does what we want

fifo = Fifo()
for i in range(1, 4):
    fifo.store(i)
while fifo:
    print(f"retrieve → {fifo.retrieve()}")
```

```{code-cell} ipython3
:cell_style: split

# same here

filo = Filo()
for i in range(1, 4):
    filo.store(i)
while filo:
    print(f"retrieve → {filo.retrieve()}")
```

```{code-cell} ipython3
def scan(start, storage):
    """
    performs a scan of all the vertices reachable from start vertex

    in an order that is DF or BF, depending on the
    storage policy (fifo or filo)

    assumptions:

    * vertices reachable from a vertex are
      stored in a 'neighbours' attribute

    * storage should have store() and retrieve() methods
      and be testable for emptiness (if storage: ...)
    * also it should be empty when entering the scan
    """

    storage.store(start)
    # keep track of what we've seen
    scanned = set()

    while storage:
        current = storage.retrieve()
        # skip vertices already seen
        if current in scanned:
            continue
        yield current
        scanned.add(current)
        for neighbour in current.neighbours:
            storage.store(neighbour)
```

```{code-cell} ipython3
class Vertex:
    def __init__(self, name):
        self.name = name
        self.neighbours = set()

    def __repr__(self):
        return self.name

    def add_neighbour(self, other):
        self.neighbours.add(other)
```

```{code-cell} ipython3
# rebuild sample graph
def tree_vertex(name, depth):
    if depth == 0:
        return Vertex(name)
    elif depth > 0:
        result = Vertex(name)
        result.add_neighbour(tree_vertex(name+'1', depth-1))
        result.add_neighbour(tree_vertex(name+'2', depth-1))
        return result
```

```{code-cell} ipython3
g = tree_vertex('v', 3)
g
```

+++ {"cell_style": "split"}

### FILO = DF - depth first

+++ {"cell_style": "split"}

### FIFO = BF - breadth first

```{code-cell} ipython3
:cell_style: split

for vertex in scan(g, Filo()):
    print(vertex)
```

```{code-cell} ipython3
:cell_style: split
:inputHidden: false
:outputHidden: false

for vertex in scan(g, Fifo()):
    print(vertex)
```

### applications

+++

being a generator, we can combine it with all the `itertools` and the like

```{code-cell} ipython3
import itertools
```

for example, if we need to print every other vertex in a DF scan

```{code-cell} ipython3
:cell_style: split

df_scan = scan(g, Filo())

for v in itertools.islice(df_scan, 0, None, 2):
    print(v)
```

```{code-cell} ipython3
:cell_style: split
:tags: [level_intermediate]

# notice that df_scan is now exhausted !

for v in itertools.islice(df_scan, 0, None, 2):
    print(v)
```

or skip the first 3..

```{code-cell} ipython3
# but we can easily create a new one !
df_scan = scan(g, Filo())

for v in itertools.islice(df_scan, 3, None):
    print(v)
```

+++ {"cell_style": "center"}

***
