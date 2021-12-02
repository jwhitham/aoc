
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

def multiply_horiz_and_depth_with_aim(filename: Path) -> int:
    horiz = 0
    depth = 0
    aim = 0
    for line in open(filename, "rt"):
        (cmd, arg) = line.split()
        value = int(arg)
        if cmd == "forward":
            horiz += value
            depth += aim * value
        elif cmd == "down":
            aim += value
        elif cmd == "up":
            aim -= value
        else:
            raise Exception("unknown command " + cmd)

    return horiz * depth

def test_multiply_horiz_and_depth_with_aim() -> None:
    assert multiply_horiz_and_depth_with_aim(Path("part1test.txt")) == 900


def main() -> None:
    print("part 1:", multiply_horiz_and_depth(Path("part1.txt")))
    print("part 2:", multiply_horiz_and_depth_with_aim(Path("part1.txt")))

if __name__ == "__main__":
    main()


