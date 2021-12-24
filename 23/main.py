YEAR = 2021
DAY = 23
PART = 3
 
from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os
import re

INPUT = Path("input")
INPUT2 = Path("input2")

IMPOSSIBLE = 1 << 31
BLANK = """#############
#           #
### # # # ###
  # # # # #
  #########"""
DEST = { "A": 2, "B": 4, "C": 6, "D": 8 }
COST = { "A": 1, "B": 10, "C": 100, "D": 1000 }

class GameState:
    def __init__(self, memo, levels):
        self.start = {}
        self.moved = {}
        self.done = {}
        self.energy = 0
        self.record = []
        self.memo = memo
        self.occupied = dict()
        self.levels = levels

    def read(self, filename):
        with open(filename, "rt") as fd:
            fd.readline()
            fd.readline()
            r = re.compile(r"[A-D]")
            count = collections.defaultdict(lambda: 0)
            for j in range(self.levels):
                for (i, c) in enumerate(r.findall(fd.readline())):
                    count[c] += 1
                    (x, y) = ((i + 1) * 2, j + 1)
                    self.start[c + str(count[c])] = (x, y)
                    self.occupied[(x, y)] = c
        self.implicit_start_to_done()

    def implicit_start_to_done(self):
        # Anything already done? Move
        for j in range(self.levels):
            for key in sorted(self.start):
                (x, y) = self.start[key]
                c = key[0]
                if ((self.done.get(c, 0) == j)
                        and (y == (self.levels - j))
                        and (x == DEST[c])):
                    del self.occupied[self.start[key]]
                    self.occupied[(x, y)] = c
                    del self.start[key]
                    self.done[c] = self.done.get(c, 0) + 1

    def move_to_done(self):
        # Can anything move into the final state from the moved state?
        action = True
        while action:
            action = False
            for key in sorted(self.moved):
                c = key[0]
                (x1, y1) = self.moved[key]
                x2 = DEST[c]
                y2 = self.levels - self.done.get(c, 0)
                steps = self.check_path((x1, y1), (x2, y2), key)
                if steps > 0:
                    # Immediately move this
                    del self.occupied[self.moved[key]]
                    self.occupied[(x2, y2)] = c
                    del self.moved[key]
                    self.done[c] = self.done.get(c, 0) + 1
                    self.energy += steps * COST[c]
                    #self.record.append("move {} to ({}, {}) - steps {} cost {}".format(
                    #        key, x2, y2, steps, steps * COST[c]))
                    action = True

    def what_can_move(self):
        # List of available moves
        for key in sorted(self.start):
            (x1, y1) = self.start[key]
            assert y1 >= 1
            # non-terminal moves
            for x2 in [0, 1, 3, 5, 7, 9, 10]:
                steps = self.check_path((x1, y1), (x2, 0), key)
                if steps > 0:
                    yield (key, x2)
            # finishing move?
            c = key[0]
            x2 = DEST[c]
            y2 = self.levels - self.done.get(c, 0)
            steps = self.check_path((x1, y1), (x2, 0), key)
            if steps > 0:
                steps = self.check_path((x2, 0), (x2, y2), key)
                if steps > 0:
                    yield (key, x2)

    def do_move(self, key, x2):
        g = GameState(self.memo, self.levels)
        g.start = dict(self.start)
        g.moved = dict(self.moved)
        g.done = dict(self.done)
        g.energy = self.energy
        g.occupied = dict(self.occupied)
        #g.record = self.record[:]

        (x1, y1) = self.start[key]
        steps = self.check_path((x1, y1), (x2, 0), key)
        assert steps > 0
        c = key[0]
        del g.occupied[g.start[key]]
        g.occupied[(x2, 0)] = c
        del g.start[key]
        #g.record.append("move {} to ({}, 0) - steps {} cost {}".format(
        #        key, x2, steps, steps * COST[c]))
        g.moved[key] = (x2, 0)
        g.energy += steps * COST[c]
        g.move_to_done()
        return g

    def state(self):
        return (tuple(self.occupied.items()))

    def search(self):
        if len(self.start) == 0 and len(self.moved) == 0:
            # Finished!
            return (self.energy, self.record)
       
        s = self.state()
        if s in self.memo:
            (best_total, best_record) = self.memo[s]
            return (self.energy + best_total,
                    self.record + best_record)

        best_total = IMPOSSIBLE
        best_record = []
        for (key, x2) in self.what_can_move():
            g = self.do_move(key, x2)
            (total, record) = g.search()
            total -= self.energy
            record = record[len(self.record):]
            if total < best_total:
                best_total = total
                best_record = record

        self.memo[s] = (best_total, best_record)
        return (self.energy + best_total,
                self.record + best_record)

    def check_path(self, pos1, pos2, key):
        (x1, y1) = pos1
        (x2, y2) = pos2
        assert y1 == 0 or y2 == 0

        # Path must be clear from x1..x2 at y == 0
        xmin = min(x1, x2)
        xmax = max(x1, x2)
        for x in range(xmin, xmax + 1):
            if (x, 0) in self.occupied:
                if x != x1:
                    return -1 # blocked in corridor

        # calculate steps
        steps = (xmax - xmin) + abs(y2 - y1)

        # Path must be clear from y1..y2 at x == room
        if y2 >= 1:
            xroom = x2
            yroom = y2
        else:
            assert y1 >= 1
            xroom = x1
            yroom = y1

        c = key[0]
        for y in range(1, yroom + 1):
            if self.occupied.get((xroom, y), c) != c:
                return -1 # blocked by something at the entrance

        return steps

    def draw(self):
        print("start = {}".format(self.start))
        print("moved = {}".format(self.moved))
        print("done = {}".format(self.done))
        rows = [list(row) for row in BLANK.split("\n")]
        for i in range(self.levels - 2):
            rows.insert(3, rows[3][:])
        for (k, (x, y)) in self.moved.items():
            assert y == 0
            rows[y + 1][x + 1] = k[0]
        for (k, (x, y)) in self.start.items():
            assert y > 0
            rows[y + 1][x + 1] = k[0]
        for (k, v) in self.done.items():
            for i in range(v):
                rows[self.levels + 1 - i][DEST[k] + 1] = k[0]

        for row in rows:
            print("".join(row))
        print("")



def read(filename: Path, levels: int) -> GameState:
    g = GameState({}, levels)
    g.read(filename)
    return g


def test_part_1() -> int:
    g = read(Path("test1"), 2)
    assert g.done["C"] == 1
    #g.draw()

    # One Bronze amphipod moves into the hallway,
    # taking 4 steps and using 40 energy:
    assert g.start["B2"] == (6, 1)
    assert ("B2", 3) in g.what_can_move()
    g = g.do_move("B2", 3)
    assert g.energy == 40
    assert "B2" not in g.start
    assert g.moved["B2"] == (3, 0)
    #g.draw()

    # The only Copper amphipod not in its side room moves there,
    # taking 4 steps and using 400 energy:
    assert g.start["C1"] == (4, 1)
    assert ("C1", 6) in g.what_can_move()
    g = g.do_move("C1", 6)
    assert g.energy == 440, g.energy
    assert "C1" not in g.start
    assert "C1" not in g.moved
    assert g.done["C"] == 2
    #g.draw()

    # A Desert amphipod moves out of the way, taking 3 steps
    # and using 3000 energy, and then the Bronze amphipod
    # takes its place, taking 3 steps and using 30 energy:
    assert g.start["D2"] == (4, 2)
    assert ("D2", 5) in g.what_can_move()
    g = g.do_move("D2", 5)
    #g.draw()
    assert g.energy == 3470, g.energy
    assert "B2" not in g.start
    assert "B2" not in g.moved
    assert g.done["B"] == 1

    # The leftmost Bronze amphipod moves to its room using 40 energy:
    assert g.start["B1"] == (2, 1)
    assert ("B1", 4) in g.what_can_move()
    g = g.do_move("B1", 4)
    #g.draw()
    assert g.energy == 3510, g.energy
    assert "B1" not in g.start
    assert "B1" not in g.moved
    assert g.done["B"] == 2

    # Both amphipods in the rightmost room move into the hallway,
    # using 2003 energy in total. Both Desert amphipods move into
    # the rightmost room using 7000 energy.
    # Finally, the last Amber amphipod moves into its room, using 8 energy:
    assert ("D1", 7) in g.what_can_move()
    g = g.do_move("D1", 7)
    assert ("A2", 9) in g.what_can_move()
    g = g.do_move("A2", 9)
    #g.draw()
    assert g.energy == 12521, g.energy
    assert len(g.start) == 0
    assert len(g.moved) == 0
    assert len(g.done) == 4
    assert g.done["A"] == 2
    assert g.done["B"] == 2
    assert g.done["C"] == 2
    assert g.done["D"] == 2
    #print("\n".join(g.record))

    g = read(Path("test1"), 2)
    assert ("B2", 3) in g.what_can_move()
    (best_total, best_record) = g.search()
    assert best_total == 12521

def thing1(filename: Path) -> int:
    g = read(filename, 2)
    (best_total, best_record) = g.search()
    return best_total

def test_part_1a() -> None:
    return thing1(INPUT) == 10526

def thing2(filename: Path) -> int:
    g = read(filename, 4)
    (best_total, best_record) = g.search()
    return best_total

def test_part_2() -> None:
    return thing2(Path("test2")) == 44169

def test_part_2a() -> None:
    return thing2(Path(INPUT2)) == 41284

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

    answer = thing2(INPUT2)
    print("part 2:", answer)

    if PART == 2:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "2", str(answer)])
        return


if __name__ == "__main__":
    main()


