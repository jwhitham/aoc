# python -m mypy main.py && python -m pytest main.py  && python main.py         
 
from pathlib import Path
import unittest
import typing


class Visits:
    def __init__(self) -> None:
        self.__visits: typing.Set[str] = set()

    def can_visit(self, name: str) -> bool:
        return not (name in self.__visits)

    def add(self, name: str) -> None:
        self.__visits.add(name)

    def remove(self, name: str) -> None:
        self.__visits.remove(name)


class Visits2(Visits):
    def __init__(self) -> None:
        Visits.__init__(self)
        self.__visits: typing.Set[str] = set()
        self.__double_visit: typing.Optional[str] = None

    def can_visit(self, name: str) -> bool:
        if not (name in self.__visits):
            return True

        if self.__double_visit is None:
            if name != "start":
                return True

        return False

    def add(self, name: str) -> None:
        if not (name in self.__visits):
            self.__visits.add(name)
            return

        if self.__double_visit is None:
            self.__double_visit = name
            return

    def remove(self, name: str) -> None:
        if self.__double_visit == name:
            assert name in self.__visits
            self.__double_visit = None
            return

        self.__visits.remove(name)


class Node:
    def __init__(self, name: str, visits: Visits) -> None:
        self.name = name
        self.visits = visits
        self.outs: typing.List[Node] = []
        self.small = (name.lower() == name)
        self.end = (self.name == "end")

    def add_edge(self, t: "Node") -> None:
        self.outs.append(t)
        t.outs.append(self)
       
    def find_paths_to_end(self) -> int:
        if self.end:
            return 1
        if not self.visits.can_visit(self.name):
            return 0

        if self.small:
            self.visits.add(self.name)

        total = 0
        for n2 in self.outs:
            total += n2.find_paths_to_end()

        if self.small:
            self.visits.remove(self.name)

        return total


def process(filename: Path, visits: Visits) -> int:
    nodes: typing.Dict[str, Node] = {}
    for line in open(filename, "rt"):
        (a, b) = line.strip().split("-")
        if not a in nodes:
            nodes[a] = Node(a, visits)
        if not b in nodes:
            nodes[b] = Node(b, visits)
        nodes[a].add_edge(nodes[b])
    return nodes["start"].find_paths_to_end()

def part_1(filename: Path) -> int:
    return process(filename, Visits())

def test_part_1() -> None:
    assert part_1(Path("test.txt")) == 10
    assert part_1(Path("test2.txt")) == 19
    assert part_1(Path("test3.txt")) == 226

def part_2(filename: Path) -> int:
    return process(filename, Visits2())

def test_part_2() -> None:
    assert part_2(Path("test.txt")) == 36
    assert part_2(Path("test2.txt")) == 103
    assert part_2(Path("test3.txt")) == 3509

def main() -> None:
    print("part 1:", part_1(Path("input.txt")))
    print("part 2:", part_2(Path("input.txt")))

if __name__ == "__main__":
    main()


