YEAR = 2019
DAY = 1
PART = 0
 
from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os

def calc(val: int) -> int:
    return (val // 3) - 2
    return 0

def thing1(filename: Path) -> int:
    total = 0
    for line in open(filename, "rt"):
        total += calc(int(line.strip()))
    return total

def test_part_1() -> None:
    assert calc(12) == 2
    assert calc(14) == 2
    assert calc(1969) == 654
    assert calc(100756) == 33583

def calc2(initial_mass: int) -> int:
    fuel_mass = calc(initial_mass)
    more = calc(fuel_mass)
    while more > 0:
        fuel_mass += more
        more = calc(more)
    
    return fuel_mass

def thing2(filename: Path) -> int:
    total = 0
    for line in open(filename, "rt"):
        total += calc2(int(line.strip()))
    return total

def test_part_2() -> None:
    assert calc2(14) == 2
    assert calc2(1969) == 966
    assert calc2(100756) == 50346

def main() -> None:
    if not os.path.isfile("input"):
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY), "download"])
        return

    subprocess.check_call([sys.executable, "-m", "mypy", sys.argv[0]])
    subprocess.check_call([sys.executable, "-m", "pytest", sys.argv[0]])

    answer = thing1(Path("input"))
    print("part 1:", answer)

    if PART == 1:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "1", str(answer)])
        return

    answer = thing2(Path("input"))
    print("part 2:", answer)

    if PART == 2:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "2", str(answer)])
        return


if __name__ == "__main__":
    main()


