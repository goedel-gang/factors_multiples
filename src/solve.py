"""
Program to optimize the "factors and multiples game" [1], by modelling the
problem as a longest path on an undirected, unweighted graph, and using a simple
depth-first search to brute force paths. Depth first is used to reduce spatial
complexity.

[1]: https://nrich.maths.org/5468/note
"""

from pprint import pformat
from shutil import get_terminal_size
from time import time
from random import sample
from math import gcd

from smartparse import ArgumentParser

WIDTH, _ = get_terminal_size()
UPDATE_FREQ = 50000

def get_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-r", "--randomise", action="store_true",
                help="randomise the graph search")
    parser.add_argument("-g", "--gcd", action="store_true",
                help="order each node by gcd (can be randomised first)")
    parser.add_argument("-n", type=int, default=100,
                help="size of 'board'")
    parser.add_argument("-v", "--verbose", action="store_true",
                help="print info")
    return parser.parse_args()

def construct_graph(n, get_shuffle):
    """
    Construct directed graph with vertices {1..n} where each vertex connects to
    each of its factors and multiples. It uses a directed representation of this
    normally undirected graph so DFS can be applied. Not particularly worried
    about time complexity here as this is a singly used initialisation.

    It could be a dictionary but seeing as the keys are in the range [1..n] this
    is better represented as a list, which is still a kind of mapping.
    """
    return [1] + [get_shuffle([j for j in range(1, i) if i % j == 0] # factors
                             + list(range(2 * i, n + 1, i)), i) # multiples
            for i in range(1, n + 1)] # each tile

def _paths(graph, seen, path, cur):
    """
    Recursively generate paths from a (directed, cyclic) graph, from a current
    path and position.  To generate all paths, use the wrapper function paths().
    """
    dead_end = True
    for vertex in graph[cur]:
        if not seen[vertex]:
            dead_end = False
            seen[vertex] = True
            path.append(vertex)
            yield from _paths(graph, seen, path, vertex)
            path.pop()
            seen[vertex] = False
    if dead_end:
        yield path

def paths(graph, get_shuffle):
    """
    Wraps _paths() to find all possible paths from a (directed, cyclic) graph
    with no current state.
    """
    for vertex in get_shuffle(list(range(1, len(graph))), None):
        seen = [False] * (len(graph))
        seen[vertex] = True
        yield from _paths(graph, seen, [vertex], vertex)

def longest_path(n, get_shuffle, v=False):
    v and print("Looking for longest path in 1..{}".format(n))
    graph = construct_graph(n, get_shuffle)
    v and print("Constructed graph {}".format(pformat(graph, width=WIDTH)))
    best_path = []
    start = time()
    try:
        for ind, path in enumerate(paths(graph, get_shuffle)):
            if ind % UPDATE_FREQ == 0:
                v and print("\r{:.1e}@{:.1e}Hz" .format(ind,
                                                        ind / (time() - start)),
                            end="")
            if len(path) > len(best_path):
                best_path = list(path)
                print("\r[{}]{}".format(len(best_path),
                                        " ".join(map(str, best_path))))
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    args = get_args()
    if args.randomise:
        def get_shuffle(l, node):
            ret = sample(l, len(l))
            if args.gcd and node is not None:
                if args.verbose:
                    print("sorting by gcd: {} {}".format(l, node))
                # sort in descending order by gcd with node
                ret.sort(key=lambda n: gcd(n, node), reverse=True)
                if args.verbose:
                    print("result: {}".format(ret))
            return ret
    else:
        get_shuffle = lambda l, node: l
    longest_path(args.n, get_shuffle, v=args.verbose)
