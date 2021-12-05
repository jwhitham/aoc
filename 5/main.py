
from pathlib import Path
import unittest
import typing
import collections
import re


LINE_DESC = re.compile(r"^(\d+),(\d+) -> (\d+),(\d+)\s*$")

def linesweeper(filename: Path) -> int:
    crossing: typing.Dict[typing.Tuple[int, int], int] = collections.defaultdict(lambda: 0)
    for line in open(filename, "rt"):
        m = LINE_DESC.match(line)
        if m:
            x1 = int(m.group(1))
            y1 = int(m.group(2))
            x2 = int(m.group(3))
            y2 = int(m.group(4))

            if x1 == x2:
                # vertical
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    crossing[(x1, y)] += 1
            elif y1 == y2:
                # horizontal
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    crossing[(x, y1)] += 1
            else:
                # line is not horizontal or vertical
                pass

    count = 0
    for ((x, y), value) in crossing.items():
        if value >= 2:
            count += 1

    return count

def test_linesweeper_1() -> None:
    assert linesweeper(Path("part1test.txt")) == 5

def main() -> None:
    print("part 1:", linesweeper(Path("part1.txt")))

if __name__ == "__main__":
    main()


