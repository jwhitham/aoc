from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os
import re

INPUT = Path("input")


def thing1(filename: Path) -> int:
    return len(visitor(open(filename, "rt").read()))

def visitor(moves: typing.List[str]) -> typing.Set[typing.Tuple[int, int]]:
    x = y = 0
    visited = set([(x, y)])
    for a in moves:
        if a == ">":
            x += 1
        elif a == "<":
            x -= 1
        elif a == "v":
            y += 1
        elif a == "^":
            y -= 1
        visited.add((x,y))
    return visited

def thing2(filename: Path) -> int:
    script = open(filename, "rt").read()
    return len(visitor(script[0::2]) | visitor(script[1::2]))

def main() -> None:
    answer = thing1(INPUT)
    print("part 1:", answer)

    answer = thing2(INPUT)
    print("part 2:", answer)


if __name__ == "__main__":
    main()


