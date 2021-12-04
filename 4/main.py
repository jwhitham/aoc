
from pathlib import Path
import unittest
import typing

BOARD_SIZE = 5

class Board:
    def __init__(self) -> None:
        self.cols: typing.List[typing.Set[int]] = [
                set() for i in range(BOARD_SIZE)]
        self.rows: typing.List[typing.Set[int]] = [
                set() for i in range(BOARD_SIZE)]

    def remove(self, n: int) -> None:
        for col in self.cols:
            col.discard(n)
        for row in self.rows:
            row.discard(n)

    def is_empty(self) -> None:
        for col in self.cols:
            if len(col) == 0:
                return True
        for row in self.rows:
            if len(row) == 0:
                return True
        return False

    def total(self) -> int:
        t = 0
        for col in self.cols:
            t += sum(col)
        return t

def bingo_1(filename: Path) -> int:
    fd = open(filename, "rt")
    number_sequence = [int(x) for x in fd.readline().split(",")]
    boards: typing.List[Board] = []
    blank = fd.readline()
    while blank == "\n":
        b = Board()
        for i in range(BOARD_SIZE):
            row = [int(x) for x in fd.readline().split()]
            assert len(row) == BOARD_SIZE
            for j in range(BOARD_SIZE):
                b.cols[j].add(row[j])
                b.rows[i].add(row[j])

        boards.append(b)
        blank = fd.readline()

    for n in number_sequence:
        for b in boards:
            b.remove(n)
            if b.is_empty():
                return b.total() * n

    assert False, "no board finished"

def test_bingo_1() -> None:
    assert bingo_1(Path("part1test.txt")) == 4512

def main() -> None:
    print("part 1:", bingo_1(Path("part1.txt")))

if __name__ == "__main__":
    main()


