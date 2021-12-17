YEAR = 2021
DAY = 17
PART = 3
 
from pathlib import Path
import unittest
import typing
import subprocess
import sys
import os

TEST_INPUT = (20, -10, 30, -5)
INPUT = (102, -146, 157, -90)


TargetArea = typing.Tuple[int, int, int, int]
Velocity = typing.Tuple[int, int]

def sim_x(initial: int, target: TargetArea) -> bool:
    x = 0
    dx = initial
    xl: typing.List[int] = []

    while True:
        xl.append(x)

        if x > target[2]:
            return False # too far

        if target[0] <= x:
            return True  # hit

        if dx <= 0:
            return False # falls short
      
        x += dx
        if dx > 0:
            dx -= 1

def sim_y(initial: int, target: TargetArea) -> bool:
    y = 0
    dy = initial
    yl = []
    once = 0

    while True:
        yl.append(y)

        if target[1] <= y <= target[3]:
            return True

        if (y < target[1]) and (dy <= 0):
            return False
            return []

        y += dy
        dy -= 1

def sim_xy(initial: Velocity, target: TargetArea) -> typing.List[typing.Tuple[int, int]]:
    x = 0
    y = 0
    (dx, dy) = initial
    xyl: typing.List[typing.Tuple[int, int]] = []

    while True:
        xyl.append((x, y))

        if (target[0] <= x <= target[2]) and (target[1] <= y <= target[3]):
            return xyl  # hit

        if x > target[2]:
            return [] # too far

        if y < target[1]:
            return [] # too low

        x += dx
        if dx > 0:
            dx -= 1
        y += dy
        dy -= 1

def get_max_y(initial: Velocity, target: TargetArea) -> int:
    max_y = -1
    for (x, y) in sim_xy(initial, target):
        max_y = max(y, max_y)
        if (target[0] <= x <= target[2]) and (target[1] <= y <= target[3]):
            return max_y

    return -1

def test_get_max_y() -> None:
    t = TEST_INPUT
    assert get_max_y((7, 2), t) > 0
    assert get_max_y((6, 3), t) == 6
    assert get_max_y((9, 0), t) == 0
    assert get_max_y((17, -4), t) == -1
    assert get_max_y((0, -4), t) == -1

def get_x_maybe(target: TargetArea) -> typing.List[int]:
    x_maybe: typing.List[int] = []
    for vx in range(target[2] + 1):
        if sim_x(vx, target):
            x_maybe.append(vx)
    return x_maybe

def get_y_maybe(target: TargetArea) -> typing.List[int]:
    y_maybe: typing.List[int] = []
    vy = min(0, target[1])
    vmax = abs(vy)
    while vy <= vmax:
        if sim_y(vy, target):
            y_maybe.append(vy)
            vmax = max(abs(vy) + 1, vmax)

        vy += 1
    return y_maybe

def get_best_max_y(target: TargetArea) -> int:
    x_maybe = get_x_maybe(target)
    y_maybe = get_y_maybe(target)
    best_y = 0
    for vy in y_maybe:
        for vx in x_maybe:
            for (x, y) in sim_xy((vx, vy), target):
                best_y = max(y, best_y)

    return best_y

def test_get_best_max_y() -> None:
    t = TEST_INPUT
    assert get_max_y((6, 9), t) == 45
    assert get_best_max_y(t) == 45

def count(target: TargetArea) -> int:
    x_maybe = get_x_maybe(target)
    y_maybe = get_y_maybe(target)
    count = 0
    for vy in y_maybe:
        for vx in x_maybe:
            if get_max_y((vx, vy), target) >= 0:
                count += 1
    return count

def test_count() -> None:
    t = TEST_INPUT
    assert count(t) == 112

def main() -> None:
    subprocess.check_call([sys.executable, "-m", "mypy", sys.argv[0]])
    subprocess.check_call([sys.executable, "-m", "pytest", sys.argv[0]])

    answer = get_best_max_y(INPUT)
    print("part 1:", answer)

    if PART == 1:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "1", str(answer)])
        return

    answer = count(INPUT)
    print("part 2:", answer)

    if PART == 2:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "2", str(answer)])
        return

if __name__ == "__main__":
    main()


