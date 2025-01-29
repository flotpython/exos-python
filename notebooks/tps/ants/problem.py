"""
the basic bricks: how to model a problem

- at its root, a problem is just
  - an ordered collection of nodes (any Python object)
  - a matrix with the distances between the nodes
    remember that in general, the distance from node i to node j
    may be different from node j to node i

- a specific kind of problem is when the nodes are in an open 2D space
  so in this case we can assume each node has a position (x, y)
  and then infer the distances

"""

import math
import itertools
from dataclasses import dataclass

import numpy as np
import pandas as pd


class Problem:
    """
    in the most generic case, a problem is just a collection of nodes
    with a distance matrix - which does not have to be symmetric btw

    the diagonal of the matrix is always 0, although this is not enforced
    as the algorithm will never use it in fact
    """
    def __init__(self, nodes: list, distances: np.ndarray):
        self.nodes = nodes
        self.distances = distances
        # sanity check
        if  distances.shape != (len(nodes), len(nodes)):
            raise ValueError("distances should be a square matrix")

    # make it iterable
    def __iter__(self):
        return iter(self.nodes)
    def __len__(self):
        return len(self.nodes)
    def __getitem__(self, i):
        return self.nodes[i]

    def distance(self, i, j):
        return self.distances[i, j]

    def mean_distance(self):
        """
        helper to get a feeling of the problem size
        """
        n = len(self)
        if n <= 1:
            return 0
        total = sum(self.distance(i, j)
                    for i, j in itertools.product(range(n), repeat=2) if i != j)
        return total / (n*(n-1))

    def print_distances(self):
        """
        helper to list all distances
        probably useful on small problems only
        """
        for i, n1 in enumerate(self):
            print("==")
            for j, n2 in enumerate(self):
                if n1 != n2:
                    print(f"{n1.name} -> {n2.name} = {self.distance(i, j):.2f}")

    def distance_along_path(self, path):
        """
        what the name says
        """
        total = 0
        # we want to go back to the first node
        # so we add the starting node at the end of the iteration
        chain = list(itertools.chain(path, [path[0]]))
        # so now we can iterate over the pairs of vertices
        # the second argument of zip is shifted by one
        # so we have the next vertex in the path
        for i, j in zip(chain, chain[1:]):
            total += self.distance(i, j)
        return total


class Problem2D(Problem):

    # make it immutable and hashable
    @dataclass(frozen=True)
    class Node:
        name: str
        x: float
        y: float

        def distance(self, other):
            return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


    def __init__(self, filename):
        """
        if filename is provided, will load from that csv file
        that should have the following columns:
        name,x,y
        """
        nodes = list()
        if filename is not None:
            df = pd.read_csv(filename)
            for _, row in df.iterrows():
                nodes.append(Problem2D.Node(row["name"], row["x"], row["y"]))
        distances = np.zeros((len(nodes), len(nodes)))
        for i, n1 in enumerate(nodes):
            for j, n2 in enumerate(nodes):
                distances[i, j] = n1.distance(n2)

        super().__init__(nodes, distances)


    def to_graphviz(self, show_distances=True):
        """
        Return a Graphviz object representing the problem.
        Works directly in Jupyter (just evaluate the returned object).
        """
        try:
            from graphviz import Graph
        except ImportError:
            print("you need to install graphviz to use this function")
            return None

        G = Graph()
        # add nodes
        for i, n in enumerate(self.nodes):
            # use same coordinates as in the ui
            G.node(str(i), label=n.name, pos=f"{n.x},{-n.y}!", shape="circle")

        # add edges
        for i, _n1 in enumerate(self.nodes):
            for j, _n2 in enumerate(self.nodes):
                if j <= i:
                    continue  # avoid duplicates
                kwdargs = {}
                if show_distances:
                    kwdargs["xlabel"] = f"{self.distances[i, j]:.2f}"
                G.edge(str(i), str(j), **kwdargs)

        # important for Graphviz to use the pos= attribute
        G.attr(overlap="false")
        G.attr(splines="true")
        G.attr(layout="neato")  # neato respects pos
        return G



    def to_plotly(self, show_distances=True,
                    node_size=12, node_label_font=14, edge_width=1):
        """
        Display the problem as an interactive Plotly graph in Jupyter.
        - Nodes are fixed at their (x, y) positions.
        - Distances appear as hover text on edges (optional).
        """
        try:
            import plotly.graph_objects as go
        except ImportError:
            print("you need to install plotly to use this function")
            return None
        xs = [n.x for n in self.nodes]
        ys = [n.y for n in self.nodes]
        labels = [n.name for n in self.nodes]
        n = len(self.nodes)

        # Build edges
        edge_x, edge_y, edge_texts = [], [], []
        for i in range(n):
            for j in range(i + 1, n):  # undirected, no duplicates
                x0, y0 = self.nodes[i].x, self.nodes[i].y
                x1, y1 = self.nodes[j].x, self.nodes[j].y
                edge_x += [x0, x1, None]
                edge_y += [y0, y1, None]
                if show_distances:
                    edge_texts.append(f"{self.distances[i, j]:.2f}")
                else:
                    edge_texts.append(None)

        # Trace for edges
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            mode="lines",
            line=dict(width=edge_width, color="gray"),
            hoverinfo="text" if show_distances else "none",
            text=edge_texts
        )

        # Trace for nodes
        node_trace = go.Scatter(
            x=xs, y=ys,
            mode="markers+text",
            text=labels,
            textposition="top center",
            marker=dict(size=node_size, color="blue"),
            textfont=dict(size=node_label_font),
            hoverinfo="text"
        )

        fig = go.Figure([edge_trace, node_trace])
        fig.update_layout(
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1),
            width=600, height=600,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        return fig
