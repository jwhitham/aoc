
from pathlib import Path
import unittest
import typing


XY = typing.Tuple[int, int]

class Height:
    def __init__(self, value: int) -> None:
        self.value = value
        self.basin_id = 0

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

    def assign_basins(self) -> typing.List[int]:
        basin_size: typing.Dict[int, int] = {}

        def flood_fill(pos: XY) -> None:
            target = self.get(pos)
            if (not target) or target.basin_id or target.value >= 9:
                return
            target.basin_id = len(basin_size)
            basin_size[target.basin_id] += 1
            (x, y) = pos
            flood_fill((x - 1, y))
            flood_fill((x + 1, y))
            flood_fill((x, y - 1))
            flood_fill((x, y + 1))

        for pos in self.find_low_points():
            basin_size[len(basin_size) + 1] = 0
            flood_fill(pos)

        return sorted(basin_size.values())

    def get_three_basins(self) -> int:
        basins = self.assign_basins()
        assert len(basins) >= 3
        return basins[-1] * basins[-2] * basins[-3]

def test_smoke_1() -> None:
    assert (1, 0) in Heightmap(Path("part1test.txt")).find_low_points()
    assert (2, 2) in Heightmap(Path("part1test.txt")).find_low_points()
    assert Heightmap(Path("part1test.txt")).get_risk_level_sum() == 15

def test_smoke_2() -> None:
    basins = Heightmap(Path("part1test.txt")).assign_basins()
    assert len(basins) == 4
    assert basins[-1] == 14
    assert basins[-2] == 9
    assert basins[-3] == 9
    assert basins[-4] == 3
    assert Heightmap(Path("part1test.txt")).get_three_basins() == 1134

def main() -> None:
    print("part 1:", Heightmap(Path("part1.txt")).get_risk_level_sum())
    print("part 2:", Heightmap(Path("part1.txt")).get_three_basins())

if __name__ == "__main__":
    main()


