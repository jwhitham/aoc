YEAR = 2021
DAY = 19
PART = 3
 
from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os

INPUT = Path("input")


def gen_vec():
    # Lost some time here due to initially thinking I might not need
    # true rotation and it would be ok to flip on the X/Y/Z axes,
    # which is not true.
    l = []
    for z in [-1, 1]:
        for y in [-1, 1]:
            for x in [-1, 1]:
                l.append([x, y, z])
    return l

VECS = gen_vec()
THRES = 3

class Scanner:
    def __init__(self, number: int) -> None:
        self.number = number
        self.sees = []
        self.rel_pos = None

    def try_match(self, other):
        # Lost some time here due to confusion about the loop structure
        # needed to figure out whether the two lists of beacons actually
        # match or not.
        #
        # The basic idea, unchanged since the beginning, is to compute
        # "t", the vector between "self" and "other" when a pair (a, b)
        # actually represents the same beacon.
        #
        # There are "self.sees" * "other.sees" possible vectors and most
        # won't match because the beacons are different. But you don't
        # know if a vector is valid on the first time you see it. Initially
        # my code wrongly accepted the first vector as valid and then
        # tried to match others against it, which would only have worked
        # if the first pair from "self.sees" * "other.sees" happened
        # to be the same beacon (quite unlikely).
        #
        # I also wrongly used 1000 as the longest allowable distance
        # for a time (misunderstanding the problem).
        #
        # Could have made progress faster here by checking that each
        # Scanner object matches itself, and also using test cases.
        # My computation of "t" is also the wrong way round.
        matching = 0
        maybe = collections.defaultdict(lambda: 0)
        for a in self.sees:
            for b in other.sees:
                t = [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
                max_t = max([abs(q) for q in t])
                if max_t > 2000:
                    continue # not valid
                else:
                    maybe[tuple(t)] += 1

        # Actually it's enough to exit the function when one of
        # the values of "maybe" has gone above THRES.
        v = sorted(maybe.values())
        if len(v) == 0:
            return None

        best = v.pop()
        if best >= THRES:
            for k in maybe:
                if maybe[k] == best:
                    return list(k)
        else:
            return None

    def rotate(self, axis: int) -> None:
        # I knew it was hard to write a correct rotate function
        # so I unit-tested this.
        assert 0 <= axis <= 2
        axis2 = (axis + 1) % 3
        for i in range(len(self.sees)):
            a = self.sees[i][axis]
            b = self.sees[i][axis2]
            (a, b) = (b, -a)
            self.sees[i][axis] = a
            self.sees[i][axis2] = b

    def try_match_rot(self, other):
        # I know that this rotates the vectors up to 64 times
        # and some of these rotations are equivalent so it's wasteful.
        # In fact there are only 24 unique rotations. But I don't know
        # a general way to find them and be sure I didn't miss one
        # (though I could hash the state of self.sees...).
        #
        # Lost some time by initially rotating the vectors back
        # into their original state, which is not useful, because
        # the resulting vector then doesn't match the rotation.
        for i in range(4):
            self.rotate(0)
            for j in range(4):
                self.rotate(1)
                for k in range(4):
                    self.rotate(2)
                    v = self.try_match(other)
                    if v is not None:
                        return v


                    #if vb is None:
                    #    v = self.try_match(other)
                    #    if v is not None:
                    #        vb = v

        return None

def test_rotate() -> None:
    s = Scanner(0)
    s.sees.append([-4, -1, 1])
    s.rotate(0)
    assert s.sees[0] == ([-1, 4, 1])
    s.rotate(0)
    assert s.sees[0] == ([4, 1, 1])
    s.rotate(0)
    assert s.sees[0] == ([1, -4, 1])

def thing1(filename: Path) -> int:
    scanners = []
    for line in open(filename, "rt"):
        line = line.strip()
        if line.startswith("--"):
            # Lost some time here because startswith("-") matches "-123"...
            fields = line.split()
            fields.pop()
            scanner = Scanner(int(fields.pop()))
            scanners.append(scanner)
        elif line != "":
            coords = line.split(",")
            x = int(coords[0])
            y = int(coords[1])
            z = int(coords[2])
            scanner.sees.append([x, y, z])

    # This sanity check should have existed from the beginning.
    v = scanners[0].try_match(scanners[0])
    assert v == [0, 0, 0], v

    s1 = scanners[0]
    s1.rel_pos = [0, 0, 0]
    # Lost some time by skipping this initially and moving to
    # try to calculate all scanner locations in a loop.
    #
    # Initially writing these tests for try_match_rot would have saved some
    # time with all the bugs I had in it. When I did write them I found
    # each produced the negation of the vector in the worked example,
    # which I considered equivalent at the time, being due to different
    # rotation code.
    if filename.name == "test1":
        s2 = scanners[1]
        v = s2.try_match_rot(s1)
        assert v == [-68, 1246, 43], v
        save = v
        s2 = scanners[4]
        v = s2.try_match_rot(s1)
        assert v == [20, 1133, -1061], v
        s2 = scanners[2]
        v = s2.try_match_rot(s1)
        assert v == [-1105, 1205, -1229], v
        s1 = scanners[1]
        s2 = scanners[3]
        v = s2.try_match_rot(s1)
        v = [a + b for (a, b) in zip(save, v)]
        assert v == [92,2380,20], v

    # This part seemed straightforward, though it was here that I
    # really hit bugs in try_match_rot and began to backtrack.
    s1 = scanners[0]
    unmatched = True
    while unmatched:
        unmatched = False
        for s1 in scanners:
            if s1.rel_pos is None:
                continue

            for s2 in scanners:
                if s1 == s2:
                    continue
                if s2.rel_pos is not None:
                    # Lost time here by forgetting to do this check
                    # (infinite loop).
                    continue

                v = s2.try_match_rot(s1)
                if v is not None:
                    s2.rel_pos = [a + b for (a, b) in zip(s1.rel_pos, v)]
                    unmatched = True

    for s1 in scanners:
        assert s1.rel_pos is not None
        print(s1.number, s1.rel_pos)

    # I seemed to be on track again when I wrote this...
    all_beacons = set()
    for s1 in scanners:
        for v in s1.sees:
            # Lost time here because I couldn't understand why a + b
            # wasn't the correct way to compute the beacon location.
            # Turned out that this is due to the wrong subtraction
            # being used to produce the "t" vector in "try_match".
            # I'm doing self - other, should be doing other - self.
            # This is also why the test values above are all negative.

            bpos = [b - a for (a, b) in zip(s1.rel_pos, v)]
            all_beacons.add(tuple(bpos))

    # Working out the Manhattan distance seemed an easy extension.
    # Still lost time due to forgetting abs, which is ok on the test
    # input (ho ho ho) but not on the real input, so a 60 second penalty
    # for submitting the wrong answer.
    mh = 0
    for s1 in scanners:
        for s2 in scanners:
            mh = max(mh, sum([abs(b - a) for (a, b) in zip(s1.rel_pos, s2.rel_pos)]))

    # Curiously some other people solving this puzzle seemed to find
    # the second part required a lot of rework. They must have done
    # it in some other way, which didn't give them the scanner positions.
    # What was this...?

    return (len(all_beacons), mh)

def test_thing1() -> int:
    assert thing1(Path("test1")) == (79, 3621)

#def test_part_2() -> None:
#    assert thing2(Path("test2")) == 1

def main() -> None:
    if not INPUT.exists():
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY), "download"])
        return

    #subprocess.check_call([sys.executable, "-m", "mypy", sys.argv[0]])
    subprocess.check_call([sys.executable, "-m", "pytest", sys.argv[0]])

    (answer, mh) = thing1(INPUT)
    print("part 1:", answer)

    if PART == 1:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "1", str(answer)])
        return

    answer = mh
    print("part 2:", answer)

    if PART == 2:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "2", str(answer)])
        return


if __name__ == "__main__":
    main()


