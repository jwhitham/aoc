
"""
    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
"""

import typing, heapq

Cell = str
Position = typing.Tuple[int, int]

PIPES = {
    "|": ((0, - 1), (0, + 1)),
    "-": ((- 1, 0), (+ 1, 0)),
    "L": ((0, - 1), (+ 1, 0)),
    "F": ((0, + 1), (+ 1, 0)),
    "7": ((- 1, 0), (0, + 1)),
    "J": ((- 1, 0), (0, - 1)),
}

class Map:
    def __init__(self, fname: str) -> None:
        self.cell: typing.Dict[Position, Cell] = {}
        self.width = self.height = 0
        self.start = (-1, -1)

        for (y, line) in enumerate(open(fname, "rt")):
            for (x, col) in enumerate(line.rstrip()):
                self.cell[(x, y)] = col
                self.width = max(self.width, x + 1)
                if col == "S":
                    self.start = (x, y)

            self.height = max(self.height, y + 1)

        self.distance: typing.Dict[Position, int] = {}
        todo: typing.List[typing.Tuple[int, Position]] = []
        self.largest_distance = 0
        heapq.heappush(todo, (0, self.start))
        while len(todo) != 0:
            (distance, (x, y)) = heapq.heappop(todo)
            if (x, y) in self.distance:
                continue
            self.distance[(x, y)] = distance
            self.largest_distance = max(distance, self.largest_distance)

            cell = self.cell.get((x, y), ".")
            out: typing.Tuple = PIPES.get(cell, tuple())
            if len(out) != 0:
                for (dx, dy) in out:
                    heapq.heappush(todo, (distance + 1, (x + dx, y + dy)))
            elif cell == "S":
                for (dx, dy) in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                    if (-dx, -dy) in PIPES.get(self.cell.get((x + dx, y + dy), "."), tuple()):
                        # Back connection exists
                        heapq.heappush(todo, (distance + 1, (x + dx, y + dy)))
    
    def part2(self) -> int:
        count = 0
        expanded: typing.Set[Position] = set()
        for y in range(self.height):
            for x in range(self.width):
                dist = self.distance.get((x, y), -1)
                if dist >= 0:
                    mx = (x * 3) + 1
                    my = (y * 3) + 1
                    cell = self.cell.get((x, y), ".")
                    for (dx, dy) in PIPES.get(cell, tuple()):
                        expanded.add((mx + dx, my + dy))

                    if cell == "S":
                        for (dx, dy) in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                            if (-dx, -dy) in PIPES.get(self.cell.get((x + dx, y + dy), "."), tuple()):
                                expanded.add((mx + dx, my + dy))

                    if cell != ".":
                        expanded.add((mx, my))
    
        for y in range(0, self.height * 3, 3):
            in_loop = False
            for x in range(self.width * 3):
                if (x, y) in expanded:
                    in_loop = not in_loop
                elif ((x % 3) == 1) and (self.distance.get((x // 3, y // 3), -1) < 0) and in_loop:
                    count += 1

        return count

def part1(fname):
    return Map(fname).largest_distance

def part2(fname):
    return Map(fname).part2()

def main():
    assert part1("test") == 4
    print(part1("input"))
    assert part2("test4") == 4
    assert part2("test8") == 8
    print(part2("input"))

if __name__ == "__main__":
    main()
