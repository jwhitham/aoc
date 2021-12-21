YEAR = 2021
DAY = 21
PART = 3
 
from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os

INPUT = Path("input")

class D:
    def __init__(self) -> None:
        self.v = 0
        self.c = 0

    def get(self) -> int:
        self.c += 1
        self.v += 1
        self.v %= 100
        if self.v == 0:
            return 100
        else:
            return self.v

class P:
    # Time cost: too much OO?
    # I thought most likely the second part would be a game with
    # more complex rules so I intended to allow the player and the
    # dice to be replaced. Actually the rules were more complex in
    # an unexpected way, and having a player class (P) was not helpful.
    # Probably the dice class (D) was also useless.
    def __init__(self, p) -> None:
        self.s = 0
        self.p = p

    def move(self, d) -> None:
        r = d.get() + d.get() + d.get()
        self.p += r
        self.p %= 10
        if self.p == 0:
            self.s += 10
        else:
            self.s += self.p

    def get(self, d):
        self.move(d)
        if self.p == 0:
            return (10, self.s)
        else:
            return (self.p, self.s)

def test_part_1() -> None:
    # Time cost: too many tests?
    # Having got a number of wrong answers on the previous day
    # I was keen to write lots of test cases this time, and
    # this was possibly a bad idea as the first part was not very
    # hard. However, I did get the right answer on the first attempt,
    # and maybe I would not have done if I had not bothered with
    # these tests.
    p1 = P(4)
    p2 = P(8)
    d = D()
    assert p1.get(d) == (10 , 10)
    assert p2.get(d) == (3 , 3)
    assert p1.get(d) == (4 , 14)
    assert p2.get(d) == (6 , 9)
    assert p1.get(d) == (6 , 20)
    assert p2.get(d) == (7 , 16)
    assert p1.get(d) == (6 , 26)
    assert p2.get(d) == (6 , 22)

def determ(p1s: int, p2s: int) -> int:
    p1 = P(p1s)
    p2 = P(p2s)
    d = D()
    while True:
        p1.get(d)
        if p1.s >= 1000:
            break
        p2.get(d)
        if p2.s >= 1000:
            break
    return d.c * min(p2.s, p1.s)

def thing1():
    return determ(1, 3)

def test_part_1a() -> None:
    assert determ(4, 8) == 993 * 745

class DR(D):
    def __init__(self, v):
        self.v = v

    def get(self):
        a = self.v % 3
        self.v = self.v // 3
        return a + 1


def dirac(p1: int, p2: int):
    d = DR(0)
    rp1 = P(0)
    rp2 = P(0)

    state = collections.defaultdict(lambda: 0)
    state[(p1, 0, p2, 0)] = 1
    p1win = 0
    p2win = 0

    while len(state) != 0:
        new_state = collections.defaultdict(lambda: 0)
        print(len(state), p1win, p2win, flush=True)

        # My solution is iterative but I saw others use a recursive
        # solution which allows the use of @functools.cache to
        # automatically memoize the final results for a game state.
        # This helps because some game states can be reached by more
        # than one path.
        for ((p1, s1, p2, s2), count) in state.items():
            assert s1 < 21
            assert s2 < 21

            # On Reddit I saw a nice trick for the dice rolls was to use
            # itertools.product([1,2,3],repeat=3) to get a Cartesian
            # product of all possible rolls.
            # But better still, precompute the possible outcomes of
            # rolling 3d3.
            for value1 in range(3 ** 3):
                # Time cost: saving and restoring the state like this
                # is painful and would be avoided by using simpler
                # functions to compute the next state.
                rp1.p = p1
                rp1.s = s1
                d.v = value1
                rp1.move(d)
                ap1 = rp1.p
                as1 = rp1.s
                # Time cost: made a mistake here by accidentally
                # restoring the state into (p1, s1, p2, s2), overwriting
                # them for the next iteration.
                assert as1 > s1
                assert d.v == 0
                if as1 < 21:
                    # Time cost: You only roll the dice for player 2
                    # if player 1 has not already won. When I used 3 ** 6
                    # in the outer loop, I pre-determined
                    # all 6 dice rolls, creating too many universes.
                    # This gives the correct answer for p2win but not
                    # p1win. I have seen other people made this mistake
                    # and it puzzled them too.
                    for value2 in range(3 ** 3):
                        rp2.p = p2
                        rp2.s = s2
                        d.v = value2
                        rp2.move(d)
                        ap2 = rp2.p
                        as2 = rp2.s
                        assert as2 > s2
                        assert d.v == 0
                        if as2 < 21:
                            new_state[(ap1, as1, ap2, as2)] += count
                        else:
                            p2win += count
                else:
                    p1win += count
        state = new_state

    return (p1win, p2win)

def test_thing2():
    (p1win, p2win) = dirac(4, 8)
    assert p1win == 444356092776315, p1win
    assert p2win == 341960390180808, p2win

def thing2():
    (p1win, p2win) = dirac(1, 3)
    return max(p1win, p2win)

def main() -> None:
    if not INPUT.exists():
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY), "download"])
        return

    subprocess.check_call([sys.executable, "-m", "pytest", sys.argv[0]])

    answer = thing1()
    print("part 1:", answer)

    if PART == 1:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "1", str(answer)])
        return

    answer = thing2()
    print("part 2:", answer)

    if PART == 2:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "2", str(answer)])
        return


if __name__ == "__main__":
    main()


