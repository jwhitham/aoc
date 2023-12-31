

import typing
import heapq

Position = typing.Tuple[int, int]
ShortestDistance = typing.Dict[Position, int]
Quad = typing.Tuple[int, int]
DEBUG = False

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
        assert (w // 2) == sx
        assert (h // 2) == sy
        quads = (steps + size - 1) // size
        evenness = steps % 2
        reachable = 0
        cache: typing.Dict[Position, ShortestDistance] = {}

        def inner_edge(qxy: int, wh: int) -> int:
            # Determine start point in any quad
            if qxy == 0:
                return wh // 2
            elif qxy > 0:
                return (qxy * wh)
            else:
                return (qxy * wh) + wh - 1

        def compute_q_distance(qxy: int, wh: int, sxy: int) -> int:
            # Distance from start point to a new start point in any quad
            if qxy == 0:
                return 0
            elif qxy > 0:
                return (wh - sxy) + ((qxy - 1) * wh)
            else:
                return sxy + 1 + ((-qxy - 1) * wh)

        def compute_quad(qx: int, qy: int) -> int:
            # Number of reachable squares within quad (qx, qy)
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

        # A zero column
        # An odd column
        # An even column
        # An inner edge
        # An outer edge
        # A mostly-zero edge
        # Minimum 6?
        if quads <= 5:
            # No special processing is required. Just add it all up.
            for qy in range(-quads, quads + 1):
                for qx in range(-quads, quads + 1):
                    reachable += compute_quad(qx, qy)

            print(f"Part 2 faster (small): {steps} = {reachable}")
            return reachable

        def add_horizontal_or_vertical(compute_quad: typing.Callable[[int], int]) -> int:
            # Search until a repeating pattern is found
            # Start point: right on the edge (or beyond it)
            qxy = quads

            # What's the repeating pattern for this edge?
            odd_repeat = compute_quad(1)
            even_repeat = compute_quad(2)
            
            # Find first part of the edge containing some reachable squares
            r = compute_quad(qxy)
            while r == 0:
                qxy -= 1
                r = compute_quad(qxy)

            # Continue until we reach the repeating pattern
            reachable = 0
            for i in range(4):
                reachable += r
                qxy -= 1
                r = compute_quad(qxy)

            assert r in (odd_repeat, even_repeat)
            assert qxy >= 1

            # How much repeating pattern until the zero line is reached?
            if (qxy % 2) == 0:
                # Same number of even and odd quads: 1, 2, 3, 4
                reachable += abs(qxy // 2) * even_repeat
                reachable += abs(qxy // 2) * odd_repeat
            else:
                # Fewer even than odd quads: 1, 2, 3
                reachable += (abs((qxy + 1) // 2) - 1) * even_repeat
                reachable += abs((qxy + 1) // 2) * odd_repeat

            # Check!
            if DEBUG:
                i = 1
                check = 0
                r = compute_quad(i)
                while r != 0:
                    check += r
                    i += 1
                    r = compute_quad(i)
                assert check == reachable

            return reachable

        def add_triangle(dqx: int, dqy: int) -> int:
            assert abs(dqx) == 1
            assert abs(dqy) == 1

            # What's the repeating pattern for this edge?
            odd_repeat = compute_quad(dqx, dqy)
            even_repeat = compute_quad(dqx * 2, dqy)
            assert even_repeat == compute_quad(dqx, dqy * 2)
            assert odd_repeat == compute_quad(dqx * 2, dqy * 2)
           
            # Find outer edge of triangle
            qx = quads * dqx
            qy = dqy
            r = compute_quad(qx, qy)
            while r == 0:
                qx -= dqx
                r = compute_quad(qx, qy)

            # Continue across the edge - reaching the repeating pattern
            reachable = 0
            for i in range(4):
                r = compute_quad(qx, qy)
                reachable += r * abs(qx)
                qx -= dqx

            assert abs(qx) >= 1
            assert r in (odd_repeat, even_repeat)

            # What's the area of the triangle?
            total_size = ((qx ** 2) + abs(qx)) // 2     # Triangle number
            odd_size = ((abs(qx) + 1) // 2) ** 2
            even_size = total_size - odd_size
            reachable += even_repeat * even_size
            reachable += odd_repeat * odd_size

            # Check!
            if DEBUG:
                check = 0
                for qx in range(dqx, dqx * (quads + 1), dqx):
                    for qy in range(dqy, dqy * (quads + 1), dqy):
                        check += compute_quad(qx, qy)
                assert check == reachable, (check, reachable, total_size)

            return reachable

        # Centre square
        reachable += compute_quad(0, 0)
        # Horizontal at qy = 0
        reachable += add_horizontal_or_vertical(lambda qxy: compute_quad(-qxy, 0))
        reachable += add_horizontal_or_vertical(lambda qxy: compute_quad(qxy, 0))
        # Vertical at qx = 0
        reachable += add_horizontal_or_vertical(lambda qxy: compute_quad(0, -qxy))
        reachable += add_horizontal_or_vertical(lambda qxy: compute_quad(0, qxy))
        # Triangles
        reachable += add_triangle(1, 1)
        reachable += add_triangle(1, -1)
        reachable += add_triangle(-1, 1)
        reachable += add_triangle(-1, -1)
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
    assert Problem("test2").part2_basic(53) == 2207
    assert Problem("test2").part2_basic(100) == 7645
    #assert Problem("test2").part2_basic(500) == 188756
    #assert Problem("test2").part2_basic(1000) == 753480
    #assert Problem("test2").part2_basic(5000) == 18807440
    assert Problem("test2").part2_faster(6) == 36
    assert Problem("test2").part2_faster(7) == 48
    assert Problem("test2").part2_faster(10) == 90
    assert Problem("test2").part2_faster(50) == 1940
    assert Problem("test2").part2_faster(51) == 2024
    assert Problem("test2").part2_faster(53) == 2207
    assert Problem("test2").part2_faster(100) == 7645
    assert Problem("test2").part2_faster(500) == 188756
    assert Problem("test2").part2_faster(1000) == 753480
    assert Problem("test2").part2_faster(5000) == 18807440
    steps = 26501365
    print(Problem("input").part2_faster(steps))


if __name__ == "__main__":
    main()
