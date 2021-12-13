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
        self.matrix: typing.Dict[XY, str] = collections.defaultdict(lambda: ' ')
        self.rows = 0
        self.cols = 0

    def add(self, line: str) -> None:
        pair = line.split(",")
        x = int(pair[0])
        y = int(pair[1])
        self.matrix[(x, y)] = '#'
        self.rows = max(self.rows, y + 1)
        self.cols = max(self.cols, x + 1)

    def fold_x(self, at_x: int) -> None:
        for y in range(self.rows):
            for x1 in range(at_x + 1, self.cols):
                x2 = at_x - (x1 - at_x)
                self.matrix[(x2, y)] = combine(
                    self.matrix[(x2, y)], self.matrix[(x1, y)])
                self.matrix[(x1, y)] = ' '

        self.recompute_boundary()

    def fold_y(self, at_y: int) -> None:
        for x in range(self.cols):
            for y1 in range(at_y + 1, self.rows):
                y2 = at_y - (y1 - at_y)
                self.matrix[(x, y2)] = combine(
                    self.matrix[(x, y2)], self.matrix[(x, y1)])
                self.matrix[(x, y1)] = ' '

        self.recompute_boundary()

    def recompute_boundary(self) -> None:
        mx = my = 0
        for x in range(self.cols - 1, 0, -1):
            for y in range(self.rows - 1, 0, -1):
                if self.matrix[(x, y)] == '#':
                    mx = max(x, mx)
                    my = max(y, my)
        self.cols = mx + 1
        self.rows = my + 1

    def count(self) -> int:
        return len([1 for i in self.matrix.values() if i == '#'])

    def do_print(self) -> None:
        for y in range(self.rows):
            print(''.join([self.matrix[(x, y)] for x in range(self.cols)]))
                            

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


