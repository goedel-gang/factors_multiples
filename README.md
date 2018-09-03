# factors\_multiples
Aiming to optimise the [NRich problem](https://nrich.maths.org/5468/solution)
for length, by various graphical algorithms.

The first approach was to implement a brute force DFS and leave this to run. I
quickly found that that was intractable, although really I knew that all along -
it was more about having something to implement in code, for the fun of it. I
also spent some time optimising it for speed, by for example pre-computing the
whole graph representing the board and using fast data-structures where possible
(favouring arrays, eg boolean array of visited locations and array of current
path.)

I modified this to instead traverse the board randomly. This quickly got some
better results. I also reimplemented this program in C rather than Python, to
gain about an order of magnitude of speed. I also wrote some utility programs
that try to naïvely or greedily insert remaining tiles between current tiles, or
to highlight the connected subgraphs within remaining tiles. However, with all
of this I was only able to generate a path of length 69.

I then spent a bit of time looking at the properties of my current solutions and
the better published solutions. I saw that they often included long "chains"
of multiples of large numbers, eg multiples of 17. I designed a simple heuristic
to emulate this behaviour, which is that the program tries to maximise the GCD
between adjacent elements. If two candidates have the same GCD, they are
randomly chosen between. Using this in conjunction with the greedy expansion
utility I generated the following sequence:

    >[76]58 29 87 3 69 23 92 46 2 62 31 93 1 35 70 10 40 80 20 100 50 25 75 15 45 90 30 60 12 96 48 24 72 36 18 54 27 81 9 63 21 42 84 28 56 14 98 49 7 91 13 52 26 78 6 66 33 99 11 44 22 88 8 16 32 64 4 76 38 19 95 5 85 17 68 34

![screenshot](https://github.com/elterminad0r/factors_multiples/blob/master/screenshot.png)

There are 10 primes between 50 and 100: 53, 59, 61, 67, 71, 73, 79, 83, 89, 97.
Only one of these can be used (via the 1), so this implies a weak upper bound of
91 as a chain length. My attempt is still pretty far from that and my program
isn't particularly sophisticated, and I've not actually had a go at
hand-optimising anything so I reckon it's still possible to get a much better
score.

Non-rigorously, I performed some exhaustive searches of lower board sizes which
might suggest that around 85 is a more reasonable goal:

    In [1]: 23 / 27, 24 / 28, 24 / 29, 26 / 30
    Out[1]:
    (0.8518518518518519,
     0.8571428571428571,
     0.8275862068965517,
     0.8666666666666667)
