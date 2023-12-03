
import re
from typing import Callable, Dict

def find_numbers(translate: Callable[[str], str], expr: str) -> int:
    find_first = re.compile(r"^.*?(" + expr + ").*$")
    find_last = re.compile(r"^.*(" + expr + ").*?$")
    total = 0
    for line in open("input", "rt"):
        first = find_first.match(line.strip())
        last = find_last.match(line.strip())
        if first and last:
            total += int(translate(first.group(1)) +
                            translate(last.group(1)), 10)
    return total

def part1() -> int:
    return find_numbers(lambda x: x, r"\d")

def part2() -> int:
    words = ["one", "two", "three",
             "four", "five", "six", "seven",
             "eight", "nine"]
    translate: Dict[str, str] = dict()
    for i in range(len(words)):
        translate[words[i]] = str(i + 1)
    return find_numbers(lambda x: translate.get(x, x),
                        r"\d|" + "|".join(words))

print(part1())
print(part2())
