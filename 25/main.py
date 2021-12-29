 
from pathlib import Path
import unittest
import typing
import subprocess
import numpy
import sys
import os

INPUT = Path("input")

EAST = ord(">")
SOUTH = ord("v")
CLEAR = ord(".")

class Grid:
    def __init__(self, filename: Path) -> None:
        self.num_cols = self.num_rows = 0
        for line in open(filename, "rt"):
            self.num_cols = max(len(line.strip()), self.num_cols)
            self.num_rows += 1

        self.grid = numpy.zeros(shape=(self.num_cols, self.num_rows), dtype=numpy.int8)
        self.east = []
        self.south = []
        for (y, line) in enumerate(open(filename, "rt")):
            for (x, col) in enumerate(line.strip()):
                self.grid[x][y] = ord(col)
                if self.grid[x][y] == EAST:
                    self.east.append((x, y))
                elif self.grid[x][y] == SOUTH:
                    self.south.append((x, y))
                elif self.grid[x][y] != CLEAR:
                    self.grid[x][y] = CLEAR

    def step1(self, what, where_list, dx, dy) -> int:
        moved_list = []
        for (i, (x, y)) in enumerate(where_list):
            x2 = (x + dx) % self.num_cols
            y2 = (y + dy) % self.num_rows
            if self.grid[x2][y2] == CLEAR:
                moved_list.append(i)

        for i in moved_list:
            (x, y) = where_list[i]
            x2 = (x + dx) % self.num_cols
            y2 = (y + dy) % self.num_rows
            assert self.grid[x][y] == what
            assert self.grid[x2][y2] == CLEAR
            self.grid[x2][y2] = what
            self.grid[x][y] = CLEAR
            where_list[i] = (x2, y2)

        return len(moved_list)

    def step(self) -> int:
        east_steps = self.step1(EAST, self.east, 1, 0)
        south_steps = self.step1(SOUTH, self.south, 0, 1)
        return east_steps + south_steps

    def show(self) -> None:
        for y in range(self.num_rows):
            line = []
            for x in range(self.num_rows):
                line.append(chr(self.grid[x][y]))
            print("".join(line))

    def run(self) -> int:
        count = 1
        while self.step() != 0:
            count += 1
        return count


def thing1(filename: Path) -> int:
    return Grid(filename).run()

def test_part_1() -> None:
    assert thing1(Path("test1")) == 58

def main() -> None:
    subprocess.check_call([sys.executable, "-m", "mypy", sys.argv[0]])
    subprocess.check_call([sys.executable, "-m", "pytest", sys.argv[0]])

    answer = thing1(INPUT)
    print("part 1:", answer)


if __name__ == "__main__":
    main()


