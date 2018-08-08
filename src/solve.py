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
from shutil import get_terminal_size

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
    """
    return {i: get_shuffle([j for j in range(1, i) if i % j == 0] # factors
                             + list(range(2 * i, n + 1, i)), i) # multiples
            for i in range(1, n + 1)} # each tile

def _paths(graph, seen, path, cur):
    """
    Recursively generate paths from a (directed, cyclic) graph, from a current
    path and position.  To generate all paths, use the wrapper function paths().
    """
    dead_end = True
    for vertex in graph[cur]:
        if vertex not in seen:
            dead_end = False
            seen.add(vertex)
            path.append(vertex)
            yield from _paths(graph, seen, path, vertex)
            path.pop()
            seen.remove(vertex)
    if dead_end:
        yield path

def paths(graph, get_shuffle):
    """
    Wraps _paths() to find all possible paths from a (directed, cyclic) graph
    with no current state.
    """
    for vertex in get_shuffle(graph.keys(), 1):
        yield from _paths(graph, {vertex}, [vertex], vertex)

def longest_path(n, get_shuffle, v=False):
    v and print("Looking for longest path in 1..{}".format(n))
    graph = construct_graph(n, get_shuffle)
    term_width = get_terminal_size()[0]
    v and print("Constructed graph {}".format(pformat(graph, width=term_width)))
    best_path = []
    start = time()
    for ind, path in enumerate(paths(graph, get_shuffle)):
        if ind % UPDATE_FREQ == 0:
            v and print("\r{:.1e}Hz  {}"
                .format(ind / (time() - start),
                    " ".join(map("{: >3}".format, path[:n // 5]))), end="")
        if len(path) > len(best_path):
            best_path = list(path)
            print("\rnew best [{}]{}".format(len(best_path),
                                             " ".join(map(str, best_path))))

if __name__ == "__main__":
    args = get_args()
    if args.randomise:
        def get_shuffle(l, node):
            ret = sample(l, len(l))
            if args.gcd:
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
