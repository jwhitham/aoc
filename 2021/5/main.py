
from pathlib import Path
import unittest
import typing
import collections
import re


LINE_DESC = re.compile(r"^(\d+),(\d+) -> (\d+),(\d+)\s*$")

def linesweeper(filename: Path, only_vertical: bool) -> int:
    crossing: typing.Dict[typing.Tuple[int, int], int] = collections.defaultdict(lambda: 0)
    for line in open(filename, "rt"):
        m = LINE_DESC.match(line)
        if not m:
            continue

        x1 = int(m.group(1))
        y1 = int(m.group(2))
        x2 = int(m.group(3))
        y2 = int(m.group(4))
        dx = x2 - x1
        dy = y2 - y1
        if (dx != 0) and (dy != 0) and only_vertical:
            # Only considering vertical or horizontal lines for part 1 and this is diagnoal
            continue

        # Lines are always vertical, horizontal, or at a 45 degree diagonal
        # so there is no need to detect intersections at arbitrary angles (potentially
        # tricky to do efficiently, avoiding N^2 comparisons). And there is also no
        # question of exactly how to deal with situations where a line partially but
        # not entirely intersects a map square. This is a rather helpful restriction.
        # Iterate from x1,y1 to x2,y2
        length = max(abs(dx), abs(dy))
        x = x1
        y = y1
        for i in range(length + 1):
            crossing[(x, y)] += 1
            x += (1 if dx > 0 else (-1 if dx < 0 else 0))
            y += (1 if dy > 0 else (-1 if dy < 0 else 0))

    count = 0
    for ((x, y), value) in crossing.items():
        if value >= 2:
            count += 1

    return count

def test_linesweeper_1() -> None:
    assert linesweeper(Path("part1test.txt"), True) == 5

def test_linesweeper_2() -> None:
    assert linesweeper(Path("part1test.txt"), False) == 12

def main() -> None:
    print("part 1:", linesweeper(Path("part1.txt"), True))
    print("part 2:", linesweeper(Path("part1.txt"), False))

if __name__ == "__main__":
    main()


