from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os
import re

INPUT = Path("input")


def thing1(filename: Path) -> int:
    total = 0
    for line in open(filename, "rt"):
        [w, h, d] = [int(x) for x in re.findall("\d+", line)]
        area1 = w * h
        area2 = h * d
        area3 = w * d
        smallest = min(area1, area2, area3)
        total += 2 * area1 + 2 * area2 + 2 * area3 + smallest
    return total 

def thing2(filename: Path) -> int:
    total = 0
    for line in open(filename, "rt"):
        [w, h, d] = [int(x) for x in re.findall("\d+", line)]
        perimeter1 = 2 * (w + h)
        perimeter2 = 2 * (h + d)
        perimeter3 = 2 * (w + d)
        smallest = min(perimeter1, perimeter2, perimeter3)
        volume = w * h * d
        total += volume + smallest
    return total

def main() -> None:
    answer = thing1(INPUT)
    print("part 1:", answer)

    answer = thing2(INPUT)
    print("part 2:", answer)


if __name__ == "__main__":
    main()


