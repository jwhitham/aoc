
from pathlib import Path
import unittest
import typing

XY = typing.Tuple[int, int]
FLASH = 10

class Octopus:
    def __init__(self, xy: XY, energy: int) -> None:
        (self.x, self.y) = xy
        self.energy = energy
        self.flashed = False

class Sea:
    def __init__(self, initial_state: Path) -> None:
        self.matrix: typing.Dict[XY, Octopus] = {}
        self.rows = self.cols = 0
        for (y, line) in enumerate(open(initial_state, "rt")):
            for (x, ch) in enumerate(line.strip()):
                self.matrix[(x, y)] = Octopus((x, y), int(ch))
                self.cols = max(x + 1, self.cols)
            self.rows = max(y + 1, self.rows)
        self.flash_count = 0
        self.fleet = self.matrix.values()

    def steps(self, count: int) -> None:
        for i in range(count):
            self.step()

    def __str__(self) -> str:
        out: typing.List[str] = []
        for y in range(self.rows):
            for x in range(self.cols):
                o = self.matrix.get((x, y), None)
                if o:
                    out.append(str(min(9, o.energy)))
                else:
                    out.append(" ")
            out.append("\n")
        return "".join(out)

    def step(self) -> None:
        # increase energy
        todo: typing.List[Octopus] = []
        for o in self.fleet:
            o.energy += 1
            if o.energy >= FLASH:
                todo.append(o)

        # process flashes
        while len(todo) != 0:
            o = todo.pop()
            if o.flashed:
                # already flashed
                continue
            assert o.energy >= FLASH
            o.flashed = True
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    o2 = self.matrix.get((o.x + dx, o.y + dy), None)
                    if o2 and o2 != o:
                        o2.energy += 1
                        if o2.energy >= FLASH:
                            todo.append(o2)

        # Afterwards
        for o in self.fleet:
            if o.flashed:
                o.energy = 0
                o.flashed = False
                self.flash_count += 1

    def find_sync_step(self) -> int:
        num = 0
        while True:
            before = self.flash_count
            self.step()
            num += 1
            if (self.flash_count - before) == len(self.fleet):
                # All flashed!
                return num

            assert num < 10000, "Expected to have synchronised by now"
        
    def read_tests(self, filename: Path) -> None:
        with open(filename) as fd:
            line = fd.readline()
            num = 0
            while line.strip() != "":
                assert line.startswith("After step ")
                self.step()
                print("got")
                print(str(self))
                print("expect")
                num += 1
                for y in range(self.rows):
                    line = fd.readline()
                    print(line.strip())
                    for x in range(self.cols):
                        got = self.matrix[(x, y)].energy 
                        expect = int(line[x])
                        assert got == expect, (
                "difference: step {} x {} y {} expect {} should be {}".format(
                    num, x, y, expect, got))

                line = fd.readline()
                assert line.strip() == ""

def test_middle() -> None:
    s = Sea(Path("middle1.txt"))
    s.read_tests(Path("middle2.txt"))

def test_large() -> None:
    s = Sea(Path("large1.txt"))
    s.read_tests(Path("large2.txt"))

def test_part_1() -> None:
    s = Sea(Path("large1.txt"))
    s.steps(10)
    assert s.flash_count == 204
    s.steps(90)
    assert s.flash_count == 1656

def test_part_2() -> None:
    s = Sea(Path("large1.txt"))
    assert s.find_sync_step() == 195

def main() -> None:
    s = Sea(Path("input.txt"))
    s.steps(100)
    print("part 1:", s.flash_count)
    s = Sea(Path("input.txt"))
    n = s.find_sync_step()
    print("part 2:", n)

if __name__ == "__main__":
    main()


