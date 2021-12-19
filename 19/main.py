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
        assert 0 <= axis <= 2
        axis2 = (axis + 1) % 3
        for i in range(len(self.sees)):
            a = self.sees[i][axis]
            b = self.sees[i][axis2]
            (a, b) = (b, -a)
            self.sees[i][axis] = a
            self.sees[i][axis2] = b

    def try_match_rot(self, other):
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

    # try to find any match
    v = scanners[0].try_match(scanners[0])
    assert v == [0, 0, 0], v

    s1 = scanners[0]
    s1.rel_pos = [0, 0, 0]
    """
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
    """

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
                    continue

                v = s2.try_match_rot(s1)
                if v is not None:
                    s2.rel_pos = [a + b for (a, b) in zip(s1.rel_pos, v)]
                    unmatched = True

    for s1 in scanners:
        assert s1.rel_pos is not None
        print(s1.number, s1.rel_pos)

    all_beacons = set()
    for s1 in scanners:
        for v in s1.sees:
            bpos = [b - a for (a, b) in zip(s1.rel_pos, v)]
            all_beacons.add(tuple(bpos))

    mh = 0
    for s1 in scanners:
        for s2 in scanners:
            mh = max(mh, sum([abs(b - a) for (a, b) in zip(s1.rel_pos, s2.rel_pos)]))

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


