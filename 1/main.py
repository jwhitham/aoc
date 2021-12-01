
from pathlib import Path
import unittest

def count_depth_increase(filename: Path) -> int:
    depths = [int(line) for line in open(filename, "rt")]
    count = 0
    for i in range(1, len(depths)):
        if depths[i] > depths[i - 1]:
            count += 1

    return count

def test_count_depth_increase() -> None:
    assert count_depth_increase(Path("part1test.txt")) == 7

def count_depth_increase_with_window(filename: Path, window_size: int) -> int:
    depths = [int(line) for line in open(filename, "rt")]
    count = 0
    for i in range(1, len(depths)):
        if sum(depths[i:i + window_size]) > sum(depths[i - 1:i + window_size - 1]):
            count += 1

    return count

def test_count_depth_increase_with_window() -> None:
    assert count_depth_increase_with_window(Path("part1test.txt"), 1) == 7
    assert count_depth_increase_with_window(Path("part1test.txt"), 3) == 5

def main() -> None:
    print("part 1:", count_depth_increase(Path("part1.txt")))
    print("part 2:", count_depth_increase_with_window(Path("part1.txt"), 3))

if __name__ == "__main__":
    main()
