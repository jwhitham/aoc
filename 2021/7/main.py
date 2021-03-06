
from pathlib import Path
import unittest
import typing

def evaluate_fuel_cost_1(initial_state: typing.List[int], target: int) -> int:
    fuel = 0
    for pos in initial_state:
        fuel += abs(pos - target)
    return fuel

def crabs(filename: Path,
          evaluate_fuel_cost: typing.Callable[[typing.List[int], int], int]) -> int:

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
    assert evaluate_fuel_cost_1([16], 2) == 14
    assert evaluate_fuel_cost_1([16, 1], 2) == 15
    assert crabs(Path("part1test.txt"), evaluate_fuel_cost_1) == 37

def evaluate_fuel_cost_2(initial_state: typing.List[int], target: int) -> int:
    fuel = 0
    for pos in initial_state:
        distance = abs(pos - target)
        fuel += (distance * (distance + 1)) // 2
    return fuel

def test_crabs_2() -> None:
    assert evaluate_fuel_cost_2([5], 5) == 0
    assert evaluate_fuel_cost_2([4], 5) == 1
    assert evaluate_fuel_cost_2([3], 5) == 3
    assert evaluate_fuel_cost_2([2], 5) == 6
    assert evaluate_fuel_cost_2([1], 5) == 10
    assert evaluate_fuel_cost_2([0], 5) == 15
    assert evaluate_fuel_cost_2([16], 5) == 66
    assert evaluate_fuel_cost_2([14], 5) == 45
    assert crabs(Path("part1test.txt"), evaluate_fuel_cost_2) == 168

def main() -> None:
    print("part 1:", crabs(Path("part1.txt"), evaluate_fuel_cost_1))
    print("part 2:", crabs(Path("part1.txt"), evaluate_fuel_cost_2))

if __name__ == "__main__":
    main()


