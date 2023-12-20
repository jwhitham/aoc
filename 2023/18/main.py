

import typing
import collections
import sys
import re


Position = typing.Tuple[int, int]
Direction = typing.Tuple[int, int]
RectangleIndex = typing.Tuple[int, int]

MOVE: typing.Dict[str, Direction] = {
    "R": (1, 0),
    "U": (0, -1),
    "L": (-1, 0),
    "D": (0, 1),
}

class Rectangle:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.inside = False
        self.left = False
        self.top = False
        self.right = False
        self.bottom = False

class Part1:
    def __init__(self) -> None:
        self.border: typing.List[Position] = []
        self.debug: typing.Optional[typing.Dict[Position, int]] = None

    def set_debug(self) -> None:
        self.debug = collections.defaultdict(lambda: 0)

    def parse(self, fname) -> None:
        parser = re.compile(r"^(\w) (\d+) \(#(\w+)\)\s*$")
        (x, y) = (0, 0)
        self.border.clear()
        for line in open(fname, "rt"):
            m = parser.match(line)
            assert m is not None
            (dx, dy) = MOVE[m.group(1)]
            distance = int(m.group(2))
            label = int(m.group(3), 16)
            x += dx * distance
            y += dy * distance
            self.border.append((x, y))

        assert (x, y) == (0, 0), (x, y)

    def area_within(self) -> int:
        # The area is divided into rectangles
        limit = (1 << 63) - 1
        x_coords = sorted(set([x for (x, _) in self.border] + [-limit, limit]))
        y_coords = sorted(set([y for (_, y) in self.border] + [-limit, limit]))
        print(x_coords)
        print(y_coords)
        rectangle: typing.Dict[RectangleIndex, Rectangle] = {}
        for xi in range(len(x_coords) - 1):
            for yi in range(len(y_coords) - 1):
                rectangle[(xi, yi)] = Rectangle(
                    x_coords[xi], y_coords[yi],
                    x_coords[xi + 1], y_coords[yi + 1])

        # For each border line, determine which rectangles are bordered
        for i in range(len(self.border)):
            (bx1, by1) = self.border[i]
            (bx2, by2) = self.border[(i + 1) % len(self.border)]
            if bx1 == bx2:
                # Vertical line
                if by1 > by2:
                    (by1, by2) = (by2, by1)

                # Detect left and right borders
                xi = x_coords.index(bx1)
                assert 0 < xi < len(x_coords)
                for yi in range(len(y_coords) - 1):
                    if ((by1 <= rectangle[(xi, yi)].y1)
                    and (rectangle[(xi, yi)].y2 <= by2)):
                        rectangle[(xi, yi)].left = True
                        rectangle[(xi - 1, yi)].right = True

            elif by1 == by2:
                # Horizontal line
                if bx1 > bx2:
                    (bx1, bx2) = (bx2, bx1)

                # Detect top and bottom borders
                yi = y_coords.index(by1)
                assert 0 < yi < len(y_coords)
                for xi in range(len(x_coords) - 1):
                    if ((bx1 <= rectangle[(xi, yi)].x1)
                    and (rectangle[(xi, yi)].x2 <= bx2)):
                        rectangle[(xi, yi)].top = True
                        rectangle[(xi, yi - 1)].bottom = True

            else:
                assert False

        # Which rectangles are within the border?
        for yi in range(len(y_coords) - 1):
            inside = False
            for xi in range(len(x_coords) - 1):
                if rectangle[(xi, yi)].left:
                    inside = not inside
                if inside:
                    rectangle[(xi, yi)].inside = inside
            xi = len(x_coords) - 2
            if rectangle[(xi, yi)].right:
                inside = not inside
            assert not inside

        # Compute area within rectangles
        total = 0
        for yi in range(len(y_coords) - 1):
            for xi in range(len(x_coords) - 1):
                r = rectangle[(xi, yi)]
                if not r.inside:
                    continue

                area = (r.x2 - r.x1 - 1) * (r.y2 - r.y1 - 1)
                total += area

                if not r.bottom:
                    area = r.x2 - r.x1 - 1
                    total += area
                if not r.right:
                    area = r.y2 - r.y1 - 1
                    total += area
                    if not r.bottom:
                        area = 1
                        total += area

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

    def check_within(self, fname) -> None:
        if not self.debug:
            return
        min_bx = min_by = sys.maxsize
        for (bx, by) in self.border:
            min_bx = min(min_bx, bx // 2)
            min_by = min(min_by, by // 2)

        for (ty, line) in enumerate(open(fname, "rt")):
            for (tx, col) in enumerate(line.rstrip()):
                x = tx + min_bx
                y = ty + min_by
                if (x, y) in self.debug:
                    print('{:x}'.format(self.debug[(x,y)]), end="")
                else:
                    print(col, end="")
            print("")

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
    #p.set_debug()
    #print(p.area_of_line())
    assert p.area_of_line() == 38
    #print(p.area_within())
    #p.check_within("test-output")
    rc = p.area_within()
    print(rc)
    assert rc == 62 - 38
    #print(p.area())
    assert p.area() == 62
    p = Part1()
    p.parse("input")
    print(p.area())
    assert p.area() == 46359


if __name__ == "__main__":
    main()