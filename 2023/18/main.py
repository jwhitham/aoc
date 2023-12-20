

import typing
import collections
import sys
import re
from bisect import bisect_left

# This puzzle is extra hard because the borders need to be counted.
# Treating the border paths as rectangles reduced the need to handle
# corners and edges as special cases.

Position = typing.Tuple[int, int]
Direction = typing.Tuple[int, int]
RectangleIndex = typing.Tuple[int, int]

MOVE: typing.Dict[str, Direction] = {
    "R": (1, 0),
    "U": (0, -1),
    "L": (-1, 0),
    "D": (0, 1),
}
MOVE2: typing.Dict[int, Direction] = {
    0: (1, 0),
    3: (0, -1),
    2: (-1, 0),
    1: (0, 1),
}

class Rectangle:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.inside = False
        self.border = False
        self.transition = False

class Part1:
    def __init__(self) -> None:
        self.border: typing.List[Position] = []
        self.debug: typing.Optional[typing.Dict[Position, int]] = None

    def set_debug(self) -> None:
        self.debug = collections.defaultdict(lambda: 0)

    def parse(self, fname) -> None:
        parser = re.compile(r"^(\w) (\d+) \(#\w+\)\s*$")
        (x, y) = (0, 0)
        self.border.clear()
        for line in open(fname, "rt"):
            m = parser.match(line)
            assert m is not None
            (dx, dy) = MOVE[m.group(1)]
            distance = int(m.group(2))
            x += dx * distance
            y += dy * distance
            self.border.append((x, y))

        assert (x, y) == (0, 0), (x, y)

    def area_within(self) -> int:
        # The area is divided into rectangles.
        # Some rectangles represent parts of the border.
        # Others are inside, others are outside.
        limit = (1 << 63) - 1
        x_coords = sorted(set([x for (x, _) in self.border])
                        | set([x + 1 for (x, _) in self.border])
                        | set([-limit, limit]))
        y_coords = sorted(set([y for (_, y) in self.border])
                        | set([y + 1 for (_, y) in self.border])
                        | set([-limit, limit]))
        rectangle: typing.Dict[RectangleIndex, Rectangle] = {}
        for xi in range(len(x_coords) - 1):
            for yi in range(len(y_coords) - 1):
                rectangle[(xi, yi)] = Rectangle(
                    x_coords[xi], y_coords[yi],
                    x_coords[xi + 1], y_coords[yi + 1])

        # Determine which rectangles correspond to part of the border
        for i in range(len(self.border)):
            (bx1, by1) = self.border[i]
            (bx2, by2) = self.border[(i + 1) % len(self.border)]
            xi1 = bisect_left(x_coords, min(bx1, bx2))
            xi2 = bisect_left(x_coords, max(bx1, bx2))
            yi1 = bisect_left(y_coords, min(by1, by2))
            yi2 = bisect_left(y_coords, max(by1, by2))
            assert 0 < xi1 <= xi2 < (len(x_coords) - 1)
            assert 0 < yi1 <= yi2 < (len(y_coords) - 1)
            for yi in range(yi1, yi2 + 1):
                for xi in range(xi1, xi2 + 1):
                    rectangle[(xi, yi)].border = True

            if bx1 == bx2:
                # Vertical line; don't include the topmost square in this
                # so that a connected horizontal line will work correctly.
                for yi in range(yi1, yi2):
                    rectangle[(xi1, yi)].transition = True

        # Which rectangles are within the border?
        for yi in range(len(y_coords) - 1):
            inside = False
            for xi in range(len(x_coords) - 1):
                r = rectangle[(xi, yi)]
                if r.border and r.transition:
                    # Entered new border rectangle
                    inside = not inside

                if inside and not r.border:
                    r.inside = True

                    # These assertions detect if one of the large border rectangles
                    # has been incorrectly classified as "inside"
                    assert abs(r.x1) < limit
                    assert abs(r.y1) < limit
                    assert abs(r.x2) < limit
                    assert abs(r.y2) < limit

            assert not inside

        # Compute area within border
        total = 0
        for yi in range(len(y_coords) - 1):
            for xi in range(len(x_coords) - 1):
                r = rectangle[(xi, yi)]
                if not r.inside:
                    continue

                assert not r.border
                assert not r.transition
                area = (r.x2 - r.x1) * (r.y2 - r.y1)
                total += area

                if self.debug is not None:
                    for y in range(r.y1, r.y2):
                        for x in range(r.x1, r.x2):
                            self.debug[(x, y)] += 1


        return total

    def area_of_line(self) -> int:
        total = 0
        for j in range(len(self.border)):
            (bx1, by1) = self.border[j]
            (bx2, by2) = self.border[(j + 1) % len(self.border)]
            assert (bx1 == bx2) or (by1 == by2)
            total += abs(by2 - by1) + abs(bx2 - bx1)
        return total

    def area(self) -> int:
        return self.area_within() + self.area_of_line()

    def dump(self, callback: typing.Callable[[int, int], typing.Any],
                min_bx: int, min_by: int, max_bx: int, max_by: int) -> None:
        for y in range(min_by, max_by + 1):
            for x in range(min_bx, max_bx + 1):
                s = callback(x, y)
                if s is None:
                    s = " "
                print(str(s), end="")
            print()

    def check_within(self, fname) -> None:
        if not self.debug:
            return
        min_bx = min_by = sys.maxsize
        for (bx, by) in self.border:
            min_bx = min(min_bx, bx)
            min_by = min(min_by, by)

        for (ty, line) in enumerate(open(fname, "rt")):
            bad = ""
            for (tx, col) in enumerate(line.rstrip()):
                x = tx + min_bx
                y = ty + min_by
                if (x, y) in self.debug:
                    if col == "*":
                        print('{:x}'.format(self.debug[(x,y)]), end="")
                    else:
                        print('!', end="")
                        bad = f" {(x, y)}"
                elif col == "*":
                    print('?', end="")
                else:
                    print(col, end="")
            print(bad)

class Part2(Part1):
    def parse(self, fname) -> None:
        parser = re.compile(r"^\w \d+ \(#(\w+)\)\s*$")
        (x, y) = (0, 0)
        self.border.clear()
        for line in open(fname, "rt"):
            m = parser.match(line)
            assert m is not None
            hexcode = int(m.group(1), 16)
            distance = hexcode >> 4
            (dx, dy) = MOVE2[hexcode & 0xf]
            x += dx * distance
            y += dy * distance
            self.border.append((x, y))

        assert (x, y) == (0, 0), (x, y)

def main() -> None:
    p = Part1()
    p.parse("test2") # A 2x2 square (line length 1)
    assert p.area_of_line() == 4
    assert p.area_within() == 0
    assert p.area() == 4
    p = Part1() # A 3x3 square (line length 2)
    p.parse("test3")
    assert p.area_of_line() == 8
    assert p.area_within() == 1
    assert p.area() == 9
    p = Part1() # A 4x4 square (line length 3)
    p.parse("test4")
    assert p.area_of_line() == 12
    assert p.area_within() == 4
    assert p.area() == 16
    p = Part1()
    # ###       3, 0
    # #*#       2, 1
    # #*###     4, 1
    # #***#     2, 3
    # #####     5, 0
    p.parse("test5")
    assert p.area_of_line() == 3 + 2 + 4 + 2 + 5
    assert p.area_within() == 1 + 1 + 3
    assert p.area() == 3 + 3 + 5 + 5 + 5
    p = Part1()
    p.parse("test")
    assert p.area_of_line() == 38
    assert p.area() == 62
    p = Part1()
    p.parse("input")
    print(p.area())
    assert p.area() == 46359

    p = Part2()
    p.parse("test")
    assert p.area() == 952408144115
    p = Part2()
    p.parse("input")
    print(p.area())

def debug_main() -> None:
    p = Part1()
    p.parse("test")
    p.set_debug()
    assert p.area_of_line() == 38
    rc = p.area_within()
    p.check_within("test-output")
    print(rc)
    assert rc == 62 - 38

if __name__ == "__main__":
    debug_main()
    main()
