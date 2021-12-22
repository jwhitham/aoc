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

# part 1 solution - very simple.
# I can't think of much potential for time saving here,
# limitation was understanding the instructions, typing speed
# and copying the test cases. Nevertheless it took me 9 minutes
# to write, which is not a good time.
#
# Small speed ups: the notorious "ints" function
# i.e. 're.findall(r"-?\d+", <line>)' might have been a slight
# speed up versus writing a new regular expression even though
# this was mostly copy/paste. An initial test run failed due
# to failing to correctly interpret the "off" case.

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

def thing1(filename: Path) -> int:
    t = T(filename)
    t.run()
    return t.count()

def test_part_1() -> None:
    assert thing1(Path("test1")) == 39
    assert thing1(Path("test2")) == 590784
    assert thing1(Path("test3")) == 474140

# part 2 initial solution
# Horrible.
# When I saw this, I thought of two directions to take, which were:
# 1. group ("discretise"?) coordinates in each of the 3 dimensions,
#    and calculate the volume of each group, knowing that none of
#    the groups can be subdivided. The space consists of a large number
#    of cuboid shapes, some of which are "on".
# 2. generate a 3D binary space partition tree and walk across the
#    leaf nodes of this tree to determine the "on" volume.
#
# I decided that 2 was completely impractical to write in the
# available time, though it would be fast. I didn't think of any
# other solutions. I thought that 1 would be good enough since
# there would be O(N^3) groups for N lines of input.
#
# I think I would have got away with 1 if I were working in a
# compile-to-machine-code language, but as it is, there were
# 590578800 cuboids. This was more than I expected.
# I also made the following mistakes.
#
# 1. Bisecting to convert coordinates to groups. It is so easy
#    to get an off-by-one error with bisect; I know this from experience,
#    and I was looking out for it, but still... There were a few
#    errors of that sort, caught by testing.
# 2. I needed to use X2+1, Y2+1, Z2+1 rather than X2, Y2, Z2 because
#    the ranges are inclusive. The first example (answer 39) doesn't
#    require this but the others do.
# 3. Trying to make the code generalise to support the small problems
#    from part 1. I did not make this work at the time, but I really
#    wanted to, because I hoped it would help me to debug bad results
#    in the large problem (which were bisecting/off-by-one errors).
# 4. How to remember the state of up to 5.9e8 Boolean elements in Python?
#    I'm using a 32-bit Python interpreter, oh dear... A set? No. 
#    A list of list of lists? No - crashes when initialising.
#    The overhead of pointers, reference counts etc. must be a problem.
#    The array module? No - can't create a 3D array that initially
#    contains many zeroes. (Or apparently even a 1D array that's
#    initially zero?) A file, then? Yes, but that's slow, presumably
#    because of the system call overhead. NumPy? Ah, yes, I can use
#    numpy.zeros to make the array. But it's still very slow...
#    because there are 5.9e8 and I need to iterate over all of them.
# 5. I don't need to iterate over all of them. I could have tracked
#    the total volume as the cuboids were turned on and off. (Actually
#    this is probably not a major help.)
# 
# The result works but is very slow and required substantial CPU time.
# I was looking for better options while it ran. But I did not think of:
#
# 1. keep a dict of known cuboids while reading the input:
#     (x1, y1, z1, x2, y2, z2): volume
# 2. when a new cuboid is added, intersect with all existing cuboids
#    and create additional cuboids which subtract the intersecting volume
#    i.e. have negative volume
# 3. if "on", add the new cuboid as a positive volume
# 4. Sum the values of the dict to get the total volume
#
# which I'm not sure I would have thought of, even if I had realised
# that the "discretise" solution would be too slow. Maybe with a break
# from the problem.
#    

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
        gridx = [0 for i in dimensionx]
        gridy = [0 for i in dimensiony]

        data = numpy.zeros([len(dimensionx),
                len(dimensiony),
                len(dimensionz)], dtype=numpy.int8)


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
            assert dimensionx[x2] == cmd[1] + 1
            assert dimensiony[y2] == cmd[3] + 1
            assert dimensionz[z2] == cmd[5] + 1
            assert dimensionx[x1] == cmd[0]
            assert dimensiony[y1] == cmd[2]
            assert dimensionz[z1] == cmd[4]
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


