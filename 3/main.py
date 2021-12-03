
from pathlib import Path
import unittest
import collections
import typing

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

def get_rating(filename: Path, use_most_common: bool) -> int:
    report_data: typing.List[typing.List[bool]] = []
    for line in open(filename, "rt"):
        record = [b == "1" for b in line.strip()]
        report_data.append(record)

    assert len(report_data) > 0
    num_bits = len(report_data[0])
    for record in report_data:
        assert num_bits == len(record)

    for filter_bit in range(num_bits):

        if len(report_data) <= 1:
            break

        ones = zeroes = 0
        for record in report_data:
            if record[filter_bit]:
                ones += 1
            else:
                zeroes += 1

        bit = ((ones >= zeroes) != use_most_common)

        filter_out: typing.List[typing.List[bool]] = []
        for record in report_data:
            if record[filter_bit] == bit:
                filter_out.append(record)

        report_data = filter_out

    assert len(report_data) == 1
    mask = 1 << num_bits
    value = 0
    for i in range(num_bits):
        mask = mask >> 1
        if report_data[0][i]:
            value |= mask

    return value

def life_support(filename: Path) -> int:
    oxygen = get_rating(filename, True)
    co2 = get_rating(filename, False)
    return oxygen * co2

def test_life_support() -> None:
    assert life_support(Path("part1test.txt")) == 230


def main() -> None:
    print("part 1:", power_consumption(Path("part1.txt")))
    print("part 2:", life_support(Path("part1.txt")))

if __name__ == "__main__":
    main()


