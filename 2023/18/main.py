

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
            x += dx * distance
            y += dy * distance
            self.border.append((x, y))

        assert (x, y) == (0, 0)

    def area_within(self) -> int:
        x_coords = sorted(set([x for (x, y) in self.border]))
        y_coords = sorted(set([y for (x, y) in self.border]))
        total = 0

        # The area within the line
        for i in range(len(y_coords) - 1):
            # Evaluate an area in the map from (-inf, y1) to (+inf, y2)
            y1 = y_coords[i]
            y2 = y_coords[i + 1]
            assert y1 < y2

            # Each x division may create a rectangle which is in the area or not
            inside = False
            x_start = x_coords[0]
            for x in x_coords:
                # Did this cross a border line?
                border = False
                for j in range(len(self.border) - 1):
                    # Examine a line in the border
                    (bx1, by1) = self.border[j]
                    (bx2, by2) = self.border[j + 1]

                    if bx1 == x and bx2 == x:
                        # This is a vertical line that might cross x
                        # Ensure by1 < by2
                        if by1 > by2:
                            (by1, by2) = (by2, by1)
                        assert by1 < by2

                        # Border line crossed?
                        if by1 <= y1 and y2 <= by2:
                            border = True
                            break
                    elif bx1 == x and by1 == by2 == y1:
                        # This is a horizontal line beginning at (x, y1)
                        

                if border:
                    if inside:
                        # Leaving the area
                        total += ((x - 1) - (x_start + 1)) * ((y2 - 1) - (y1 + 1))
                        inside = False
                    else:
                        # Entering the area
                        x_start = x
                        inside = True
        return total

    def area_of_line(self) -> int:
        total = 0
        for j in range(len(self.border) - 1):
            (bx1, by1) = self.border[j]
            (bx2, by2) = self.border[j + 1]
            if bx1 == bx2:
                total += abs(by2 - by1)
            else:
                total += abs(bx2 - bx1)

        return total

    def area(self) -> int:
        return self.area_of_line() + self.area_within()

def main() -> None:
    p = Part1()
    p.parse("test")
    assert p.area_of_line() == 38
    print(p.area_within())
    assert p.area_within() == 24
    assert p.area() == 62
    p.parse("input")
    p = Part1()
    print(p.area())
    assert p.area() == 46359


if __name__ == "__main__":
    main()
