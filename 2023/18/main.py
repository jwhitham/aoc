

import typing
import re


Position = typing.Tuple[int, int]
Direction = typing.Tuple[int, int]

MOVE: typing.Dict[str, Direction] = {
    "R": (1, 0),
    "U": (0, -1),
    "L": (-1, 0),
    "D": (0, 1),
}


class Problem:
    def __init__(self, fname: str) -> None:
        self.colour: typing.Dict[Position, int] = {}
        self.border: typing.Set[Position] = set()
        (x, y) = (0, 0)
        self.border.add((x, y))
        self.min_x = self.min_y = self.max_x = self.max_y = 0
        parser = re.compile(r"^(\w) (\d+) \(#(\w+)\)\s*$")
        for line in open(fname, "rt"):
            m = parser.match(line)
            assert m is not None
            (dx, dy) = MOVE[m.group(1)]
            distance = int(m.group(2))
            label = int(m.group(3), 16)
            for i in range(distance * 3):
                x += dx
                y += dy
                if (x % 3) == 0 and (y % 3) == 0:
                    self.min_x = min(x, self.min_x)
                    self.min_y = min(y, self.min_y)
                    self.max_x = max(x, self.max_x)
                    self.max_y = max(y, self.max_y)
                    self.colour[(x, y)] = label

                self.border.add((x, y))

    def fill(self) -> None:
        for y in range(self.min_y - 1, self.max_y + 1, 3):
            inside = False
            for x in range(self.min_x - 1, self.max_x + 2, 1):
                if (x, y) in self.border:
                    inside = not inside

                if inside and ((x % 3) == 0) and ((x, y + 1) not in self.colour):
                    assert (y + 1) % 3 == 0
                    self.colour[(x, y + 1)] = 0

            assert not inside

    def part1(self) -> int:
        #self.dump()
        self.fill()
        #self.dump()
        return len(self.colour)

    def dump(self) -> None:
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                if (x, y) in self.border:
                    print("#", end="")
                elif (x, y) in self.colour:
                    print("*", end="")
                else:
                    print(".", end="")
            print("")
        print("")

def part1(fname: str) -> int:
    return Problem(fname).part1()

def main() -> None:
    assert part1("test") == 62
    print(part1("input"))


if __name__ == "__main__":
    main()
