# python -m mypy main.py && python -m pytest main.py  && python main.py         
 
from pathlib import Path
import unittest
import typing

def thing1(filename: Path) -> int:
    return 0

def test_part_1() -> None:
    assert thing1(Path("input.txt")) == 1234

def thing2(filename: Path) -> int:
    return 0

def test_part_2() -> None:
    assert thing2(Path("input.txt")) == 1234

def main() -> None:
    print("part 1:", thing1(Path("input.txt")))
    print("part 2:", thing2(Path("input.txt")))

if __name__ == "__main__":
    main()


