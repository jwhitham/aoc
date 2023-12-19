

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


class Part1:
    def __init__(self) -> None:
        self.border: typing.List[Position] = []

    def parse(self, fname) -> None:
        parser = re.compile(r"^(\w) (\d+) \(#(\w+)\)\s*$")
        (x, y) = (0, 0)
        self.border.clear()
        self.border.append((x, y))
        for line in open(fname, "rt"):
            m = parser.match(line)
            assert m is not None
            (dx, dy) = MOVE[m.group(1)]
            distance = int(m.group(2))
            label = int(m.group(3), 16)
            x += dx * distance * 2
            y += dy * distance * 2
            self.border.append((x, y))

        assert (x, y) == (0, 0), (x, y)

    def count_borders_between_cx_cy_and_inf_cy(self, cx: int, cy: int) -> int:
        # How many border lines between (cx, cy) and (inf, cy)?
        borders = 0
        for j in range(len(self.border) - 1):
            (bx1, by1) = self.border[j]
            (bx2, by2) = self.border[j + 1]
            if bx1 != bx2:
                # Not a vertical line: skip
                continue
            if bx1 < cx:
                # Vertical line to the left of cx: skip
                continue

            if by1 > by2:
                # Line is upside down
                (by1, by2) = (by2, by1)

            if not (by1 <= cy <= by2):
                # Line does not intersect (cx, cy) and (inf, cy)
                continue

            borders += 1
        return borders

    def is_point_on_border(self, x, y):
        for j in range(len(self.border) - 1):
            (bx1, by1) = self.border[j]
            (bx2, by2) = self.border[j + 1]
            if by1 == by2 == y:
                # Horizontal line at y
                if bx1 > bx2:
                    # Line is backwards
                    (bx1, bx2) = (bx2, bx1)
                if bx1 <= x <= bx2:
                    return True
            elif bx1 == bx2 == x:
                # Vertical line at x
                if by1 > by2:
                    # Line is upside down
                    (by1, by2) = (by2, by1)
                if by1 <= y <= by2:
                    return True
        return False

    def area_within(self) -> int:
        total = 0
        # Area divided into rectangles
        x_coords = sorted(set([x for (x, y) in self.border]))
        y_coords = sorted(set([y for (x, y) in self.border]))

        # Visit each rectangle and determine if it's inside the border
        for xi in range(len(x_coords) - 1):
            x1 = x_coords[xi]
            x2 = x_coords[xi + 1]
            assert (x1 % 2) == 0
            assert (x2 % 2) == 0
            assert x1 < x2
            for yi in range(len(y_coords) - 1):
                y1 = y_coords[yi]
                y2 = y_coords[yi + 1]
                assert (y1 % 2) == 0
                assert (y2 % 2) == 0
                assert y1 < y2

                # Centre of the rectangle
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                # How many border lines between (cx, cy) and (inf, cy)?
                area = ((x2 - x1 - 2) * (y2 - y1 - 2)) // 4
                borders = self.count_borders_between_cx_cy_and_inf_cy(cx, cy)
                #print(f"Rectangle ({x1},{y1}) ({x2},{y2}) borders {borders} area {area}")
                if (borders % 2) == 0:
                    # Even number of borders, this rectangle is outside the border
                    continue

                # Rectangle is within the border
                total += area

                # Count the lines around the rectangle
                if not self.is_point_on_border(cx, y2):
                    area = (x2 - x1 - 2) // 2
                    #print(f"Internal line ({x1},{y2}) ({x2},{y2}) area {area}")
                    total += area
                if not self.is_point_on_border(x2, cy):
                    area = (y2 - y1 - 2) // 2
                    #print(f"Internal line ({x2},{y1}) ({x2},{y2}) area {area}")
                    total += area

        return total

    def area_of_line(self) -> int:
        total = 0
        for j in range(len(self.border) - 1):
            (bx1, by1) = self.border[j]
            (bx2, by2) = self.border[j + 1]
            assert (bx1 == bx2) or (by1 == by2)
            total += abs(by2 - by1) + abs(bx2 - bx1)
        return total // 2

    def area(self) -> int:
        return self.area_within() + self.area_of_line()

def main() -> None:
    p = Part1()
    p.parse("test2") # A 2x2 square (line length 1)
    assert p.area_of_line() == 4
    assert p.area_within() == 0
    p = Part1() # A 3x3 square (line length 2)
    p.parse("test3")
    assert p.area_of_line() == 8
    assert p.area_within() == 1
    p = Part1() # A 4x4 square (line length 3)
    p.parse("test4")
    assert p.area_of_line() == 12
    assert p.area_within() == 4
    p = Part1()
    # ###       3, 0
    # #*#       2, 1
    # #*###     4, 1
    # #***#     2, 3
    # #####     5, 0
    p.parse("test5")
    assert p.area_of_line() == 3 + 2 + 4 + 2 + 5
    assert p.area_within() == 1 + 1 + 3
    p = Part1()
    p.parse("test")
    print(p.area_of_line())
    assert p.area_of_line() == 38
    print(p.area_within())
    #assert p.area_within() == 62 - 38
    print(p.area())
    assert p.area() == 62
    p.parse("input")
    p = Part1()
    print(p.area())
    assert p.area() == 46359


if __name__ == "__main__":
    main()
