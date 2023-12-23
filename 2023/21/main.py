

import typing
import heapq

Position = typing.Tuple[int, int]

class Problem:
    def __init__(self, fname: str) -> None:
        self.start = (-1, -1)
        self.width = -1
        self.height = -1
        self.garden: typing.Set[Position] = set()
        with open(fname, "rt") as fd:
            for (y, line) in enumerate(fd):
                for (x, col) in enumerate(line.rstrip()):
                    if col == "S":
                        self.start = (x, y)
                    if col != "#":
                        self.garden.add((x, y))
                    self.width = max(self.width, x + 1)
                self.height = max(self.height, y + 1)

        self.shortest_distance: typing.Dict[Position, int] = {}
        todo: typing.List[typing.Tuple[int, Position]] = []
        heapq.heappush(todo, (0, self.start))
        while len(todo) != 0:
            (distance, (x, y)) = heapq.heappop(todo)
            if ((x, y) in self.shortest_distance) or ((x, y) not in self.garden):
                continue
            self.shortest_distance[(x, y)] = distance
            heapq.heappush(todo, (distance + 1, (x + 1, y)))
            heapq.heappush(todo, (distance + 1, (x - 1, y)))
            heapq.heappush(todo, (distance + 1, (x, y - 1)))
            heapq.heappush(todo, (distance + 1, (x, y + 1)))

    def part1(self, steps: int) -> int:
        # Anything with a shortest distance <= steps
        # and reachable in an even number of steps
        reachable = 0
        for y in range(self.height):
            for x in range(self.width):
                distance = self.shortest_distance.get((x, y), steps + 1)
                if distance > steps:
                    # Not in the garden or not reachable within the specified number
                    # of steps, so we can exclude it.
                    pass
                elif (distance % 2) == (steps % 2):
                    # Evenness matches steps
                    reachable += 1
        return reachable


def main():
    assert Problem("test").part1(6) == 16
    print(Problem("input").part1(64))

if __name__ == "__main__":
    main()
