
from pathlib import Path
import unittest
import typing


CLOSING = {"(":")", "[":"]", "{":"}", "<":">"}
INCOMPLETE = "!"
COMPLETE = "."
SCORE = {")": 3, "]": 57, "}": 1197, ">": 25137}

def get_first_illegal_character(line: str) -> str:
    expect: typing.List[str] = []
    for ch in line:
        if ch in CLOSING:
            expect.append(CLOSING[ch])
        elif (len(expect) != 0) and (expect[-1] == ch):
            expect.pop()
        else:
            # corrupted line with illegal character
            return ch

    if len(expect) != 0:
        return INCOMPLETE
    else:
        return COMPLETE

def total_score(filename: Path) -> int:
    total = 0
    for line in open(filename, "rt"):
        ch = get_first_illegal_character(line.strip())
        if ch in SCORE:
            total += SCORE[ch]
    return total
    
def test_illegal() -> None:
    assert get_first_illegal_character("{([(<{}[<>[]}>{[]{[(<()>") == "}"
    assert get_first_illegal_character("[[<[([]))<([[{}[[()]]]") == ")"
    assert get_first_illegal_character("[{[{({}]{}}([{[{{{}}([]") == "]"
    assert get_first_illegal_character("[<(<(<(<{}))><([]([]()") == ")"
    assert get_first_illegal_character("<{([([[(<>()){}]>(<<{{") == ">"

def test_score() -> None:
    assert total_score(Path("part1test.txt")) == 26397

def main() -> None:
    print("part 1:", total_score(Path("part1.txt")))

if __name__ == "__main__":
    main()


