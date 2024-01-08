
import typing
import re

IntersectXY = typing.Optional[typing.Tuple[float, float]]
DEBUG = False

class Stone:
    def __init__(self,
            px: float, py: float, pz: float,
            vx: float, vy: float, vz: float) -> None:
        self.px = px
        self.py = py
        self.pz = pz
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def __str__(self) -> str:
        return f"{self.px} {self.py} {self.pz} @ {self.vx} {self.vy} {self.vz}"

    def intersect_xy(self, other: "Stone") -> IntersectXY:
        # from Computer Graphics Principles and Practice (2nd. Ed), Foley et al. page 113
        # via lib20k/intersect.py, adapted for lines of infinite length
        xa = self.vx
        xa1 = self.px
        xb = other.vx
        xb1 = other.px

        ya = self.vy
        ya1 = self.py
        yb = other.vy
        yb1 = other.py

        a = ( xa * yb ) - ( xb * ya )
        if ( a == 0.0 ):
            return None

        b = ((( xa * ya1 ) + ( xb1 * ya ) - ( xa1 * ya )) - ( xa * yb1 ))
        tb = float(b) / float(a)

        if tb <= 0.0:
            return None # doesn't intersect

        if ( xa == 0.0 ):
            # xa and ya can't both be zero - if they are, a == 0 too
            ta = ( yb1 + ( yb * tb ) - ya1 ) / float(ya)
        else:
            ta = ( xb1 + ( xb * tb ) - xa1 ) / float(xa)

        if ta <= 0.0:
            return None # doesn't intersect

        return (xb1 + ( xb * tb ), yb1 + ( yb * tb ))

class Problem:
    def __init__(self, fname: str) -> None:
        self.stones: typing.List[Stone] = []
        with open(fname, "rt") as fd:
            for line in fd:
                values = [float(x) for x in re.findall("-?\d+", line)]
                assert len(values) == 6
                self.stones.append(Stone(*values))

    def part1(self, bound1: float, bound2: float) -> int:
        total = 0
        for i in range(len(self.stones) - 1):
            for j in range(i + 1, len(self.stones)):
                ixy = self.stones[i].intersect_xy(self.stones[j])
                if DEBUG:
                    print(self.stones[i], "  and  ", self.stones[j], "  at  ", ixy)
                if ixy is not None:
                    (ix, iy) = ixy
                    if ((bound1 <= ix <= bound2) and (bound1 <= iy <= bound2)):
                        total += 1

        return total

if __name__ == "__main__":
    assert Problem("test").part1(7, 27) == 2
    bound1 = 200000000000000
    bound2 = 400000000000000
    print(Problem("input").part1(bound1, bound2))


