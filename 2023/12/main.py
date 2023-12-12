

class Arrangements:
    def __init__(self, line: str) -> None:
        (s_bits, s_counts) = line.split()
        self.true_counts = [int(x) for x in s_counts.split(",")]
        self.true_bits = list(s_bits)
        self.search_bits = []

    def search(self) -> int:
        bit_index = len(self.search_bits)
        total = 0
        if bit_index >= len(self.true_bits):
            total += 1
        elif self.true_bits[bit_index] == "?":
            self.search_bits.append("#")
            if self.is_valid():
                total += self.search()
            self.search_bits.pop()
            self.search_bits.append(".")
            if self.is_valid():
                total += self.search()
            self.search_bits.pop()
        else:
            self.search_bits.append(self.true_bits[bit_index])
            if self.is_valid():
                total += self.search()
            self.search_bits.pop()

        return total

    def is_valid(self) -> bool:
        bit_index = len(self.search_bits)
        count_index = 0
        group_size = 0
        for section in (self.search_bits, self.true_bits[bit_index:], "."):
            for bit in section:
                if bit == "#":
                    group_size += 1
                    if ((count_index >= len(self.true_counts))
                    or (group_size > self.true_counts[count_index])):
                        return False
                elif bit == ".":
                    if group_size:
                        assert count_index < len(self.true_counts)
                        if group_size != self.true_counts[count_index]:
                            return False
                        count_index += 1
                        group_size = 0
                else:
                    return True

        if (count_index == len(self.true_counts)) and (group_size == 0):
            return True
        else:
            return False
        

def arrangements(line: str) -> int:
    return Arrangements(line).search()

def part1() -> int:
    total = 0
    for line in open("input", "rt"):
        total += arrangements(line.strip())
    return total

if __name__ == "__main__":
    assert arrangements("???.### 1,1,3") == 1
    assert arrangements(".??..??...?##. 1,1,3") == 4
    assert arrangements("?#?#?#?#?#?#?#? 1,3,1,6") == 1
    assert arrangements("????.#...#... 4,1,1") == 1
    assert arrangements("????.######..#####. 1,6,5") == 4
    assert arrangements("?###???????? 3,2,1") == 10
    print(part1())
