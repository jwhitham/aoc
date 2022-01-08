from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os
import re
import enum
import bisect

INPUT = Path("input")

class Action(enum.Enum):
    ON = enum.auto()
    OFF = enum.auto()
    TOGGLE = enum.auto()

def subdivide(todo, offset):
    division = set()
    for (_, c1, c2) in todo:
        division.add(c1[offset])
        division.add(c2[offset])
    return sorted(division)


def main(filename: Path = INPUT) -> int:
    todo = []
    for line in open(filename, "rt"):
        ints = [int(x) for x in re.findall(r"\d+", line)]
        if line.startswith("turn on"):
            action = Action.ON
        elif line.startswith("toggle"):
            action = Action.TOGGLE
        elif line.startswith("turn off"):
            action = Action.OFF
        (x1, y1, x2, y2) = ints
        todo.append((action, (x1, y1), (x2 + 1, y2 + 1)))

    dimensionx = subdivide(todo, 0)
    dimensiony = subdivide(todo, 1)
    cell_on = set()
    brightness = collections.defaultdict(lambda: 0)

    for (action, c1, c2) in todo:
        xi1 = bisect.bisect_left(dimensionx, c1[0])
        xi2 = bisect.bisect_left(dimensionx, c2[0])
        yi1 = bisect.bisect_left(dimensiony, c1[1])
        yi2 = bisect.bisect_left(dimensiony, c2[1])
        assert dimensionx[xi1] == c1[0], (dimensionx[xi1], c1[0])
        assert dimensionx[xi2] == c2[0]
        assert dimensiony[yi1] == c1[1]
        assert dimensiony[yi2] == c2[1]

        for xi in range(xi1, xi2):
            for yi in range(yi1, yi2):
                key = (xi, yi)
                if action == Action.TOGGLE:
                    if key in cell_on:
                        cell_on.remove(key)
                    else:
                        cell_on.add(key)
                    brightness[key] += 2
                elif action == Action.ON:
                    cell_on.add(key)
                    brightness[key] += 1
                else:
                    cell_on.discard(key)
                    brightness[key] = max(brightness[key] - 1, 0)

    total = 0
    for (xi, yi) in cell_on:
        total += ((dimensionx[xi + 1] - dimensionx[xi]) *
                    (dimensiony[yi + 1] - dimensiony[yi]))
    print("part 1:", total)
    total = 0
    for (xi, yi) in brightness:
        total += (brightness[(xi, yi)] *
                    (dimensionx[xi + 1] - dimensionx[xi]) *
                    (dimensiony[yi + 1] - dimensiony[yi]))
    print("part 2:", total)


if __name__ == "__main__":
    main()


