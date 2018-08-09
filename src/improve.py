"""
Script to perform naive optimisation of a path by examining adjacent pairs and
attempting to insert remaining numbers between them.

Generally, I'm not too bothered about performance here, as nothing is expected
to run on an arbitrarily large input or for an arbitrarily long time.

It also has a couple of assertions, which mean this is also used to check
validity of a sequence. Generally, I'm using it as a kind of post-processor for
other brute-forces outputs.
"""

from collections import deque
from itertools import islice
from random import shuffle

from smartparse import ArgumentParser

def get_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-s", "--sequence" , required=True, nargs="+", type=int,
            help="sequence to optimise")
    parser.add_argument("-n", type=int, default=100,
            help="size of board")
    return parser.parse_args()

def link_exists(a, b):
    return a % b == 0 or b % a == 0

def rolling_slice(it, n):
    it = iter(it)
    sl = deque(islice(it, n), maxlen=n)
    yield sl
    for i in it:
        sl.append(i)
        yield sl

def improve(nums, n):
    assert len(set(nums)) == len(nums)
    unused = list(set(range(1, n + 1)) - set(nums))
    shuffle(unused)
    for a, b in rolling_slice(nums, 2):
        assert link_exists(a, b)
        yield a
        for i in unused:
            if link_exists(a, i) and link_exists(b, i):
                unused.remove(i)
                yield i
                break
    yield b

if __name__ == "__main__":
    args = get_args()
    cur_seq = args.sequence
    print("given [{}]{}".format(len(cur_seq), " ".join(map(str, cur_seq))))
    while True:
        improvement = list(improve(cur_seq, args.n))
        if len(improvement) > len(cur_seq):
            print("improved to [{}]{}".format(len(improvement),
                                              " ".join(map(str, improvement))))
            cur_seq = improvement
        else:
            print("no further improvement found")
            break
