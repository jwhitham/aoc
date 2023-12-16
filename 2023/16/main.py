
import typing


Position = typing.Tuple[int, int]
Direction = typing.Tuple[int, int]

class Problem:
    def __init__(self, fname: str) -> None:
        self.mirrors: typing.Dict[Position, str] = {}
        self.width = self.height = 0
        for (y, line) in enumerate(open(fname, "rt")):
            for (x, col) in enumerate(line.rstrip()):
                self.mirrors[(x, y)] = col
                self.width = max(self.width, x + 1)
            self.height = max(self.height, y + 1)
        self.reset()

    def reset(self) -> None:
        self.energised: typing.Set[Position] = set()
        self.done: typing.Set[typing.Tuple[Position, Direction]] = set()

    def part1(self) -> int:
        self.recursive((0, 0), (1, 0))
        return len(self.energised)

    def part2(self) -> int:
        best = [0]
        def test(xy, dxdy):
            self.reset()
            self.recursive(xy, dxdy)
            best[0] = max(best[0], len(self.energised))

        for y in range(self.height):
            test((0, y), (1, 0))
            test((self.width - 1, y), (-1, 0))
        for x in range(self.width):
            test((x, 0), (0, 1))
            test((x, self.height - 1), (0, -1))
        return best[0]

    def dump(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.energised:
                    print("#", end="")
                else:
                    print(self.mirrors[(x, y)], end="")
            print("    ", end="")
            for x in range(self.width):
                print(self.mirrors[(x, y)], end="")
            print("")

    def recursive(self, xy: Position, dxdy: Direction) -> None:
        (x, y) = xy
        (dx, dy) = dxdy
        while True:
            here = self.mirrors.get((x, y), "")
            if here == "":
                return # off the edge

            key = ((x, y), (dx, dy))
            if key in self.done:
                return # already processed
            self.done.add(key)

            self.energised.add((x, y))
            if (here == ".") or (here == "-" and dy == 0) or (here == "|" and dx == 0):
                pass
            elif here == "/":
                # (0, -1) -> (1, 0)
                # (1, 0) -> (0, -1)
                # (0, 1) -> (-1, 0)
                # (-1, 0) -> (0, 1)
                (dx, dy) = (-dy, -dx)
            elif here == "\\":
                # (0, -1) -> (-1, 0)
                # (1, 0) -> (0, 1)
                # (0, 1) -> (1, 0)
                # (-1, 0) -> (0, -1)
                (dx, dy) = (dy, dx)
            elif here == "|":
                self.recursive((x, y + 1), (0, 1))
                (dx, dy) = (0, -1)
            elif here == "-":
                self.recursive((x + 1, y), (1, 0))
                (dx, dy) = (-1, 0)
            else:
                assert False, here

            x += dx
            y += dy

def part1(fname: str) -> int:
    p = Problem(fname)
    try:
        return p.part1()
    finally:
        #p.dump()
        pass

def part2(fname: str) -> int:
    return Problem(fname).part2()

def main() -> None:
    assert part1("test") == 46
    print(part1("input"))
    assert part2("test") == 51
    print(part2("input"))


if __name__ == "__main__":
    main()
