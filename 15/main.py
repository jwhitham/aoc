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
        self.cells = {}
        self.rows = self.cols = 0
        for (y, line) in enumerate(open(filename, "rt")):
            for (x, col) in enumerate(line.strip()):
                self.cells[(x, y)] = Cell(x, y, int(col))
                self.cols = max(x + 1, self.cols)
            self.rows = y + 1

    def shortest_path(self) -> int:
        start = self.cells[(0, 0)]
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

            evaluate(self.cells.get((now.x - 1, now.y), None))
            evaluate(self.cells.get((now.x, now.y - 1), None))
            evaluate(self.cells.get((now.x + 1, now.y), None))
            evaluate(self.cells.get((now.x, now.y + 1), None))

        return self.cells[(self.cols - 1, self.rows - 1)].best_risk


def thing1(filename: Path) -> int:
    return Map(filename).shortest_path()

def test_part_1() -> None:
    assert thing1(Path("test1")) == 40

class Map2(Map):
    def __init__(self, filename: Path, mult: int) -> None:
        Map.__init__(self, filename)
        for y in range(self.rows):
            for x in range(self.cols):
                for ry in range(mult):
                    ty = (ry * self.rows) + y
                    for rx in range(mult):
                        tx = (rx * self.cols) + x
                        risk = self.cells[(x, y)].risk_here
                        risk += rx + ry
                        risk -= 1
                        risk %= 9
                        risk += 1
                        self.cells[(tx, ty)] = Cell(tx, ty, risk)

        self.rows = self.rows * mult
        self.cols = self.cols * mult

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


