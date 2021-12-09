
from pathlib import Path
import unittest
import typing


XY = typing.Tuple[int, int]

class Height:
    def __init__(self, value: int) -> None:
        self.value = value

class Heightmap:
    def __init__(self, filename: Path) -> None:
        self.matrix: typing.Dict[XY, Height] = {}
        self.rows = 0
        self.cols = 0

        for (y, line) in enumerate(open(filename, "rt")):
            for (x, cell) in enumerate(line.strip()):
                self.matrix[(x, y)] = Height(int(cell))
                self.cols = max(self.cols, x + 1)

            self.rows = max(self.rows, y + 1)

    def get(self, pos: XY) -> typing.Optional[Height]:
        return self.matrix.get(pos, None)

    def find_low_points(self) -> typing.List[XY]:
        low_points: typing.List[XY] = []
        for y in range(self.rows):
            for x in range(self.cols):
                here = self.get((x, y))
                if not here:
                    continue

                low_point = True
                for adjacent in [self.get((x - 1, y)), self.get((x + 1, y)),
                                 self.get((x, y - 1)), self.get((x, y + 1))]:
                    if adjacent and adjacent.value <= here.value:
                        low_point = False

                if not low_point:
                    continue

                low_points.append((x, y))

        return low_points
    
    def get_risk_level_sum(self) -> int:
        risk = 0
        for (x, y) in self.find_low_points():
            here = self.get((x, y))
            assert here
            risk += 1 + here.value
        return risk

def test_smoke_1() -> None:
    assert (1, 0) in Heightmap(Path("part1test.txt")).find_low_points()
    assert (2, 2) in Heightmap(Path("part1test.txt")).find_low_points()
    assert Heightmap(Path("part1test.txt")).get_risk_level_sum() == 15

def main() -> None:
    print("part 1:", Heightmap(Path("part1.txt")).get_risk_level_sum())

if __name__ == "__main__":
    main()


