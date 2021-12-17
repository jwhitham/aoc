YEAR = 2021
DAY = 17
PART = 2
 
from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os

INPUT = Path("input")


TargetArea = typing.Tuple[int, int, int, int]
Velocity = typing.Tuple[int, int]

def hit_or_miss(initial: Velocity, target: TargetArea) -> typing.Tuple[int, int]:
    assert target[0] < target[2]
    assert target[1] < target[3]
    x = 0
    y = 0
    (dx, dy) = initial
    max_y = 0

    while True:
        if (x > target[2]) and (dx >= 0):
            return (1, max_y)  # too far

        if (target[0] <= x) and (target[1] <= y <= target[3]):
            return (0, max_y)  # hit

        if ((y < target[1]) and (dy <= 0)) or ((x < 0) and (dx <= 0)):
            return (-1, max_y) # falls short
      
        x += dx
        y += dy
        max_y = max(max_y, y)
        dy -= 1
        if dx > 0:
            dx -= 1
        elif dx < 0:
            dx += 1


def test1() -> None:
    t = (20, -10, 30, -5)
    assert hit_or_miss((7, 2), t)[0] == 0
    assert hit_or_miss((6, 3), t) == (0, 6)
    assert hit_or_miss((9, 0), t) == (0, 0)
    assert hit_or_miss((17, -4), t)[0] == 1
    assert hit_or_miss((0, -4), t)[0] == -1
    assert how_high(t) == 45

def how_high(t: TargetArea) -> int:
    r = 2000
    best_y = 0
    for vx in range(1, r + 1):
        for vy in range(-r, r + 1):
            (hm, max_y) = hit_or_miss((vx, vy), t)
            if hm == 0:
                best_y = max(max_y, best_y)
    return best_y

def count(t: TargetArea) -> int:
    r = 2000
    count = 0
    for vx in range(1, r + 1):
        for vy in range(-r, r + 1):
            (hm, max_y) = hit_or_miss((vx, vy), t)
            if hm == 0:
                count += 1
    return count

def test2() -> None:
    t = (20, -10, 30, -5)
    assert count(t) == 112

def thing1(filename: Path) -> int:
    t = (102, -146, 157, -90)
    return how_high(t)

def thing2(filename: Path) -> int:
    t = (102, -146, 157, -90)
    return count(t)

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


