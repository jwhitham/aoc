
from pathlib import Path
import unittest
import typing


CLOSING = {"(":")", "[":"]", "{":"}", "<":">"}
INCOMPLETE = "!"
COMPLETE = "."
ILLEGAL_SCORE = {")": 3, "]": 57, "}": 1197, ">": 25137}

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

def total_illegal_score(filename: Path) -> int:
    total = 0
    for line in open(filename, "rt"):
        ch = get_first_illegal_character(line.strip())
        if ch in ILLEGAL_SCORE:
            total += ILLEGAL_SCORE[ch]
    return total
    
def test_illegal() -> None:
    assert get_first_illegal_character("{([(<{}[<>[]}>{[]{[(<()>") == "}"
    assert get_first_illegal_character("[[<[([]))<([[{}[[()]]]") == ")"
    assert get_first_illegal_character("[{[{({}]{}}([{[{{{}}([]") == "]"
    assert get_first_illegal_character("[<(<(<(<{}))><([]([]()") == ")"
    assert get_first_illegal_character("<{([([[(<>()){}]>(<<{{") == ">"

def test_illegal_score() -> None:
    assert total_illegal_score(Path("part1test.txt")) == 26397

COMPLETION_SCORE = {")": 1, "]": 2, "}": 3, ">": 4}

def get_completion(line: str) -> str:
    expect: typing.List[str] = []
    for ch in line:
        if ch in CLOSING:
            expect.append(CLOSING[ch])
        elif (len(expect) != 0) and (expect[-1] == ch):
            expect.pop()
        else:
            # corrupted line with illegal character - discard
            return ""

    return "".join(reversed(expect))

def get_completion_score(completion: str) -> int:
    total = 0
    for ch in completion:
        total *= 5
        total += COMPLETION_SCORE[ch]
    return total

def overall_completion_score(filename: Path) -> int:
    scores: typing.List[int] = []
    for line in open(filename, "rt"):
        v = get_completion_score(get_completion(line.strip()))
        if v != 0:
            scores.append(v)
    scores.sort()
    return scores[len(scores) // 2]
    
def test_completion() -> None:
    assert get_completion("[({(<(())[]>[[{[]{<()<>>") == "}}]])})]"
    assert get_completion("[(()[<>])]({[<{<<[]>>(") == ")}>]})"
    assert get_completion("(((({<>}<{<{<>}{[]{[]{}") == "}}>}>))))"
    assert get_completion("{<[[]]>}<{[{[{[]{()[[[]") == "]]}}]}]}>"
    assert get_completion("<{([{{}}[<[[[<>{}]]]>[]]") == "])}>"

def test_completion_score() -> None:
    assert get_completion_score("])}>") == 294
    assert get_completion_score("}}]])})]") == 288957
    assert get_completion_score(")}>]})") == 5566
    assert get_completion_score("}}>}>))))") == 1480781
    assert get_completion_score("]]}}]}]}>") == 995444
    assert overall_completion_score(Path("part1test.txt")) == 288957

def main() -> None:
    print("part 1:", total_illegal_score(Path("part1.txt")))
    print("part 2:", overall_completion_score(Path("part1.txt")))

if __name__ == "__main__":
    main()


