
from pathlib import Path
import unittest
import typing

def lanternfish(filename: Path, days: int) -> int:
    state = [int(x) for x in open(filename, "rt").read().split(",")]
    for day in range(days):
        for i in range(len(state)):
            if state[i] == 0:
                # spawn
                state.append(8)
                state[i] = 6
            else:
                state[i] -= 1

    return len(state)

def test_lanternfish_1() -> None:
    assert lanternfish(Path("part1test.txt"), 0) == 5
    assert lanternfish(Path("part1test.txt"), 1) == 5
    assert lanternfish(Path("part1test.txt"), 2) == 6
    assert lanternfish(Path("part1test.txt"), 3) == 7
    assert lanternfish(Path("part1test.txt"), 18) == 26
    assert lanternfish(Path("part1test.txt"), 80) == 5934

def main() -> None:
    print("part 1:", lanternfish(Path("part1.txt"), 80))
    #print("part 2:", lanternfish(Path("part1.txt"), False))

if __name__ == "__main__":
    main()


