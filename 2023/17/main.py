

import typing
import heapq


Position = typing.Tuple[int, int]
Direction = typing.Tuple[int, int]
SearchStateHashKey = typing.Tuple[int, int, int, int, int]

TURN_LEFT: typing.Dict[Direction, Direction] = {
    (1, 0): (0, -1),        # East -> North
    (0, -1): (-1, 0),       # North -> West
    (-1, 0): (0, 1),        # West -> South
    (0, 1): (1, 0),         # South -> East
}
SYMBOL: typing.Dict[Direction, str] = {
    (1, 0): ">",
    (0, -1): "^",
    (-1, 0): "<",
    (0, 1): "v",
}


class SearchState:
    def __init__(self, xy: Position, dxdy: Direction, move_count: int, heat: int,
                back: typing.Optional["SearchState"]) -> None:
        (self.x, self.y) = xy
        (self.dx, self.dy) = dxdy
        self.move_count = move_count
        self.heat = heat
        self.back = back

    def __lt__(self, other: typing.Optional["SearchState"]) -> bool:
        if not isinstance(other, SearchState):
            return False
        return self.heat < other.heat
       
    def key(self) -> SearchStateHashKey:
        return (self.x, self.y, self.dx, self.dy, self.move_count)

class Problem:
    def __init__(self, fname: str) -> None:
        self.heat: typing.Dict[Position, int] = {}
        self.best: typing.Dict[SearchStateHashKey, SearchState] = {}
        self.width = self.height = 0
        for (y, line) in enumerate(open(fname, "rt")):
            for (x, col) in enumerate(line.rstrip()):
                self.heat[(x, y)] = int(col)
                self.width = max(self.width, x + 1)
            self.height = max(self.height, y + 1)

    def search(self, min_moves: int, max_moves: int) -> int:
        self.best.clear()
        todo: typing.List[SearchState] = []
        overall_best: typing.Optional[SearchState] = None
        end = (self.width - 1, self.height - 1)
        heapq.heappush(todo, SearchState((1, 0), (1, 0), 0, 0, None))
        heapq.heappush(todo, SearchState((0, 1), (0, 1), 0, 0, None))
        while True:
            current = heapq.heappop(todo)
            (x, y) = (current.x, current.y)
            (dx, dy) = (current.dx, current.dy)
            key = current.key()

            if ((key in self.best)
            or (x < 0) or (y < 0)
            or (x >= self.width) or (y >= self.height)):
                continue

            self.best[key] = current
            move_count = current.move_count + 1
            heat = current.heat + self.heat[(x, y)]

            if move_count < max_moves:
                # Go straight on
                heapq.heappush(todo, SearchState((x + dx, y + dy), (dx, dy), move_count, heat, current))

            if min_moves <= move_count:
                # Terminate?
                if (x, y) == end:
                    return heat

                # Turn left
                (dx, dy) = TURN_LEFT[(dx, dy)]
                heapq.heappush(todo, SearchState((x + dx, y + dy), (dx, dy), 0, heat, current))

                # Turn right
                (dx, dy) = TURN_LEFT[(dx, dy)]
                (dx, dy) = TURN_LEFT[(dx, dy)]
                heapq.heappush(todo, SearchState((x + dx, y + dy), (dx, dy), 0, heat, current))

def part1(fname: str) -> int:
    return Problem(fname).search(1, 3)

def part2(fname: str) -> int:
    return Problem(fname).search(4, 10)

def main() -> None:
    assert part1("test") == 102
    print(part1("input"))
    assert part2("test") == 94
    print(part2("input"))


if __name__ == "__main__":
    main()
