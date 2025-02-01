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
notebookname: parcours de graphe
---

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat</span>
</div>

+++

### plus court chemin - algorithme de Dijkstra

+++

digression sur ce sujet

```{code-cell} ipython3
import graphviz
```

```{code-cell} ipython3
g = graphviz.Digraph(engine='dot')
g.edge('v1', 'v3', label='5')
g.edge('v1', 'v2', label='1')
g.edge('v2', 'v3', label='1')
g.edge('v3', 'v4', label='1')
g.edge('v2', 'v4', label='3')
g.edge('v2', 'v5', label='4')
g.edge('v4', 'v5', label='1')
g.edge('v4', 'v6', label='3')
g.edge('v5', 'v6', label='1')
g
```

```{code-cell} ipython3
graph = {
    'v1': {'v3': 5, 'v2': 1},
    'v3': {'v4': 1},
    'v2': {'v3': 1, 'v4': 3},
    'v4': {'v5': 1, 'v6': 3},
    'v5': {'v6': 1},
}
```

```{code-cell} ipython3
# inf stands for infinity
from math import inf

class ClosestNext(dict):

    def __init__(self):
        self.min_vertex = None
        self.min_distance = inf
        
    def record(self, vertex, total):
        if vertex in self:
            if total >= self[vertex]:
                return
        self[vertex] = total
        if total < self.min_distance:
            self.min_vertex = vertex
            self.min_distance = total
```

```{code-cell} ipython3
# calcule seulement la distance
def shortest_distance(graph_data, src, dst):
    explored = {src: 0}
    while dst not in explored:
        closest = ClosestNext()
        for past_vertex in explored:
            for next_vertex, distance in graph_data[past_vertex].items():
                if next_vertex in explored:
                    continue
                closest.record(next_vertex, explored[past_vertex] + distance)

        best_vertex = closest.min_vertex 
        # no progress: we're stuck
        if not best_vertex:
            print(f"NOPE, {explored}")
            return
        explored[best_vertex] = closest.min_distance
    print(f"YES ! shortest distance is {explored[dst]}")
```

```{code-cell} ipython3
shortest_distance(graph, 'v1', 'v6')
```

```{code-cell} ipython3
from math import inf

class ClosestPreviousNext(dict):

    def __init__(self):
        self.min_previous = None
        self.min_vertex = None
        self.min_distance = inf
        
    def record(self, previous, vertex, total):
        if vertex in self:
            if total >= self[vertex]:
                return
        self[vertex] = total
        if total < self.min_distance:
            self.min_previous = previous
            self.min_vertex = vertex
            self.min_distance = total
```

```{code-cell} ipython3
# même algo mais mémorise aussi le chemin
def shortest_path(graph_data, src, dst):
    # on en garde un peu plus dans cette structure
    explored = {src: (0, [src])}
    while dst not in explored:
        closest = ClosestPreviousNext()
        for past_vertex in explored:
            for next_vertex, distance in graph_data[past_vertex].items():
                if next_vertex in explored:
                    continue
                closest.record(past_vertex, next_vertex, explored[past_vertex][0] + distance)

        best_vertex = closest.min_vertex
        best_previous = closest.min_previous
        # no progress: we're stuck
        if not best_vertex:
            print(f"NOPE, {explored}")
            return
        explored[best_vertex] = (
            closest.min_distance, explored[best_previous][1] + [best_vertex])
    print(f"YES ! shortest path is {explored[dst]}")
```

```{code-cell} ipython3
shortest_path(graph, 'v1', 'v6')
```
