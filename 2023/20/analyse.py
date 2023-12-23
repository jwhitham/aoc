
import math
from main import Problem

"""
There are 48 flip flops.

They seem to be organised as 4 * 12 bit counters.

The counters reset at different points. My guess is that
when all four counters reset simultaneously, the output is triggered.

Need to know the reset point of each counter - need to know
at least two times when it resets - then it's possible to
calculate when resets coincide.
"""

def main() -> None:
    stateful = Problem("input").get_stateful_list()
    ff0 = ff1 = 0
    num_bits = len(stateful)
    count = [0 for i in range(num_bits)]
    total = 0
    seen = set()
    for line in open("part2.txt", "rt"):
        ff0 = ff1
        ff1 = int(line.split()[0], 16)
        assert not (ff1 in seen)
        seen.add(ff1)
        for i in range(num_bits):
            if ((ff0 ^ ff1) >> i) & 1:
                count[i] += 1
        total += 1

    log2 = math.log(2.0)
    resorted = []
    for (i, (c, v)) in enumerate(zip(stateful, count)):
        proportion = v / total
        cbit = math.inf
        if v != 0:
            cbit = -(math.log(proportion) / log2)
        resorted.append((cbit, i, v, proportion, c))

    resorted.sort()
    for (cbit, i, v, proportion, c) in resorted:
        print(f"name {c.name:5s} bit {i:3d} changed {v:5d} {proportion:1.6f} counter? {cbit:6.3f}")

if __name__ == "__main__":
    main()
