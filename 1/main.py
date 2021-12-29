from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os

INPUT = Path("input")


def thing1(filename: Path) -> int:
    c = 0
    for a in open(filename, "rt").read():
        if a == "(":
            c += 1
        elif a == ")":
            c -= 1
    return c

def thing2(filename: Path) -> int:
    c = 0
    p = 0
    for a in open(filename, "rt").read():
        p += 1
        if a == "(":
            c += 1
        elif a == ")":
            c -= 1
        if c == -1:
            return p

    return -1

def main() -> None:
    answer = thing1(INPUT)
    print("part 1:", answer)

    answer = thing2(INPUT)
    print("part 2:", answer)


if __name__ == "__main__":
    main()


