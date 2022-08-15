"""
Script to detect communities using Girvan-Newman Algorithm.

author: @anshulrao
date:   07-08-2022
"""

import sys

from girvan_newman import GirvanNewman
from graph import Graph
import pickle


def get_graph(filename):
    """
    Read a file that has edges (one edge per row where an edge
    from a to b is written as 'a b') and return graph.

    :param filename: name of the file that has edges.
    :return: an undirected graph created using the list of edges.
    """
    # read file having edges.
    with open(filename, "r") as f:
        data = f.read()

    # convert read data to a nested list of edges.
    edges = []
    is_digit = False
    if data[0].isdigit():
        is_digit = True
    for edge in set(data.split("\n")) - {""}:
        u, v = edge.split()
        if is_digit:
            edges.append([int(u), int(v)])
        else:
            edges.append([u, v])

    return Graph(edges)


def plot_communities(communities, g):
    """
    Plot the communities and save it as "communities.html".

    """
    from pyvis.network import Network
    network = Network()
    count = 1
    for community in communities:
        for node in community:
            network.add_node(node, label=node, group=count)
        count += 1

    for u in g.list:
        for v in g.list[u]:
            if u < v:
                network.add_edge(u, v)

    network.show("communities.html")


def main():
    """
    The main method.

    """
    filename = sys.argv[1]
    sys.setrecursionlimit(5000)

    g = get_graph(f"data/{filename}.txt")  #
    girvan_newman = GirvanNewman(g)
    communities, g = girvan_newman.detect_communities()
    with open(f"{filename}_communities.pkl", "wb") as f:
        pickle.dump(communities, f)
    with open(f"{filename}_community_network.pkl", "wb") as f:
        pickle.dump(g, f)
    plot_communities(communities, g)


if __name__ == "__main__":
    main()
