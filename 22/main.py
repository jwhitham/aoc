YEAR = 2021
DAY = 22
PART = 3
 
from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os
import re
import bisect
import numpy

INPUT = Path("input")

R = re.compile(r"^(on|off) x=(-*\d+)[.][.](-*\d+),"
r"y=(-*\d+)[.][.](-*\d+),"
r"z=(-*\d+)[.][.](-*\d+)\s*$")
LL = -50
UL = 50

class T:
    def __init__(self, filename: Path):
        self.cmd = []
        for line in open(filename, "rt"):
            m = R.match(line)
            assert m, line
            self.cmd.append((m.group(1) == "on",
                    [int(x) for x in m.groups()[1:]]))

        self.cube = set()

    def run(self):
        for (on, cmd) in self.cmd:
            x1 = cmd[0]
            x2 = cmd[1]
            y1 = cmd[2]
            y2 = cmd[3]
            z1 = cmd[4]
            z2 = cmd[5]
            if (x2 < LL) or (y2 < LL) or (z2 < LL):
                continue
            if (x1 > UL) or (y1 > UL) or (z2 > UL):
                continue
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    for z in range(z1, z2 + 1):
                        if on:
                            self.cube.add((x, y, z))
                        else:
                            self.cube.discard((x, y, z))

    def count(self):
        return len(self.cube)

class T2:
    def __init__(self, filename: Path, small):
        self.cmd = []
        for line in open(filename, "rt"):
            m = R.match(line)
            assert m, line
            self.cmd.append((m.group(1) == "on",
                    [int(x) for x in m.groups()[1:]]))

        self.cube = set()
        self.total = 0
        self.small = small

    def run(self):
        small = self.small
        u = set([LL, UL, LL - 1, UL - 1])
        dimensionx = sorted(set([cmd[0] for (_, cmd) in self.cmd])
                    | u | set([cmd[1] + 1 for (_, cmd) in self.cmd]))
        dimensiony = sorted(set([cmd[2] for (_, cmd) in self.cmd])
                    | u | set([cmd[3] + 1 for (_, cmd) in self.cmd]))
        dimensionz = sorted(set([cmd[4] for (_, cmd) in self.cmd])
                    | u | set([cmd[5] + 1 for (_, cmd) in self.cmd]))
        dimensionx.append(dimensionx[-1] + 1)
        dimensiony.append(dimensiony[-1] + 1)
        dimensionz.append(dimensionz[-1] + 1)
        dimensionx.append(dimensionx[-1] + 1)
        dimensiony.append(dimensiony[-1] + 1)
        dimensionz.append(dimensionz[-1] + 1)
        #M = 100 ** 10
        #dimensionx.append(dimensionx[-1] + M)
        #dimensiony.append(dimensiony[-1] + M)
        #dimensionz.append(dimensionz[-1] + M)
        #print(dimensionx)
        #print(dimensiony)
        #print(dimensionz)
        print(len(dimensionx))
        print(len(dimensiony))
        print(len(dimensionz))
        gridx = [0 for i in dimensionx]
        gridy = [0 for i in dimensiony]

        data = numpy.zeros([len(dimensionx),
                len(dimensiony),
                len(dimensionz)], dtype=numpy.int8)
        """
        t = open("x.bin", "wb+")
        t.seek(len(dimensionx) * len(dimensiony) * len(dimensionz), 0)
        t.write(b"\x00")

        def index(x, y, z):
            return z + (y * len(dimensionz)) + (x * len(dimensiony) * len(dimensionz))

        def iset(x, y, z, on):
            t.seek(index(x, y, z))
            if on:
                t.write(b"\x01")
            else:
                t.write(b"\x00")
        def get(x, y, z):
            t.seek(index(x, y, z))
            return t.read(1) != b"\x00"
        """


        for (on, cmd) in self.cmd:
            if small:
                cmd = cmd[:]
                print("")
                print(cmd)
                for i in range(6):
                    cmd[i] = min(max(cmd[i], LL - 1), UL + 1)
                bad = False
                for i in range(3):
                    if (cmd[(i * 2) + 1] < LL) or (cmd[(i * 2)] > UL):
                        bad = True
                print(cmd, bad)
                if bad:
                    continue

            x1 = bisect.bisect_right(dimensionx, cmd[0] - 1)
            x2 = bisect.bisect(dimensionx, cmd[1])
            y1 = bisect.bisect_right(dimensiony, cmd[2] - 1)
            y2 = bisect.bisect(dimensiony, cmd[3])
            z1 = bisect.bisect_right(dimensionz, cmd[4] - 1)
            z2 = bisect.bisect(dimensionz, cmd[5])
            #print(dimensionx[x1], dimensiony[y1], dimensionz[z1])
            #print(dimensionx[x2], dimensiony[y2], dimensionz[z2])
            assert dimensionx[x2] == cmd[1] + 1
            assert dimensiony[y2] == cmd[3] + 1
            assert dimensionz[z2] == cmd[5] + 1
            assert dimensionx[x1] == cmd[0]
            assert dimensiony[y1] == cmd[2]
            assert dimensionz[z1] == cmd[4]
            #print(x1, y1, z1, x2, y2, z2)
            for x in range(x1, x2):
                for y in range(y1, y2):
                    for z in range(z1, z2):
                        if on and data[x, y, z] == 0:
                            data[x, y, z] = 1
                            gridx[x] += 1
                            gridy[y] += 1
                        elif data[x, y, z] == 1 and not on:
                            data[x, y, z] = 0
                            gridx[x] -= 1
                            gridy[y] -= 1

        for x in range(len(dimensionx) - 1):
            assert gridx[x] >= 0
            if gridx[x] == 0:
                continue
            for y in range(len(dimensiony) - 1):
                assert gridy[y] >= 0
                if gridy[y] == 0:
                    continue
                for z in range(len(dimensionz) - 1):
                    if data[x, y, z]:
                        volume = ((dimensionx[x + 1] - dimensionx[x])
                                * (dimensiony[y + 1] - dimensiony[y])
                                * (dimensionz[z + 1] - dimensionz[z]))
                        #print(volume)
                        #assert volume == 1
                        self.total += volume
        print(self.total)

    def count(self):
        return self.total


def thing1(filename: Path) -> int:
    t = T(filename)
    t.run()
    return t.count()

def test_part_1() -> None:
    assert thing1(Path("test1")) == 39
    assert thing1(Path("test2")) == 590784
    assert thing1(Path("test3")) == 474140

def thing2(filename: Path, small) -> int:
    t = T2(filename, small)
    t.run()
    return t.count()

def test_part_2() -> None:
    assert thing2(Path("test1"), True) == 39
    #assert thing2(Path("test2"), True) == 590784
    #assert thing2(Path("test2"), True) == 474140
    assert thing2(Path("test3"), False) == 2758514936282235

def xmain() -> None:
    assert thing2(Path("test1"), True) == 39
    #assert thing2(Path("test2"), True) == 590784
    #assert thing2(Path("test2"), True) == 474140
    assert thing2(Path("test3"), False) == 2758514936282235

def main() -> None:
    if not INPUT.exists():
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY), "download"])
        return

    #subprocess.check_call([sys.executable, "-m", "mypy", sys.argv[0]])
    subprocess.check_call([sys.executable, "-m", "pytest", sys.argv[0]])

    answer = thing1(INPUT)
    print("part 1:", answer)

    if PART == 1:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "1", str(answer)])
        return

    answer = thing2(INPUT, False)
    print("part 2:", answer)

    if PART == 2:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "2", str(answer)])
        return


if __name__ == "__main__":
    main()


