
import collections

def part1(fname):
    total = 0
    for line in open(fname, "rt"):
        (_, _, s_numbers) = line.rstrip().partition(":")
        (s_winning, _, s_have) = s_numbers.partition("|")

        winning = [int(s) for s in s_winning.split()]
        have = set([int(s) for s in s_have.split()])

        match = 0
        for n in winning:
            if n in have:
                match += 1

        if match > 0:
            total += 2 ** (match - 1)
        
    return total

def part2(fname):
    count = collections.defaultdict(lambda: 1)
    for (i, line) in enumerate(open(fname, "rt")):
        s_card = i + 1
        (_, _, s_numbers) = line.rstrip().partition(":")
        (s_winning, _, s_have) = s_numbers.partition("|")
        winning = [int(s) for s in s_winning.split()]
        have = set([int(s) for s in s_have.split()])
        count[s_card] += 0
        match = 0
        for n in winning:
            if n in have:
                match += 1

        for n in range(match):
            count[n + 1 + s_card] += count[s_card]

    return sum(count.values())

def main():
    assert part1("test") == 13
    print(part1("input"))
    print(part2("test"))
    assert part2("test") == 30
    print(part2("input"))

if __name__ == "__main__":
    main()
