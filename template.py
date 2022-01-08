YEAR = 2019
DAY = 1
PART = 3
 
from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os

INPUT = Path("input")

def thing1(filename: Path) -> int:
    return 0

def test_part_1() -> None:
    assert thing1(Path("test1")) == 1

def thing2(filename: Path) -> int:
    return 0

def test_part_2() -> None:
    assert thing2(Path("test2")) == 1

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


