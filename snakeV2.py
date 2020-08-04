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

    def __compute_adjacent_nodes(self, edge_length):

        nodes = [[] for _ in range(self.__node_number)]
        for i in range(self.__node_number):

            # Node not in first row
            if i >= edge_length:
                nodes[i].append(i - edge_length)

            # Node not in last row
            if i+edge_length < self.__node_number:
                nodes[i].append(i + edge_length)

            # Node not in first column
            if (i % edge_length) != 0:
                nodes[i].append(i - 1)

            # Node not in last column
            if ((i+1) % edge_length) != 0:
                nodes[i].append(i + 1)

        return nodes

    def find_all_hamiltonian_paths(self):
        self.__found_paths = 0
        for i in range(self.__node_number):
            visited = [False] * self.__node_number
            visited[i] = True
            self.__find_hamiltonian_paths(i, visited, [i])

    def __find_hamiltonian_paths(self, start, visited, path):

        if len(path) == self.__node_number:
            self.__found_paths += 1
            return

        for adj in self.__adjacent_node[start]:

            if not visited[adj]:
                visited[adj] = True
                self.__find_hamiltonian_paths(adj, visited, path+[adj])
                visited[adj] = False

    def get_number_of_possible_path(self):
        return self.__found_paths


def path_count(edge_length):
    graph = SnakeGraph(edge_length)
    graph.find_all_hamiltonian_paths()
    return graph.get_number_of_possible_path()


if __name__ == '__main__':
    import time
    start_time = time.time()
    print(path_count(edge_length=5))
    print("--- %s seconds ---" % (time.time() - start_time))
