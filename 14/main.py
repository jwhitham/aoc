YEAR = 2021
DAY = 14
PART = 1
 
from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os

INPUT = Path("input")

def thing1(filename: Path) -> int:
    with open(filename, "rt") as fd:
        state = fd.readline().strip()
        fd.readline()
        match = dict()
        for rule in fd:
            (pair, outcome) = rule.strip().split(" -> ")
            match[pair] = outcome

        for step in range(10):
            next_state = []
            for i in range(len(state) - 1):
                pair = state[i:i+2]
                next_state.append(state[i])
                if pair in match:
                    next_state.append(match[pair])
            next_state.append(state[-1])
            state = ''.join(next_state)

        count: typing.Dict[str, int] = collections.defaultdict(lambda: 0)
        for elt in state:
            count[elt] += 1

        lc_mc = sorted(count.values())
        return lc_mc[-1] - lc_mc[0]

def test_part_1() -> None:
    assert thing1(Path("test_part_1")) == 1588

def thing2(filename: Path) -> int:
    return 0

"""
def test_part_2() -> None:
    assert thing2(Path("test2")) == 1
"""

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


