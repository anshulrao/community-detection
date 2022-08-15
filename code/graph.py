"""
Class module for graph.

author: @anshulrao
date:   07-08-2022
"""


class Graph(object):

    def __init__(self, edges, list=True):
        """
        Constructor.

        """
        self.edges = edges
        self.nodes = set()
        for edge in edges:
            self.nodes.update(edge)
        self.list = {key: [] for key in self.nodes}
        if not list:
            self.initialize_matrix()  # adjacency matrix representation
        else:
            self.initialize_list()  # adjacency list representation

    @property
    def V(self):
        return len(self.nodes)

    @property
    def E(self):
        return len(self.edges)

    def initialize_matrix(self):
        # TODO: implement this function to return adjacency list
        pass

    def initialize_list(self):
        """
        Initialize an adjacency list representation of graph using
        list of edges.
        """
        for u, v in self.edges:
            self.add_edge(u, v)

    def add_edge(self, u, v):
        self.list[u].append(v)
        self.list[v].append(u)

    def del_edge(self, u, v):
        self.list[u].remove(v)
        self.list[v].remove(u)
