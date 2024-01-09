
import typing
import re

IntersectXY = typing.Optional[typing.Tuple[float, float]]
DEBUG = False
EPSILON = 1e-6


def near(a: float, b: float) -> bool:
    return abs(a - b) < EPSILON

def near_or_none(a: typing.Optional[float], b: typing.Optional[float]) -> bool:
    if (a is not None) and (b is not None):
        return near(a, b)
    else:
        return True

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

    def part2(self) -> int:
        ti = 1
        for tj in range(2, 20):
            for i in range(len(self.stones)):
                for j in range(len(self.stones)):
                    #print("try", i, ti, j, tj)
                    v = self.try_vector(i, ti, j, tj)
                    if v is not None:
                        return v

        # Not solveable
        return -1
        
    def try_vector(self, i: int, ti: int, j: int, tj: int) -> typing.Optional[int]:
        # Determine vector that passes through i at ti, then j at tj
        # pxi + ti*vxi = pxa + ti*vxa   AND   pxj + tj*vxj = pxa + tj*vxa
        # pxi + ti*vxi - pxj - tj*vxj = pxa + ti*vxa - pxa - tj*vxa
        # pxi + ti*vxi - pxj - tj*vxj = (ti - tj)*vxa
        vxa = (self.stones[i].px + (ti * self.stones[i].vx)
                - self.stones[j].px - (tj * self.stones[j].vx)) / (ti - tj)
        vya = (self.stones[i].py + (ti * self.stones[i].vy)
                - self.stones[j].py - (tj * self.stones[j].vy)) / (ti - tj)
        vza = (self.stones[i].pz + (ti * self.stones[i].vz)
                - self.stones[j].pz - (tj * self.stones[j].vz)) / (ti - tj)
        pxa = self.stones[i].px + (ti * self.stones[i].vx) - (ti * vxa)
        pya = self.stones[i].py + (ti * self.stones[i].vy) - (ti * vya)
        pza = self.stones[i].pz + (ti * self.stones[i].vz) - (ti * vza)
        #print("try", i, j, pxa, pya, pza)

        # Does this work?
        for k in range(len(self.stones)):
            # pxk + tk*vxk = pxa + tk*vxa
            # (pxk - pxa) / (vxa - vxk) = tk
            tkx = tky = tkz = None
            if not near(vxa, self.stones[k].vx):
                tkx = (self.stones[k].px - pxa) / (vxa - self.stones[k].vx)
            if not near(vya, self.stones[k].vy):
                tky = (self.stones[k].py - pya) / (vya - self.stones[k].vy)
            if not near(vza, self.stones[k].vz):
                tkz = (self.stones[k].pz - pza) / (vza - self.stones[k].vz)
            if not (near_or_none(tkx, tky) and near_or_none(tky, tkz)
                    and near_or_none(tkx, tkz)):
                return None

        return pxa + pya + pza


if __name__ == "__main__":
    assert Problem("test").part1(7, 27) == 2
    bound1 = 200000000000000
    bound2 = 400000000000000
    print(Problem("input").part1(bound1, bound2))
    assert Problem("test").part2() == 47
    #print(Problem("input").part2())
