YEAR = 2019
DAY = 12
PART = 2
 
from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os
import re

INPUT = Path("input")

M = re.compile(r"^[<]x=(-*\d+), y=(-*\d+), z=(-*\d+)[>]\s*$")

class Moon:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.dx = 0
        self.dy = 0
        self.dz = 0

    def gravity(self, m2: "Moon") -> None:
        if m2.x < self.x:
            self.dx -= 1
        elif m2.x > self.x:
            self.dx += 1
        if m2.y < self.y:
            self.dy -= 1
        elif m2.y > self.y:
            self.dy += 1
        if m2.z < self.z:
            self.dz -= 1
        elif m2.z > self.z:
            self.dz += 1

    def velocity(self) -> None:
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz

    def energy(self) -> int:
        return ((abs(self.x) + abs(self.y) + abs(self.z)) 
            * (abs(self.dx) + abs(self.dy) + abs(self.dz)))

    def __str__(self) -> str:
        return "<x={}, y={}, z={}> <dx={}, dy={}, dz={}>".format(
               self.x, self.y, self.z, self.dx, self.dy, self.dz)

class MoonPlane:
    def __init__(self, x: int) -> None:
        self.x = x
        self.dx = 0

    def gravity(self, m2: "MoonPlane") -> None:
        if m2.x < self.x:
            self.dx -= 1
        elif m2.x > self.x:
            self.dx += 1

    def velocity(self) -> None:
        self.x += self.dx

    def state(self) -> typing.Tuple[int, int]:
        return (self.x, self.dx)

class Universe:
    def __init__(self, filename: Path) -> None:
        self.moons = []
        for line in open(filename, "rt"):
            m = M.match(line)
            assert m
            x = int(m.group(1))
            y = int(m.group(2))
            z = int(m.group(3))
            self.moons.append(Moon(x, y, z))

    def gravity(self) -> None:
        for m1 in self.moons:
            for m2 in self.moons:
                m1.gravity(m2)

    def velocity(self) -> None:
        for m1 in self.moons:
            m1.velocity()

    def energy(self) -> int:
        return sum([m1.energy() for m1 in self.moons])

    def __str__(self) -> str:
        return '\n'.join([str(m1) for m1 in self.moons])

    def how_long(self) -> int:
        moons_x = [MoonPlane(m.x) for m in self.moons]
        moons_y = [MoonPlane(m.y) for m in self.moons]
        moons_z = [MoonPlane(m.z) for m in self.moons]

        def calc_period(moons_x: typing.List[MoonPlane]) -> int:
            states = set()
            i = 0
            while True:
                state = tuple([mp.state() for mp in moons_x])
                if state in states:
                    return i
                states.add(state)
                i += 1
                for mp in moons_x:
                    for mp2 in moons_x:
                        mp.gravity(mp2)

                for mp in moons_x:
                    mp.velocity()


        px = calc_period(moons_x)
        py = calc_period(moons_y)
        pz = calc_period(moons_z)
        pxy = lcm(px, py)
        return lcm(pxy, pz)

def lcm(a, b):
    m = a * b
    if not m: return 0
    while True:
        a %= b
        if not a: return m // b
        b %= a
        if not b: return m // a


def test_part_1() -> None:
    u = Universe(Path("test"))
    print(str(u))
    u.gravity()
    u.velocity()
    print(str(u))
    u.gravity()
    u.velocity()
    print(str(u))

    for i in range(8):
        u.gravity()
        u.velocity()

    assert u.energy() == 179

    u = Universe(Path("test2"))
    for i in range(100):
        u.gravity()
        u.velocity()

    assert u.energy() == 1940

def thing1(filename: Path) -> int:
    u = Universe(filename)
    for i in range(1000):
        u.gravity()
        u.velocity()
    return u.energy()

def thing2(filename: Path) -> int:
    u = Universe(filename)
    return u.how_long()

def test_part_2() -> None:
    u = Universe(Path("test"))
    assert u.how_long() == 2772
    u = Universe(Path("test2"))
    assert u.how_long() == 4686774924

def main() -> None:
    if not INPUT.exists():
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY), "download"])
        return

    subprocess.check_call([sys.executable, "-m", "mypy", sys.argv[0]])
    subprocess.check_call([sys.executable, "-m", "pytest", sys.argv[0]])

    answer = thing1(INPUT)
    print("part 1:", answer)

    if PART == 1:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "1", str(answer)])
        return

    answer = thing2(INPUT)
    print("part 2:", answer)

    if PART == 2:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "2", str(answer)])
        return


if __name__ == "__main__":
    main()


