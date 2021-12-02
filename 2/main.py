
from pathlib import Path
import unittest

def multiply_horiz_and_depth(filename: Path) -> int:
    horiz = 0
    depth = 0
    for line in open(filename, "rt"):
        (cmd, arg) = line.split()
        value = int(arg)
        if cmd == "forward":
            horiz += value
        elif cmd == "down":
            depth += value
        elif cmd == "up":
            depth -= value
        else:
            raise Exception("unknown command " + cmd)

    return horiz * depth

def test_multiply_horiz_and_depth() -> None:
    assert multiply_horiz_and_depth(Path("part1test.txt")) == 150


def main() -> None:
    print("part 1:", multiply_horiz_and_depth(Path("part1.txt")))

if __name__ == "__main__":
    main()


