

import typing
import heapq

Position = typing.Tuple[int, int]
ShortestDistance = typing.Dict[Position, int]

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

    def compute_distances(self, steps: int, start: Position, infinity: bool) -> ShortestDistance:
        shortest_distance = {}
        w = self.width
        h = self.height
        todo: typing.List[typing.Tuple[int, Position]] = []
        heapq.heappush(todo, (0, start))
        while len(todo) != 0:
            (distance, (x, y)) = heapq.heappop(todo)
            if (((x, y) in shortest_distance)
            or (distance > steps)
            or ((not infinity) and ((x, y) not in self.garden))
            or (infinity and ((x % w, y % h) not in self.garden))):
                continue
            shortest_distance[(x, y)] = distance
            heapq.heappush(todo, (distance + 1, (x + 1, y)))
            heapq.heappush(todo, (distance + 1, (x - 1, y)))
            heapq.heappush(todo, (distance + 1, (x, y - 1)))
            heapq.heappush(todo, (distance + 1, (x, y + 1)))

        return shortest_distance

    def count(self, steps: int, start: Position, infinity: bool) -> int:
        shortest_distance = self.compute_distances(steps, start, infinity)
        evenness = steps % 2
        reachable = 0
        for distance in shortest_distance.values():
            assert distance is not None
            assert distance <= steps
            if (distance % 2) == evenness:
                reachable += 1
        return reachable

    def part1(self, steps: int) -> int:
        r = self.count(steps, self.start, False)
        print(f"Part 1: {steps} = {r}")
        return r

    def part2_basic(self, steps: int) -> int:
        r = self.count(steps, self.start, True)
        print(f"Part 2 basic: {steps} = {r}")
        return r

    def part2_faster(self, steps: int) -> int:
        (sx, sy) = self.start
        size = max(self.width, self.height)
        w = self.width
        h = self.height
        quads = (steps + size - 1) // size
        evenness = steps % 2

        cache: typing.Dict[Position, ShortestDistance] = {}

        def inner_edge(qxy: int, wh: int) -> int:
            if qxy == 0:
                return wh // 2
            elif qxy > 0:
                return (qxy * wh)
            else:
                return (qxy * wh) + wh - 1

        def compute_q_distance(qxy: int, wh: int, sxy: int) -> int:
            if qxy == 0:
                return 0
            elif qxy > 0:
                return (wh - sxy) + ((qxy - 1) * wh)
            else:
                return sxy + 1 + ((-qxy - 1) * wh)

        def compute_quad(qx: int, qy: int) -> int:
            (sx, sy) = self.start
            q_distance = compute_q_distance(qx, w, sx) + compute_q_distance(qy, h, sy)

            sx = inner_edge(qx, w)
            sy = inner_edge(qy, h)
            key = (sx, sy)
            q_values = cache.get(key, None)
            if q_values is None:
                q_values = self.compute_distances(size * 2, (sx % w, sy % h), False)
                cache[key] = q_values

            sx = qx * w
            sy = qy * h
            reachable = 0
            for (x, y) in q_values:
                distance = q_values[(x, y)] + q_distance
                if (distance <= steps) and (distance % 2) == evenness:
                    reachable += 1

            return reachable

        print(f"Part 2 faster: {steps}")
        with open(f"matrix{steps}.csv", "wt") as fd:
            reachable = 0
            for qy in range(-quads, quads + 1):
                for qx in range(-quads, quads + 1):
                    r = compute_quad(qx, qy)
                    reachable += r
                    fd.write(f"{r},")
                fd.write("\n")

        print(f"Part 2 faster: {steps} = {reachable}")
        return reachable


def main():
    assert Problem("test").part1(6) == 16
    print(Problem("input").part1(64))
    assert Problem("test").part2_basic(6) == 16
    assert Problem("test").part2_basic(10) == 50
    assert Problem("test").part2_basic(50) == 1594
    assert Problem("test").part2_basic(100) == 6536
    assert Problem("test2").part2_basic(6) == 36
    assert Problem("test2").part2_basic(7) == 48
    assert Problem("test2").part2_basic(10) == 90
    assert Problem("test2").part2_basic(50) == 1940
    assert Problem("test2").part2_basic(51) == 2024
    assert Problem("test2").part2_basic(100) == 7645
    #assert Problem("test2").part2_basic(500) == 188756
    #assert Problem("test2").part2_basic(1000) == 753480
    assert Problem("test2").part2_faster(6) == 36
    assert Problem("test2").part2_faster(7) == 48
    assert Problem("test2").part2_faster(10) == 90
    assert Problem("test2").part2_faster(50) == 1940
    assert Problem("test2").part2_faster(51) == 2024
    assert Problem("test2").part2_faster(100) == 7645
    assert Problem("test2").part2_faster(500) == 188756
    assert Problem("test2").part2_faster(1000) == 753480
    assert Problem("test2").part2_faster(5000) == 18807440
    steps = 26501365
    print(Problem("test").part2_fast(steps))


if __name__ == "__main__":
    main()
