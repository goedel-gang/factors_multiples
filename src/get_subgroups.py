#!/usr/bin/env python3

"""
Determine all subgroups of a set of numbers interpreted as a graph as per all
the rest of the stuff whatever
"""

from improve import link_exists

def subgroups(l):
    groups = []
    while l:
        target = l.pop()
        group = {target}
        for ind, i in reversed(list(enumerate(l))):
            if link_exists(i, target):
                group.add(l.pop(ind))
        groups.append(group)
    return groups
