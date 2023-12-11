
import typing, heapq

Cell = int
Position = typing.Tuple[int, int]
Expansion = typing.Dict[int, int]

class Map:
    def __init__(self, fname: str, expand_constant: int) -> None:
        unexpanded_map: typing.Dict[Position, Cell] = {}
        unexpanded_width = unexpanded_height = 0
        occupied_column: typing.Set[int] = set()
        occupied_row: typing.Set[int] = set()

        # Original map
        for (y, line) in enumerate(open(fname, "rt")):
            for (x, col) in enumerate(line.rstrip()):
                if col == "#":
                    unexpanded_map[(x, y)] = len(unexpanded_map) + 1
                    occupied_column.add(x)
                    occupied_row.add(y)

                unexpanded_width = max(unexpanded_width, x + 1)

            unexpanded_height = max(unexpanded_height, y + 1)

        # How should it expand?
        x_expansion = self.compute_expansion(occupied_column, unexpanded_width, expand_constant)
        y_expansion = self.compute_expansion(occupied_row, unexpanded_height, expand_constant)
        self.width = max(x_expansion.values()) + 1
        self.height = max(y_expansion.values()) + 1

        # New map
        self.map: typing.Dict[Position, Cell] = {}
        for (x, y) in unexpanded_map:
            self.map[(x_expansion[x], y_expansion[y])] = unexpanded_map[(x, y)]

    def compute_expansion(self, occupied: typing.Set[int],
                unexpanded_size: int, expand_constant: int) -> Expansion:
        j = 0
        expansion: Expansion = {}
        for i in range(unexpanded_size):
            expansion[i] = j
            if i not in occupied:
                j += expand_constant
            else:
                j += 1
        return expansion

    def compute_distances(self, pos: Position) -> typing.Dict[Position, int]:
        # Actually the Manhattan distance is good enough...
        distance: typing.Dict[Position, int] = {}
        todo: typing.List[typing.Tuple[int, Position]] = []
        heapq.heappush(todo, (0, pos))
        while len(todo) != 0:
            (d, (x, y)) = heapq.heappop(todo)
            if ((x, y) in distance
            or (x < 0) or (y < 0)
            or (x >= self.width) or (y >= self.height)):
                continue
            distance[(x, y)] = d
            heapq.heappush(todo, (d + 1, (x + 1, y + 0)))
            heapq.heappush(todo, (d + 1, (x - 1, y + 0)))
            heapq.heappush(todo, (d + 1, (x + 0, y - 1)))
            heapq.heappush(todo, (d + 1, (x + 0, y + 1)))

        return distance

    def compute_total_distances(self) -> int:
        total = 0
        for pos1 in self.map:
            #distance = self.compute_distances(pos1)
            (x1, y1) = pos1
            for pos2 in self.map:
                if pos1 < pos2:
                    (x2, y2) = pos2
                    md = abs(x2 - x1) + abs(y2 - y1) 
                    #assert md == distance[pos2]
                    total += md

        return total
        

def part1(fname):
    return Map(fname, 2).compute_total_distances()

def part2(fname):
    return Map(fname, 1000000).compute_total_distances()

def main():
    assert part1("test") == 374
    print(part1("input"))
    assert Map("test", 10).compute_total_distances() == 1030, (
            Map("test", 10).compute_total_distances())
    assert Map("test", 100).compute_total_distances() == 8410
    print(part2("input"))

if __name__ == "__main__":
    main()
