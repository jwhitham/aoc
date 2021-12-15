YEAR = 2021
DAY = 15
PART = 3
 
from pathlib import Path
import unittest
import typing
import subprocess
import sys
import heapq
import os

INPUT = Path("input")

class Cell:
    def __init__(self, x: int, y: int, risk: int) -> None:
        self.x = x
        self.y = y
        self.risk_here = risk
        self.best_risk = 1 << 31

    def __lt__(self, other) -> None:
        return self.best_risk < other.best_risk

class Map:
    def __init__(self, filename: Path) -> None:
        self.cells: typing.List[typing.List[Cell]] = []
        for (y, line) in enumerate(open(filename, "rt")):
            row: typing.List[Cell] = []
            self.cells.append(row)
            for (x, col) in enumerate(line.strip()):
                row.append(Cell(x, y, int(col)))

        self.rows = len(self.cells)
        self.cols = len(self.cells[0])

    def get(self, x: int, y: int) -> typing.Optional[Cell]:
        if (0 <= x < self.cols) and (0 <= y < self.rows):
            return self.cells[y][x]
        else:
            return None

    def shortest_path(self) -> int:
        start = self.get(0, 0)
        end = self.get(self.cols - 1, self.rows - 1)
        assert start
        assert end
        start.best_risk = 0

        todo: typing.List[Cell] = []
        heapq.heappush(todo, start)

        while len(todo) != 0:
            now = heapq.heappop(todo)

            def evaluate(then: typing.Optional[Cell]) -> None:
                if not then:
                    return
                if then.best_risk <= (now.best_risk + then.risk_here):
                    return
                then.best_risk = now.best_risk + then.risk_here
                heapq.heappush(todo, then)

            evaluate(self.get(now.x - 1, now.y))
            evaluate(self.get(now.x + 1, now.y))
            evaluate(self.get(now.x, now.y - 1))
            evaluate(self.get(now.x, now.y + 1))

        return end.best_risk


def thing1(filename: Path) -> int:
    return Map(filename).shortest_path()

def test_part_1() -> None:
    assert thing1(Path("test1")) == 40

class Map2(Map):
    def __init__(self, filename: Path, mult: int) -> None:
        Map.__init__(self, filename)

        def modulo(risk: int) -> int:
            return ((risk - 1) % 9) + 1

        # Expand in X direction
        for y in range(self.rows):
            row = self.cells[y]
            for rx in range(1, mult):
                for x in range(self.cols):
                    risk = modulo(row[x].risk_here + rx)
                    row.append(Cell(x + (rx * self.cols), y, risk))

        self.cols *= mult

        # Expand in Y direction
        for ry in range(1, mult):
            for y in range(self.rows):
                old_row = self.cells[y]
                new_row: typing.List[Cell] = []
                for x in range(self.cols):
                    risk = modulo(old_row[x].risk_here + ry)
                    new_row.append(Cell(x, y + (ry * self.rows), risk))

                self.cells.append(new_row)

        self.rows *= mult


def thing2(filename: Path) -> int:
    return Map2(filename, 5).shortest_path()

def test_part_2() -> None:
    assert thing2(Path("test1")) == 315

def main() -> None:
    if not INPUT.exists():
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY), "download"])
        return

    subprocess.check_call([sys.executable, "-m", "mypy", sys.argv[0]])
    subprocess.check_call([sys.executable, "-m", "pytest", sys.argv[0]])

    answer = thing1(INPUT)
    print("part 1:", answer)

    if PART == 1:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "1", str(answer)])
        return

    answer = thing2(INPUT)
    print("part 2:", answer)

    if PART == 2:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "2", str(answer)])
        return


if __name__ == "__main__":
    main()


