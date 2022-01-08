
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

    def is_empty(self) -> bool:
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

def bingo(filename: Path, pick_first: bool) -> int:
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

    last_non_empty_board: typing.Optional[Board] = None
    for n in number_sequence:
        non_empty_board_count = 0
        for b in boards:
            b.remove(n)
            if b.is_empty():
                if pick_first or (b == last_non_empty_board):
                    return b.total() * n
            else:
                non_empty_board_count += 1
                last_non_empty_board = b

        if non_empty_board_count != 1:
            last_non_empty_board = None

    assert False, "no board finished"

def test_bingo_1() -> None:
    assert bingo(Path("part1test.txt"), True) == 4512

def test_bingo_2() -> None:
    assert bingo(Path("part1test.txt"), False) == 1924

def main() -> None:
    print("part 1:", bingo(Path("part1.txt"), True))
    print("part 2:", bingo(Path("part1.txt"), False))

if __name__ == "__main__":
    main()


