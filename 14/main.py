YEAR = 2021
DAY = 14
PART = 3
 
from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os

INPUT = Path("input")

Count = typing.Dict[str, int]

def factory() -> Count:
    return collections.defaultdict(lambda: 0)

class Puzzle:
    def __init__(self, filename: Path) -> None:
        with open(filename, "rt") as fd:
            self.original = fd.readline().strip()
            fd.readline()
            self.match: typing.Dict[str, str] = dict()
            for rule in fd:
                (pair, outcome) = rule.strip().split(" -> ")
                self.match[pair] = outcome

        self.single_count = factory()
        for i in range(len(self.original)):
            self.single_count[self.original[i]] += 1

        self.pair_count = factory()
        for i in range(len(self.original) - 1):
            self.pair_count[self.original[i:i+2]] += 1

    def step(self) -> None:
        # should have thought of this earlier...
        after = factory()
        before = self.pair_count
        for old_pair in before:
            if old_pair in self.match:
                new_pair_1 = old_pair[0] + self.match[old_pair]
                new_pair_2 = self.match[old_pair] + old_pair[1]
                self.single_count[self.match[old_pair]] += before[old_pair]
                after[new_pair_1] += before[old_pair]
                after[new_pair_2] += before[old_pair]
            else:
                after[old_pair] += before[old_pair]

        self.pair_count = after


def stepper(filename: Path, steps: int) -> int:
    p = Puzzle(filename)
    for i in range(steps):
        p.step()

    lc_mc = sorted(p.single_count.values())
    return lc_mc[-1] - lc_mc[0]

def test_part_1() -> None:
    assert stepper(Path("test_part_1"), 10) == 1588

def main() -> None:
    if not INPUT.exists():
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY), "download"])
        return

    subprocess.check_call([sys.executable, "-m", "mypy", sys.argv[0]])
    subprocess.check_call([sys.executable, "-m", "pytest", sys.argv[0]])

    answer = stepper(INPUT, 10)
    print("part 1:", answer)
    answer = stepper(INPUT, 40)
    print("part 2:", answer)

    if PART == 2:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "2", str(answer)])
        return


if __name__ == "__main__":
    main()


