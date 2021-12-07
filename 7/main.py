
from pathlib import Path
import unittest
import typing

def evaluate_fuel_cost(initial_state: typing.List[int], target: int) -> int:
    fuel = 0
    for pos in initial_state:
        fuel += abs(pos - target)
    return fuel

def crabs(filename: Path) -> int:
    initial_state = [int(x) for x in open(filename, "rt").read().split(",")]
    left = min(initial_state)
    right = max(initial_state)
    while left < right:
        mid = (left + right) // 2
        left_cost = evaluate_fuel_cost(initial_state, mid)
        right_cost = evaluate_fuel_cost(initial_state, mid + 1)
        if left_cost < right_cost:
            right = mid
        else:
            left = mid + 1

    assert left == right
    return evaluate_fuel_cost(initial_state, left)

def test_crabs_1() -> None:
    assert evaluate_fuel_cost([16], 2) == 14
    assert evaluate_fuel_cost([16, 1], 2) == 15
    assert crabs(Path("part1test.txt")) == 37

def main() -> None:
    print("part 1:", crabs(Path("part1.txt")))

if __name__ == "__main__":
    main()


