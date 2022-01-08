YEAR = 2021
DAY = 20
PART = 3
 
from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os

INPUT = Path("input")


class T:
    def __init__(self, filename: Path):
        rows = []
        with open(filename, "rt") as fd:
            self.table = fd.readline().strip()
            fd.readline()
            for line in fd:
                rows.append(line.strip())

        self.image = dict()
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.everywhere = '.'
        for (y, r) in enumerate(rows):
            for (x, c) in enumerate(r):
                self.image[(x, y)] = c
                if c == '#':
                    self.x1 = max(self.x1, x)
                    self.y1 = max(self.y1, y)

    def collect3x3(self, x, y):
        v = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                v = v << 1
                if self.image.get((x + dx, y + dy), self.everywhere) == '#':
                    v |= 1
        return v

    def step(self):
        new_image = dict()
        m = 1
        nx0 = self.x0 - m
        ny0 = self.y0 - m
        nx1 = self.x1 + m
        ny1 = self.y1 + m
        va = self.collect3x3(self.x0 - 10, self.y0)

        for y in range(ny0, ny1 + 1):
            for x in range(nx0, nx1 + 1):
                v = self.collect3x3(x, y)
                c = self.table[v]
                new_image[(x, y)] = c

        self.everywhere = self.table[va]
        self.image = new_image
        self.x0 = nx0
        self.y0 = ny0
        self.x1 = nx1
        self.y1 = ny1

    def size(self):
        if self.everywhere == '#':
            return None
        else:
            return len([x for x in self.image.values() if x == '#'])

    def printout(self):
        for y in range(self.y0 - 1, self.y1 + 2):
            out = []
            for x in range(self.x0 - 1, self.x1 + 2):
                out.append(self.image.get((x, y), self.everywhere))

            out.append(" ")
            out.append(self.everywhere)
            print("".join(out))
        

def thing1(filename: Path) -> int:
    t = T(filename)
    t.step()
    t.step()
    return t.size()

def test_main() -> None:
    t = T(Path("test1"))
    t.printout()
    assert t.size() == 10
    t.step()
    t.printout()
    assert t.size() > 10
    t.step()
    t.printout()
    assert t.size() == 35
    assert thing1(Path("test1")) == 35
    t = T(INPUT)
    print(t.size())
    t.step()
    print(t.size())
    t.step()
    print(t.size())
    assert t.size() != 4897
    assert t.size() != 5919
    assert t.size() != 26322
    assert t.size() != 51691
    assert t.size() == 4873

    t = T(Path("test1"))
    for i in range(50):
        t.step()
    assert t.size() == 3351
    return 0

def thing2(filename: Path) -> int:
    t = T(filename)
    for i in range(50):
        t.step()
    return t.size()

def main() -> None:
    if not INPUT.exists():
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY), "download"])
        return

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

# The main cost of time was that almost all of the infinite space
# flips value on each step, in the real puzzle only.
#
# This was not obvious at first. I submitted a wrong answer.
#
# Seeing this, I thought I just needed to increase the margin (m) to better
# account for the edges; this was wrong, and led to 1 (maybe 2) more wrong
# answers.
#
# Then I tried to account for the problem with a hack, which was using
# a pixel from the new margin to represent everything else. This led
# to even more wrong answers (which looked plausible).
#
# I must have submitted 5 wrong answers before the 20 minute mark
# because I got a time penalty lasting until 25 minutes.
#
# At this point I took more time over it and added a special field
# to represent everywhere else. I got this to work with the test
# data and then got the right answer on the next attempt.
#

if __name__ == "__main__":
    main()


