YEAR = 2019
DAY = 2
PART = 3
 
from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os

INPUT = Path("input")

def thing1(filename: Path) -> int:
    memory = load(open(filename, "rt").read())
    memory[1] = 12
    memory[2] = 2
    return run(memory)

def load(prog: str) -> typing.Dict[int, int]:
    return {
            address: int(code)
            for (address, code) in enumerate(prog.strip().split(","))
            }

def run(memory: typing.Dict[int, int]) -> int:
    address = 0
    while True:
        opcode = memory[address]
        if opcode == 1:
            a = memory[address + 1]
            b = memory[address + 2]
            r = memory[address + 3]
            address += 4
            memory[r] = memory[a] + memory[b]
        elif opcode == 2:
            a = memory[address + 1]
            b = memory[address + 2]
            r = memory[address + 3]
            address += 4
            memory[r] = memory[a] * memory[b]
        elif opcode == 99:
            return memory[0]
        else:
            assert False, "invalid opcode {} at address {}".format(opcode, address)

def test_part_1() -> None:
    assert run(load("1,9,10,3,2,3,11,0,99,30,40,50")) == 3500
    assert run(load("1,0,0,0,99")) == 2
    assert run(load("2,3,0,3,99")) == 2
    assert run(load("2,4,4,0,99,0")) == 9801
    assert run(load("1,1,1,4,99,5,6,0,99")) == 30

def thing2(filename: Path) -> int:
    for noun in range(100):
        for verb in range(100):
            memory = load(open(filename, "rt").read())
            memory[1] = noun
            memory[2] = verb
            if run(memory) == 19690720:
                return (100 * noun) + verb

    assert False, "not found"

def main() -> None:
    if not INPUT.exists():
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY), "download"])
        return

    subprocess.check_call([sys.executable, "-m", "mypy", sys.argv[0]])
    subprocess.check_call([sys.executable, "-m", "pytest", sys.argv[0]])

    answer = thing1(INPUT)
    print("part 1:", answer)

    if PART == 1:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "1", str(answer)])
        return

    answer = thing2(INPUT)
    print("part 2:", answer)

    if PART == 2:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "2", str(answer)])
        return


if __name__ == "__main__":
    main()


