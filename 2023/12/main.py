

import typing

class SearchState:
    count_index: int
    group_size: int
    bit_index: int

    @staticmethod
    def new() -> "SearchState":
        c = SearchState()
        c.count_index = 0
        c.group_size = 0
        c.bit_index = -1
        return c

    def key(self) -> typing.Tuple[int, int, int]:
        return (self.count_index, self.group_size, self.bit_index)

    def copy(self) -> "SearchState":
        c = SearchState()
        c.count_index = self.count_index
        c.group_size = self.group_size
        c.bit_index = self.bit_index
        return c

    def done(self, problem: "Arrangements") -> bool:
        return ((self.count_index == len(problem.true_counts))
            or ((self.count_index == (len(problem.true_counts) - 1))
                and self.group_size == problem.true_counts[-1]))

    def test(self, problem: "Arrangements", bit: str) -> typing.Optional["SearchState"]:
        c = self.copy()
        c.bit_index += 1
        assert c.bit_index >= 0
        assert c.bit_index < len(problem.true_bits)
        if bit == "#":
            c.group_size += 1
            if ((c.count_index >= len(problem.true_counts))
            or (c.group_size > problem.true_counts[c.count_index])):
                return None
        elif bit == ".":
            if c.group_size:
                assert c.count_index < len(problem.true_counts)
                if c.group_size != problem.true_counts[c.count_index]:
                    return None
                c.count_index += 1
                c.group_size = 0
        else:
            assert False

        return c

class Arrangements:
    def __init__(self, line: str) -> None:
        (s_bits, s_counts) = line.split()
        self.true_counts = [int(x) for x in s_counts.split(",")]
        self.true_bits = list(s_bits)
        self.memo: typing.Dict[typing.Tuple, int] = {}

    def part2_multiply(self, factor: int) -> "Arrangements":
        original_counts = self.true_counts[:]
        for i in range(factor - 1):
            self.true_counts.extend(original_counts)

        original_bits = self.true_bits[:]
        for i in range(factor - 1):
            self.true_bits.append("?")
            self.true_bits.extend(original_bits)

        return self

    def search(self) -> int:
        return self.count(SearchState.new())

    def count(self, parent: SearchState) -> int:
        key = parent.key()
        value = self.memo.get(key, -1)
        if value >= 0:
            return value

        bit_index = parent.bit_index + 1
        total = 0
        if bit_index >= len(self.true_bits):
            if parent.done(self):
                total += 1
        elif self.true_bits[bit_index] == "?":
            child = parent.test(self, "#")
            if child:
                total += self.count(child)
            child = parent.test(self, ".")
            if child:
                total += self.count(child)
        else:
            child = parent.test(self, self.true_bits[bit_index])
            if child:
                total += self.count(child)

        self.memo[key] = total
        return total

def arrangements(line: str) -> int:
    return Arrangements(line).search()

def part1() -> int:
    total = 0
    for line in open("input", "rt"):
        total += arrangements(line.strip())
    return total

def arrangements2(line: str) -> int:
    return Arrangements(line).part2_multiply(5).search()

def part2() -> int:
    total = 0
    for line in open("input", "rt"):
        total += arrangements2(line.strip())
    return total

if __name__ == "__main__":
    assert arrangements("???.### 1,1,3") == 1
    assert arrangements(".??..??...?##. 1,1,3") == 4
    assert arrangements("?#?#?#?#?#?#?#? 1,3,1,6") == 1
    assert arrangements("????.#...#... 4,1,1") == 1
    assert arrangements("????.######..#####. 1,6,5") == 4
    assert arrangements("?###???????? 3,2,1") == 10
    print(part1(), flush=True)
    assert part1() == 7090
    assert arrangements2("???.### 1,1,3") == 1
    assert arrangements2(".??..??...?##. 1,1,3") == 16384
    assert arrangements2("?#?#?#?#?#?#?#? 1,3,1,6") == 1
    assert arrangements2("????.#...#... 4,1,1") == 16
    assert arrangements2("????.######..#####. 1,6,5") == 2500
    assert arrangements2("?###???????? 3,2,1") == 506250
    print(part2(), flush=True)
