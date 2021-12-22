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

class T2:
    def __init__(self, filename: Path, small):
        self.cmd = []
        for line in open(filename, "rt"):
            m = R.match(line)
            assert m, line
            self.cmd.append((m.group(1) == "on",
                    [int(x) for x in m.groups()[1:]]))

        self.total = 0

        if small:
            # clip to the starting area cube.
            new_cmd = []
            for j in range(len(self.cmd)):
                (on, cmd) = self.cmd[j]
                for i in range(0, 6, 2):
                    cmd[i+0] = min(UL + 1, max(cmd[i+0], LL))
                    cmd[i+1] = min(UL, max(cmd[i+1], LL - 1))

    def run(self):
        dimensionx = sorted(set([cmd[0] for (_, cmd) in self.cmd])
                    | set([cmd[1] + 1 for (_, cmd) in self.cmd]))
        dimensiony = sorted(set([cmd[2] for (_, cmd) in self.cmd])
                    | set([cmd[3] + 1 for (_, cmd) in self.cmd]))
        dimensionz = sorted(set([cmd[4] for (_, cmd) in self.cmd])
                    | set([cmd[5] + 1 for (_, cmd) in self.cmd]))
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

        self.total = 0
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

def xtest_part_2() -> None:
    assert thing2(Path("test1"), True) == 39
    assert thing2(Path("test2"), True) == 590784
    assert thing2(Path("test3"), True) == 474140
    assert thing2(Path("test3"), False) == 2758514936282235


# The above works but is very slow and required substantial CPU time.
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
# .... so I returned to the problem in an attempt to write up this better
# solution. It is fiddly to get it right. A simpler implementation uses
# a list of cuboids, but this is a bad idea, because many of them overlap,
# and so it is better to use a map. If a map is used, however, you must be
# mindful that the previous volume of a cuboid may be positive, negative or
# zero, because of repeatedly adding and removing elements. If it's zero,
# nothing needs to be cancelled. The complexity of the solution means I'm
# not sure I would have got it done in time even if I thought of it.

class T2A(T2):
    def run(self):
        self.cuboids = collections.defaultdict(lambda: 0)

        def get_volume(bounds):
            return (max(0, bounds[1] + 1 - bounds[0])
                    * max(0, bounds[3] + 1 - bounds[2])
                    * max(0, bounds[5] + 1 - bounds[4]))

        for (new_cuboid_is_on, new_cuboid_bounds) in self.cmd:
            # Remove the new cuboid from all existing cuboids
            new_cuboids = []
            for (old_cuboid_bounds, old_volume) in self.cuboids.items():
                clipped_bounds = new_cuboid_bounds[:]
                for i in range(0, 6, 2):
                    ul = old_cuboid_bounds[i+1] # upper limit for clip
                    ll = old_cuboid_bounds[i+0] # lower limit for clip
                    clipped_bounds[i+0] = min(ul + 1, max(clipped_bounds[i+0], ll))
                    clipped_bounds[i+1] = min(ul, max(clipped_bounds[i+1], ll - 1))

                volume = get_volume(clipped_bounds)
                assert volume >= 0
                if volume == 0 or old_volume == 0:
                    # If volume is zero they don't intersect
                    pass
                elif old_volume > 0:
                    # Existing cuboid has positive volume, so subtract volume
                    new_cuboids.append((clipped_bounds, -volume))
                else:
                    # Existing cuboid has negative volume, so add volume
                    new_cuboids.append((clipped_bounds, volume))

            # Add positive volume cuboids only
            volume = get_volume(new_cuboid_bounds)
            if new_cuboid_is_on and volume > 0:
                new_cuboids.append((new_cuboid_bounds, volume))

            # Update existing cuboids
            for (new_cuboid_bounds, volume) in new_cuboids:
                self.cuboids[tuple(new_cuboid_bounds)] += volume

        self.total = sum(self.cuboids.values())


def thing2a(filename: Path, small) -> int:
    t = T2A(filename, small)
    t.run()
    return t.count()

def test_part_2a() -> None:
    assert thing2a(Path("test1"), True) == 39
    assert thing2a(Path("test2"), True) == 590784
    assert thing2a(Path("test3"), True) == 474140
    assert thing2a(Path("test3"), False) == 2758514936282235

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

    answer = thing2a(INPUT, False)
    print("part 2:", answer)

    if PART == 2:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "2", str(answer)])
        return


if __name__ == "__main__":
    main()


