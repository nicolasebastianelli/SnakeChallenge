"""
Snake Problem
=============

Question
--------

Write a program that calculates how many different ways a snake of
length 16 can be laid out on a 4x4 grid.


Example
-------

Given a grid like so::

    +---------+---------+---------+---------+
    |         |         |         |         |
    |    0    |    1    |    2    |    3    |
    |         |         |         |         |
    +---------+---------+---------+---------+
    |         |         |         |         |
    |    4    |    5    |    6    |    7    |
    |         |         |         |         |
    +---------+---------+---------+---------+
    |         |         |         |         |
    |    8    |    9    |   10    |   11    |
    |         |         |         |         |
    +---------+---------+---------+---------+
    |         |         |         |         |
    |   12    |   13    |   14    |   15    |
    |         |         |         |         |
    +---------+---------+---------+---------+


one path would be
``[0, 1, 2, 3, 7, 6, 5, 4, 8, 9, 10, 11, 15, 14, 13, 12]``::

    +---------+---------+---------+---------+
    |  Start  |         |         |         |
    |    0---------1---------2---------3    |
    |         |         |         |    |    |
    +---------+---------+---------+----|----+
    |         |         |         |    |    |
    |    4---------5---------6---------7    |
    |    |    |         |         |         |
    +----|----+---------+---------+---------+
    |    |    |         |         |         |
    |    8---------9---------10-------11    |
    |         |         |         |    |    |
    +---------+---------+---------+----|----+
    |   End   |         |         |    |    |
    |    12-------13--------14--------15    |
    |         |         |         |         |
    +---------+---------+---------+---------+


and another ``[5, 6, 10, 9, 8, 4, 0, 1, 2, 3, 7, 11, 15, 14, 13, 12]``::

    +---------+---------+---------+---------+
    |         |         |         |         |
    |    0---------1---------2---------3    |
    |    |    |         |         |    |    |
    +----|----+---------+---------+----|----+
    |    |    |  Start  |         |    |    |
    |    4    |    5---------6    |    7    |
    |    |    |         |    |    |    |    |
    +----|----+---------+----|----+----|----+
    |    |    |         |    |    |    |    |
    |    8---------9--------10    |   11    |
    |         |         |         |    |    |
    +---------+---------+---------+----|----+
    |  End    |         |         |    |    |
    |   12--------13--------14--------15    |
    |         |         |         |         |
    +---------+---------+---------+---------+

There are many more but what is the total of all possible unique paths?


Rules
-----

* Do not output all the paths, just the total path count.  A single
  number is all that is required as output of this program.

* Diagonal movements are not allowed.

* Use Python 3.8+ and the standard modules only.  No Numpy or any third
  party modules.


Tips
----

* The answers for smaller square grids:

    * 1x1 grid (snake length 1) has 1 path.
    * 2x2 grid (snake length 4) has 8 paths.
    * 3x3 grid (snake length 9) has 40 paths.

* Consider performance when writing your solution.

* We will test your solution with square grids of different sizes.

"""


class SnakeGraph:

    def __init__(self, edge_length):

        self.__node_number = edge_length ** 2
        self.__adjacent_node = self.__compute_adjacent_nodes(edge_length)
        self.__found_paths = 0

    # Build a list of list representing the adjacency matrix of the graph.
    def __compute_adjacent_nodes(self, edge_length):

        nodes = [[] for _ in range(self.__node_number)]
        for i in range(self.__node_number):

            # Node is not in first row.
            if i >= edge_length:
                nodes[i].append(i - edge_length)

            # Node is not in last row.
            if i+edge_length < self.__node_number:
                nodes[i].append(i + edge_length)

            # Node is not in first column.
            if (i % edge_length) != 0:
                nodes[i].append(i - 1)

            # Node is not in last column.
            if ((i+1) % edge_length) != 0:
                nodes[i].append(i + 1)

        return nodes

    # Return the central node of odd length graphs, e.g. 5x5.
    def __get_graph_central_node(self):
        if self.__node_number % 2 == 0:
            return None
        return int(self.__node_number/2)

    # Return the set of representative nodes for the current graph.
    # A node is representative when applying rotations on the graph it covers other nodes of the graph.
    def __get_representative_subgraph_nodes(self):
        edge_length = int(self.__node_number**(1/2.))
        i = int(edge_length / 2)
        j = int(round(edge_length/2.+0.1))
        return [jj+ii*edge_length for ii in range(i) for jj in range(j)]

    # [Depth-First Search] Given a starting node and the visited nodes list,
    # it recursively find all the Hamiltonian Paths.
    def __find_hamiltonian_paths(self, start, visited):

        # Stopping criteria: if some nodes are unreachable stop the current exploration.
        if not self.__all_nodes_are_reachable(start, visited):
            return

        visited[start] = True

        if all(visited):
            self.__found_paths += 1
            return

        for adj in self.__adjacent_node[start]:
            if not visited[adj]:
                self.__find_hamiltonian_paths(adj, visited)
                visited[adj] = False  # Backtracking.

    # [Flood-Fill Algorithm] Check if all nodes are still reachable.
    def __all_nodes_are_reachable(self, start, visited):
        if visited.count(True) < 5:  # At least 5 exploration are required to make a node unreachable.
            return True
        flooded_visited = visited[:]
        self.__flood_graph(start, flooded_visited)
        if all(flooded_visited):
            return True
        else:
            return False

    # [Depth-First Search]
    def __flood_graph(self, start, flooded_visited):
        flooded_visited[start] = True
        for adj in self.__adjacent_node[start]:
            if not flooded_visited[adj]:
                self.__flood_graph(adj, flooded_visited)

    def find_all_hamiltonian_paths(self):
        self.__found_paths = 0

        # Compute Hamiltonian Paths starting from only representative sub-nodes of the graph
        # (it reduce by 4 the computation time)
        for i in self.__get_representative_subgraph_nodes():
            visited = [False] * self.__node_number
            self.__find_hamiltonian_paths(i, visited)
        self.__found_paths *= 4

        # Compute Hamiltonian Paths starting from central node of the graph
        i = self.__get_graph_central_node()
        if i is not None:
            visited = [False] * self.__node_number
            self.__find_hamiltonian_paths(i, visited)

    def get_number_of_possible_path(self):
        return self.__found_paths


def path_count(edge_length):
    graph = SnakeGraph(edge_length)
    graph.find_all_hamiltonian_paths()
    return graph.get_number_of_possible_path()


"""
Tests run on: MacBook Pro - Core i5 2,3 GHz - Ram 8 GB 2133 MHz

edge_length=1     time: 5.912e-05 seconds    solution: 1
edge_length=2     time: 7.581e-05 seconds    solution: 8
edge_length=3     time: 3.850e-04 seconds    solution: 40
edge_length=4     time: 7.284e-03 seconds    solution: 552
edge_length=5     time: 0.3646438 seconds    solution: 8648
edge_length=6     time: 24.621315 seconds    solution: 458696
edge_length=7     time: 7505.7514 seconds    solution: 27070560
"""

if __name__ == '__main__':
    import time
    start_time = time.time()
    print(path_count(edge_length=7))
    print("--- %s seconds ---" % (time.time() - start_time))
