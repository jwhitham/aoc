from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os
import re
import hashlib

INPUT = Path("input")

def vowels(line: str) -> bool:
    c = 0
    for a in line:
        if a in "aeiou":
            c += 1
            if c >= 3:
                return True

    return False

def repeats(line: str) -> bool:
    for i in range(1, len(line)):
        if line[i] == line[i - 1]:
            return True

    return False

BAD = re.compile(r"^.*(ab|cd|pq|xy).*$")

def baddies(line: str) -> bool:
    return (BAD.match(line) is not None)

def thing1(filename: Path) -> int:
    count = 0
    for line in open(filename, "rt"):
        line = line.strip()
        if vowels(line) and repeats(line) and not baddies(line):
            count += 1
    return count

def pairs(line: str) -> bool:
    pair_index = {}
    for i in range(0, len(line) - 1):
        pair = line[i:i + 2]
        previous = pair_index.get(pair, -1)
        if previous >= 0:
            if previous < (i - 1):
                return True
        else:
            pair_index[pair] = i

    return False

def repeats2(line: str) -> bool:
    for i in range(2, len(line)):
        if line[i] == line[i - 2]:
            return True

    return False

def thing2(filename: Path) -> int:
    assert pairs("qjhvhtzxzqqjkmpb")
    assert pairs("xxyxx")
    assert pairs("uurcxstgmygtbstg")
    assert not pairs("ieodomkazucvgmuy")
    assert not pairs("xxx")
    assert pairs("xxxx")
    count = 0
    for line in open(filename, "rt"):
        line = line.strip()
        if pairs(line) and repeats2(line):
            count += 1
    return count

def main() -> None:
    answer = thing1(INPUT)
    print("part 1:", answer)

    answer = thing2(INPUT)
    print("part 2:", answer)


if __name__ == "__main__":
    main()


