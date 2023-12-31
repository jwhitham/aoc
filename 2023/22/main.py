

import typing
import heapq
import re
import sys

Position = typing.Tuple[int, int, int]
Occupied = typing.Dict[Position, "Brick"]
SupportGraph = typing.Dict["Brick", typing.Set["Brick"]]

RE_BRICK = re.compile(r"^(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)\s*$")

class Brick:
    def __init__(self, name: str, text: str) -> None:
        self.name = name
        m = RE_BRICK.match(text)
        assert m is not None
        (self.x1, self.y1, self.z1,
            self.x2, self.y2, self.z2) = [int(v) for v in m.groups()]
        assert self.x1 <= self.x2
        assert self.y1 <= self.y2
        assert self.z1 <= self.z2
        assert 0 <= self.z1

    def positions(self) -> typing.Iterator[Position]:
        for z in range(self.z1, self.z2 + 1):
            for y in range(self.y1, self.y2 + 1):
                for x in range(self.x1, self.x2 + 1):
                    yield (x, y, z)

    def fall(self) -> None:
        self.z1 -= 1
        self.z2 -= 1
        assert self.z1 <= self.z2
        assert 0 <= self.z1

    def supports(self, occupied: Occupied) -> typing.Set["Brick"]:
        s: typing.Set[Brick] = set()
        for y in range(self.y1, self.y2 + 1):
            for x in range(self.x1, self.x2 + 1):
                b = occupied.get((x, y, self.z2 + 1), None)
                if b is not None:
                    s.add(b)
        return s

    def is_supported(self, occupied: Occupied) -> bool:
        if self.z1 == 0:
            return True

        for y in range(self.y1, self.y2 + 1):
            for x in range(self.x1, self.x2 + 1):
                b = occupied.get((x, y, self.z1 - 1), None)
                if b is not None:
                    return True
        return False
        
class Problem:
    def __init__(self, fname: str) -> None:
        self.bricks: typing.List[Brick] = []
        self.occupied: Occupied = {}
        self.x2 = self.y2 = self.z2 = -1
        self.x1 = self.y1 = sys.maxsize
        self.z1 = 0
        with open(fname, "rt") as fd:
            for (i, line) in enumerate(fd):
                b = Brick(chr(i + ord("A")) if i < 26 else str(i), line)
                self.bricks.append(b)
                self.add_brick(b)
                self.x1 = min(self.x1, b.x1)
                self.y1 = min(self.y1, b.y1)
                self.x2 = max(self.x2, b.x2)
                self.y2 = max(self.y2, b.y2)
                self.z2 = max(self.z2, b.z2)

    def add_brick(self, b: Brick) -> None:
        for p in b.positions():
            assert p not in self.occupied
            self.occupied[p] = b

    def remove_brick(self, b: Brick) -> None:
        for p in b.positions():
            assert p in self.occupied
            del self.occupied[p]

    def fall(self) -> None:
        fell = True
        while fell:
            fell = False
            for b in self.bricks:
                while not b.is_supported(self.occupied):
                    self.remove_brick(b)
                    b.fall()
                    self.add_brick(b)
                    fell = True
                
    def make_support_graph(self) -> typing.Tuple[SupportGraph, SupportGraph]:
        supported_by: SupportGraph = {}
        supports: SupportGraph = {}

        for b1 in self.bricks:
            supports[b1] = b1.supports(self.occupied)

        for b1 in self.bricks:
            supported_by[b1] = set()

        for b1 in self.bricks:
            for b2 in supports[b1]:
                supported_by[b2].add(b1)

        return (supports, supported_by)

    def part1(self) -> int:
        self.fall()
        (supports, supported_by) = self.make_support_graph()
        total = 0
        for b1 in self.bricks:
            all_have_multi_support = True
            for b2 in supports[b1]:
                b2_has_multi_support = False
                for b3 in supported_by[b2]:
                    if b3 != b1:
                        b2_has_multi_support = True
                        break
                if not b2_has_multi_support:
                    all_have_multi_support = False
            if all_have_multi_support:
                total += 1

        return total

    def part2(self) -> int:
        self.fall()
        (supports, supported_by) = self.make_support_graph()
        moved: typing.Set[Brick] = set()
        total = 0
        
        def add_all_moved(b1: Brick) -> None:
            if len(supported_by[b1] - moved) == 0:
                # No longer supported
                moved.add(b1)
                for b2 in supports[b1]:
                    add_all_moved(b2)

        for b1 in self.bricks:
            moved.clear()
            old_size = len(moved)
            moved.add(b1)
            while len(moved) != old_size:
                old_size = len(moved)
                for b2 in supports[b1]:
                    add_all_moved(b2)

            total += len(moved) - 1

        return total

    def dump(self) -> None:
        print(" x ")
        for z in range(self.z2, self.z1 - 1, -1):
            for x in range(self.x1, self.x2 + 1):
                found: typing.Set["Brick"] = set()
                for y in range(self.y1, self.y2 + 1):
                    b = self.occupied.get((x, y, z), None)
                    if b is not None:
                        found.add(b)
                if len(found) == 0:
                    print(".", end="")
                elif len(found) == 1:
                    print(list(found)[0].name, end="")
                else:
                    print("?", end="")
            print("")


        for b in self.bricks:
            s = " and ".join([b2.name for b2 in b.supports(self.occupied)])
            if s == "":
                s = "nothing"
            print(f"Brick {b.name} supports {s}")

def main():
    assert Problem("test").part1() == 5
    print(Problem("input").part1())
    assert Problem("test").part2() == 7
    print(Problem("input").part2())


if __name__ == "__main__":
    main()
