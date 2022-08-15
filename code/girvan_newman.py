"""
Module for detecting communities using Girvan-Newman algorithm.

author: @anshulrao
date:   07-08-2022

"""

from graph import Graph


class GirvanNewman(object):
    def __init__(self, g):
        """
        Constructor.

        """
        if not isinstance(g, Graph):
            raise TypeError("Type of graph object is incorrect.")
        self.g = g

    def _compute_ebc(self):
        """
        Computes edge-betweenness centrality (ebc) scores for all the edges
        in graph.

        """
        edge_betweenness = dict.fromkeys([tuple(e) for e in self.g.edges], 0)

        def bfs(root):
            """
            BFS (Breadth-First Traversal) starting from root node.

            :param root: the starting node for BFS traversal.
            :return: shortest paths dictionary that stores the number of
            different paths present to a certain node from root node, depth
            dictionary that stores the depth at which a particular node
            exists w.r.t. the root node and a reverse_edges representation of
            reverse/backward edges that will help in computing edge-betweenness
            centrality when we go back up in reverse.

            Time Complexity: O(V + E)
            Space Complexity: O(V)
            """
            shortest_paths = dict.fromkeys(self.g.nodes, 1)
            reverse_edges = {}
            queue = [root]
            visited = {root}
            depth = {root: 0}

            while queue:
                # the current node is the parent whose children we will check.
                parent = queue.pop(0)
                for child in self.g.list[parent]:
                    if child not in visited:
                        queue.append(child)
                        visited.add(child)
                        depth[child] = depth[parent] + 1
                        # add reverse edges from child to parent.
                        if child not in reverse_edges:
                            reverse_edges[child] = [parent]
                        else:
                            reverse_edges[child].append(parent)
                        # this child is visited for the first time so the
                        # number of shortest paths to reach this node is
                        # same as its parent.
                        shortest_paths[child] = shortest_paths[parent]
                    # checking that child node is indeed a child since it has
                    # already been visited.
                    elif depth[parent] == depth[child] - 1:
                        # add reverse edges from child to parent.
                        if child not in reverse_edges:
                            reverse_edges[child] = [parent]
                        else:
                            reverse_edges[child].append(parent)
                        # this child has already been visited earlier
                        # so we will add the shortest paths of its another
                        # parent to it.
                        shortest_paths[child] += shortest_paths[parent]
            return shortest_paths, depth, reverse_edges

        # consider each root as the root
        for root in self.g.nodes:
            paths, levels, edges = bfs(root)
            # sort the levels in the reverse order because we intend
            # to traverse in reverse.
            levels = {k: v for k, v in sorted(levels.items(),
                                              key=lambda item: item[1],
                                              reverse=True)}

            prev = dict()
            for u in levels:
                if u != root:
                    # considering current backward edge (u, v) and computing its
                    # ebc score w.r.t. root.
                    for v in edges[u]:
                        # 1 is the default capacity for every node.
                        # we add to it the previously added value at node u
                        # to get total capacity.
                        # after that we divide that value by shortest paths at u.
                        # and then distribute among all nodes connected to u.
                        # for example, if capacity of node u is 1 and number of
                        # shortest paths crossing u is 3, then we will divide
                        # 1/3 = 0.33. let's say we have two backward edges from
                        # u: (u, v1) and (u, v2). v1 has two paths and v1 has one
                        # path crossing it.
                        # so, ebc score for (u, v1) = 0.33 and (u, v2) = 0.33 * 2.

                        val = ((1 + prev.get(u, 0)) / paths[u]) * paths[v]
                        if u < v:
                            edge_betweenness[(u, v)] += val
                        else:
                            edge_betweenness[(v, u)] += val
                        # v can be connected to two nodes u1 and u2.
                        # its capacity value will get incremented from each of
                        # (u1, v) and (u2, v) ebc score.
                        if v not in prev:
                            prev[v] = val
                        else:
                            prev[v] += val

        # divide all scores by 2 and round them off too.
        edge_betweenness = {k: round(v / 2, 2)
                            for k, v in edge_betweenness.items()}

        return edge_betweenness

    def _decouple_graph(self, edges_to_remove):
        """
        Remove the edges from the graph

        :param edges_to_remove: edges with high edge-betweenness
        centrality values that are to be removed.

        Time Complexity = O(V + E)
        """
        visited = dict.fromkeys(self.g.nodes, False)

        # delete the edges from the graph
        for u, v in edges_to_remove:
            self.g.del_edge(u, v)

        def dfs(comp, vertex):
            """
            DFS (Depth-First Traversal) of the graph.
            :param comp: current connected component.
            :param vertex: current vertex.

            """
            visited[vertex] = True
            comp.append(vertex)
            for node in self.g.list[vertex]:
                if not visited[node]:
                    comp = dfs(comp, node)
            return comp

        # look for connected components using DFS.
        connected_components = []
        for node in self.g.nodes:
            if not visited[node]:
                component = []
                connected_components.append(dfs(component, node))

        return connected_components

    def detect_communities(self):
        communities = []
        # in this version of the algorithm as soon as the graph splits into
        # two or more communities, we stop there.
        while len(communities) < 2:
            # compute edge-betweenness centrality values.
            ebc_scores = self._compute_ebc()
            # remove edges with maximum ebc score values.
            edges_to_remove = [k for k, v in ebc_scores.items()
                               if v == max(ebc_scores.values())]
            communities = self._decouple_graph(edges_to_remove)
        return communities, self.g
