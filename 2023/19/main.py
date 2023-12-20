

import re
import typing

PARSE_WORKFLOW = re.compile(r"^(\w+){(.+)}\s*$")

class Workflow:
    def __init__(self, text: str) -> None:
        m = PARSE_WORKFLOW.match(text)
        assert m is not None, text
        self.name = m.group(1)
        self.rules = [Rule(subtext) for subtext in m.group(2).split(",")]

PARSE_RULE = re.compile(r"^((\w+)([<>])(\d+):|)(\w+)$")

class Rule:
    def __init__(self, text: str) -> None:
        m = PARSE_RULE.match(text)
        assert m is not None, text
        if m.group(1) != "":
            self.category = m.group(2)
            self.operator = m.group(3)
            self.value = int(m.group(4))
        else:
            self.category = self.operator = ""
            self.value = 0
        self.dest = m.group(5)

    def match(self, part: "Part") -> bool:
        if self.operator == "":
            return True
        elif self.operator == ">":
            return part.data[self.category] > self.value
        elif self.operator == "<":
            return part.data[self.category] < self.value
        else:
            assert False

    def match2(self, part_group: "PartGroup") -> typing.Tuple["PartGroup", "PartGroup"]:
        if self.operator == "":
            true_copy = part_group.copy()
            false_copy = PartGroup()
            return (true_copy, false_copy)

        true_copy = part_group.copy()
        false_copy = part_group.copy()
        true_copy.data[self.category] = set()
        false_copy.data[self.category] = set()
        if self.operator == ">":
            for item in part_group.data[self.category]:
                if item > self.value:
                    true_copy.data[self.category].add(item)
                else:
                    false_copy.data[self.category].add(item)
        else:
            assert self.operator == "<"
            for item in part_group.data[self.category]:
                if item < self.value:
                    true_copy.data[self.category].add(item)
                else:
                    false_copy.data[self.category].add(item)

        if len(true_copy.data[self.category]) == 0:
            true_copy = PartGroup()
        if len(false_copy.data[self.category]) == 0:
            false_copy = PartGroup()
        return (true_copy, false_copy)

        
PARSE_PART = re.compile(r"^{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}$")

class Part:
    def __init__(self, text: str) -> None:
        m = PARSE_PART.match(text)
        assert m is not None, text
        self.data = {
            "x": int(m.group(1)),
            "m": int(m.group(2)),
            "a": int(m.group(3)),
            "s": int(m.group(4)),
        }

    def value(self) -> int:
        return sum(self.data.values())

class PartGroup:
    def __init__(self) -> None:
        self.data: typing.Dict[str, typing.Set[int]] = {k: set() for k in "xmas"}

    def copy(self) -> "PartGroup":
        out = PartGroup()
        out.data = {k: set(self.data[k]) for k in "xmas"}
        return out

    def fill(self) -> None:
        for k in self.data:
            self.data[k] = set(range(1, 4001))

    def is_empty(self) -> bool:
        for k in self.data:
            if len(self.data[k]) == 0:
                return True
        return False

    def value(self) -> int:
        total = 1
        for k in self.data:
            total *= len(self.data[k])
        return total

class Part1:
    def __init__(self, fname: str) -> None:
        self.workflows: typing.Dict[str, Workflow] = {}
        self.parts: typing.List[Part] = []
        gap_reached = False
        for line in open(fname, "rt"):
            line = line.strip()
            if line == "":
                gap_reached = True
            elif not gap_reached:
                w = Workflow(line)
                self.workflows[w.name] = w
            else:
                self.parts.append(Part(line))

        assert "in" in self.workflows

    def part1(self) -> int:
        total = 0
        for part in self.parts:
            w_name = "in"
            while True:
                assert w_name in self.workflows
                w = self.workflows[w_name]
                w_name = ""
                for r in w.rules:
                    if r.match(part):
                        w_name = r.dest
                        break

                assert w_name
                if w_name == "A":
                    total += part.value()
                    break
                elif w_name == "R":
                    break

        return total

class Part2(Part1):
    def send_to_workflow(self, name: str, part_group: PartGroup) -> int:
        if name == "A":
            return part_group.value()
        if name == "R" or part_group.is_empty():
            return 0

        total = 0
        carried = part_group.copy()
        for r in self.workflows[name].rules:
            (branched, carried) = r.match2(carried)
            total += self.send_to_workflow(r.dest, branched)

        assert carried.is_empty()
        return total

    def part2(self) -> int:
        initial = PartGroup()
        initial.fill()
        return self.send_to_workflow("in", initial)

def main() -> None:
    assert Part1("test").part1() == 19114
    print(Part1("input").part1())
    assert Part2("test").part2() == 167409079868000
    print(Part2("input").part2())

if __name__ == "__main__":
    main()
