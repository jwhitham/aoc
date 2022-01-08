YEAR = 2021
DAY = 13
PART = 3
 
from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os
import re

INPUT = Path("input")
FOLD = re.compile(r"fold along (x|y)=(\d+)\s*$")
XY = typing.Tuple[int, int]

def combine(a: str, b: str) -> str:
    if "#" == a or "#" == b:
        return "#"
    else:
        return " "

class Grid:
    def __init__(self) -> None:
        self.dots: typing.Set[XY] = set()

    def add(self, line: str) -> None:
        pair = line.split(",")
        x = int(pair[0])
        y = int(pair[1])
        self.dots.add((x, y))

    def fold_x(self, at_x: int) -> None:
        copy: typing.Set[XY] = set()
        for (x1, y) in self.dots:
            if x1 > at_x:
                x2 = at_x - (x1 - at_x)
                copy.add((x2, y))
            else:
                copy.add((x1, y))
        self.dots = copy

    def fold_y(self, at_y: int) -> None:
        copy: typing.Set[XY] = set()
        for (x, y1) in self.dots:
            if y1 > at_y:
                y2 = at_y - (y1 - at_y)
                copy.add((x, y2))
            else:
                copy.add((x, y1))
        self.dots = copy

    def count(self) -> int:
        return len(self.dots)

    def do_print(self) -> None:
        matrix: typing.Dict[XY, str] = collections.defaultdict(lambda: " ")
        rows = cols = 0
        for (x, y) in self.dots:
            matrix[(x, y)] = '#'
            cols = max(x + 1, cols)
            rows = max(y + 1, rows)


        for y in range(rows):
            print(''.join([matrix[(x, y)] for x in range(cols)]))
                            

def folding1(filename: Path) -> int:
    g = Grid()
    for line in open(filename, "rt"):
        line = line.strip()
        m = FOLD.match(line)
        if m:
            if m.group(1) == "x":
                g.fold_x(int(m.group(2)))
            else:
                g.fold_y(int(m.group(2)))
            return g.count()

        elif line != "":
            g.add(line)

    return g.count()

def folding2(filename: Path) -> None:
    g = Grid()
    for line in open(filename, "rt"):
        line = line.strip()
        m = FOLD.match(line)
        if m:
            if m.group(1) == "x":
                g.fold_x(int(m.group(2)))
            else:
                g.fold_y(int(m.group(2)))
        elif line != "":
            g.add(line)

    g.do_print()

def test_part_1() -> None:
    assert folding1(Path("test")) == 17

def main() -> None:
    if not INPUT.exists():
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY), "download"])
        return

    subprocess.check_call([sys.executable, "-m", "mypy", sys.argv[0]])
    subprocess.check_call([sys.executable, "-m", "pytest", sys.argv[0]])

    answer = folding1(INPUT)
    print("part 1:", answer)

    if PART == 1:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "1", str(answer)])
        return

    folding2(INPUT)


if __name__ == "__main__":
    main()


