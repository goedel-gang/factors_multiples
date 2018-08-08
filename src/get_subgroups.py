#!/usr/bin/env python3

"""
Determine all subgroups of a set of numbers interpreted as a graph as per all
the rest of the stuff whatever

Pretty lazy implementation as it's not doing any heavy lifting, asymptotically.
"""

from improve import link_exists

from smartparse import ArgumentParser

def get_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-s", "--sequence", nargs="*", type=int,
                        help="sequence to find subgroups in")
    parser.add_argument("--invert", type=int,
                        help="range, for which the arguments will be inverted")
    return parser.parse_args()

def subgroups(l):
    groups = []
    while l:
        target = l.pop()
        group = {target}

        done = False
        while not done:
            done = True
            for ind, i in reversed(list(enumerate(l))):
                if any(link_exists(i, other) for other in group):
                    group.add(l.pop(ind))
                    done = False

        groups.append(group)
    return groups

if __name__ == "__main__":
    args = get_args()
    if args.invert is not None:
        args.sequence = [i for i in range(1, args.invert + 1)
                         if i not in args.sequence]
        print("inverted to {}".format(args.sequence))
    print("\n".join(" ".join(map(str, i))
                    for i in subgroups(args.sequence)))
