
from pathlib import Path
import unittest
import collections

def power_consumption(filename: Path) -> int:
    bits = ""
    for line in open(filename, "rt"):
        num_bits = len(line.strip())
        break

    ones = [0 for i in range(num_bits)]
    zeroes = [0 for i in range(num_bits)]
    for line in open(filename, "rt"):
        bits = line.strip()
        for i in range(num_bits):
            if bits[i] == "1":
                ones[i] += 1
            else:
                zeroes[i] += 1

    gamma = 0
    epsilon = 0
    mask = 1 << num_bits
    for i in range(num_bits):
        mask = mask >> 1
        if ones[i] > zeroes[i]:
            gamma |= mask
        if ones[i] < zeroes[i]:
            epsilon |= mask

    return gamma * epsilon

def test_power_consumption() -> None:
    assert power_consumption(Path("part1test.txt")) == 198


def main() -> None:
    print("part 1:", power_consumption(Path("part1.txt")))

if __name__ == "__main__":
    main()


