
import typing
import collections


class Pattern:
    def __init__(self) -> None:
        self.col_value: typing.Dict[int, int] = collections.defaultdict(lambda: 0)
        self.row_value: typing.Dict[int, int] = collections.defaultdict(lambda: 0)
        self.width = 0
        self.height = 0

    def add(self, line: str) -> None:
        y = self.height
        for (x, col) in enumerate(line):
            if col == "#":
                self.col_value[x] |= 1 << y
                self.row_value[y] |= 1 << x

        self.width = max(self.width, len(line))
        self.height += 1

    def detect_reflection(self,
            size: int, within: typing.Dict[int, int]) -> typing.List[int]:
        reflection = []
        for mid in range(1, size):
            bad = False
            for delta in range(size):
                x1 = mid - delta - 1
                x2 = mid + delta
                if not (0 <= x1 and x2 < size):
                    break
                if within[x2] != within[x1]:
                    bad = True
                    break
            if not bad:
                reflection.append(mid)
        return reflection

    def compute(self) -> int:
        col = self.detect_reflection(self.width, self.col_value)
        row = self.detect_reflection(self.height, self.row_value)
        return sum(col) + (100 * sum(row))
                
class Pattern2(Pattern):
    def detect_reflection(self,
            size: int, within: typing.Dict[int, int]) -> typing.List[int]:
        reflection = []
        for mid in range(1, size):
            errors = 0
            for delta in range(size):
                x1 = mid - delta - 1
                x2 = mid + delta
                if not (0 <= x1 and x2 < size):
                    break
                compare = within[x2] ^ within[x1]
                while compare != 0:
                    if compare & 1:
                        errors += 1
                    compare = compare >> 1

                if errors > 1:
                    break
            if errors == 1:
                reflection.append(mid)
        return reflection

def part(pattern_class, fname: str) -> int:
    total = 0
    pattern = pattern_class()
    for line in open(fname, "rt"):
        line = line.rstrip()
        if line != "":
            pattern.add(line)
        else:
            total += pattern.compute()
            pattern = pattern_class()
    total += pattern.compute()
    return total

def main():
    assert part(Pattern, "test") == 405
    print(part(Pattern, "input"))
    assert part(Pattern2,"test") == 400
    print(part(Pattern2, "input"))

if __name__ == "__main__":
    main()
