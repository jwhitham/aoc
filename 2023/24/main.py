
import typing
import re
import math

IntersectXY = typing.Optional[typing.Tuple[float, float]]
DEBUG = False
EPSILON = 1e-6


def round_epsilon(x: float) -> float:
    return math.floor((x / EPSILON) + 0.5) * EPSILON

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
        si = self.stones[0]
        sj = self.stones[1]
        sk = self.stones[2]
        ti = 1.0
        error2 = self.try_vector(self.get_line_a(si, ti, sj, 2.0), sk)
        error3 = self.try_vector(self.get_line_a(si, ti, sj, 3.0), sk)
        assert error2 is not None
        assert error3 is not None
        increasing_tj_makes_error_more_positive = (error3 > error2)
        min_tj = 0.0
        max_tj = 1e6
        while (max_tj - min_tj) > EPSILON:
            assert max_tj > min_tj
            tj = (max_tj + min_tj) * 0.5
            error = self.try_vector(self.get_line_a(si, ti, sj, tj), sk)
            assert error is not None, (max_tj, min_tj, tj)

            if (error < 0.0) == increasing_tj_makes_error_more_positive:
                max_tj = tj
            else:
                min_tj = tj

        # Now we have a fairly accurate idea of tj, we know what the line is...
        tj = round_epsilon(tj)
        sa = self.get_line_a(si, 1.0, sj, tj)
        print(str(sa))
        return int(round_epsilon(sa.px + sa.py + sa.pz))

    def get_line_a(self, si: Stone, ti: int, sj: Stone, tj: int) -> Stone:
        # Determine vector that passes through i at ti, then j at tj
        # pxi + ti*vxi = pxa + ti*vxa   AND   pxj + tj*vxj = pxa + tj*vxa
        # pxi + ti*vxi - pxj - tj*vxj = pxa + ti*vxa - pxa - tj*vxa
        # pxi + ti*vxi - pxj - tj*vxj = (ti - tj)*vxa
        vxa = (si.px + (ti * si.vx) - sj.px - (tj * sj.vx)) / (ti - tj)
        vya = (si.py + (ti * si.vy) - sj.py - (tj * sj.vy)) / (ti - tj)
        vza = (si.pz + (ti * si.vz) - sj.pz - (tj * sj.vz)) / (ti - tj)
        pxa = si.px + (ti * si.vx) - (ti * vxa)
        pya = si.py + (ti * si.vy) - (ti * vya)
        pza = si.pz + (ti * si.vz) - (ti * vza)
        return Stone(pxa, pya, pza, vxa, vya, vza)

    def get_tk(self, sa: Stone, sk: Stone) -> typing.Optional[int]:
        # Where does sa intersect with sk, considering only XY?
        ixya = sk.intersect_xy(sa)
        if ixya is None:
            return None

        (xa, ya) = ixya

        # pxa + tk*vxa = xa
        # pza + tk*vza = za
        tk = (xa - sa.px) / sa.vx
        return tk

    def try_vector(self, sa: Stone, sk: Stone) -> typing.Optional[int]:
        tk = self.get_tk(sa, sk)
        if tk is None:
            return None

        # What's Z on line a at the intersection?
        za = sa.pz + (tk * sa.vz)

        # What's Z on line k at the intersection?
        zk = sk.pz + (tk * sk.vz)

        # What's the error?
        return zk - za

if __name__ == "__main__":
    assert Problem("test").part1(7, 27) == 2
    bound1 = 200000000000000
    bound2 = 400000000000000
    print(Problem("input").part1(bound1, bound2))
    print(Problem("test").part2())
    assert Problem("test").part2() == 47
    print(Problem("input").part2())
