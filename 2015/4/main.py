from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os
import re
import hashlib

INPUT = b"ckczppom"
CACHE = {}
BASE = hashlib.md5()
BASE.update(INPUT)
MAX_CACHE = 100000

def find(number):
    hit = CACHE.get(number, None)
    if hit:
        return hit

    if number < 10:
        miss = BASE.copy()
    else:
        miss = find(number // 10).copy()

    miss.update(bytes([(number % 10) + 48]))
    CACHE[number] = miss
    if len(CACHE) > MAX_CACHE:
        CACHE.clear()

    return miss


def thing1(filename: Path) -> int:
    number = 0
    while True:
        now = find(number)
        if now.hexdigest()[:5] == "00000":
            return number
        number += 1

def thing2(filename: Path) -> int:
    number = 0
    while True:
        now = find(number)
        if now.hexdigest()[:6] == "000000":
            return number
        number += 1
    return 0

def main() -> None:
    answer = thing1(INPUT)
    print("part 1:", answer)

    answer = thing2(INPUT)
    print("part 2:", answer)


if __name__ == "__main__":
    main()


