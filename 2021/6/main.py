
from pathlib import Path
import unittest
import typing

NUM_STATES = 9

def lanternfish(filename: Path, days: int) -> int:
    initial_state = [int(x) for x in open(filename, "rt").read().split(",")]
    count_for_state = [0 for i in range(NUM_STATES)]
    for i in range(len(initial_state)):
        count_for_state[initial_state[i]] += 1

    for day in range(days):
        # rotate and deal with every fish in state 0
        number_spawning = count_for_state.pop(0)
        count_for_state[6] += number_spawning   # existing fish return to state 6
        count_for_state.append(number_spawning) # new fish added to state 8

    return sum(count_for_state)

def test_lanternfish_1() -> None:
    assert lanternfish(Path("part1test.txt"), 0) == 5
    assert lanternfish(Path("part1test.txt"), 1) == 5
    assert lanternfish(Path("part1test.txt"), 2) == 6
    assert lanternfish(Path("part1test.txt"), 3) == 7
    assert lanternfish(Path("part1test.txt"), 18) == 26
    assert lanternfish(Path("part1test.txt"), 80) == 5934

def test_lanternfish_2() -> None:
    assert lanternfish(Path("part1test.txt"), 256) == 26984457539

def main() -> None:
    print("part 1:", lanternfish(Path("part1.txt"), 80))
    print("part 2:", lanternfish(Path("part1.txt"), 256))

if __name__ == "__main__":
    main()


