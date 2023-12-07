
import collections

CARD_VALUE = {
    "A": 64,
    "K": 63,
    "Q": 62,
    "J": 61,
    "T": 60,
    }

class Hand1:
    def __init__(self, contents: str) -> None:
        self.contents = contents

        self.strength = self.evaluate_strength(contents)

    def evaluate_card(self, sk: str) -> int:
        return CARD_VALUE.get(sk, ord(sk))

    def evaluate_strength(self, contents: str) -> int:
        contents2 = {}
        for x in contents:
            contents2[x] = 1 + contents2.get(x, 0)
        contents3 = sorted(contents2.values())

        kind5 = (contents3 == [5])
        kind4 = (contents3 == [1, 4])
        fh = (contents3 == [2, 3])
        kind3 = (contents3 == [1, 1, 3])
        pair2 = (contents3 == [1, 2, 2])
        pair1 = (contents3 == [1, 1, 1, 2])

        if kind5:
            return 6 
        elif kind4:
            return 5
        elif fh:
            return 4
        elif kind3:
            return 3
        elif pair2:
            return 2
        elif pair1:
            return 1
        else:
            return 0

    def __repr__(self) -> str:
        return "Hand({}, s={})".format(self.contents, self.strength)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Hand1):
            return False
        if self.strength < other.strength:
            return True
        if self.strength > other.strength:
            return False

        for i in range(5):
            sv = self.evaluate_card(self.contents[i])
            ov = self.evaluate_card(other.contents[i])
            if sv < ov:
                return True
            if sv > ov:
                return False

        return False

class Hand2(Hand1):
    def evaluate_card(self, sk: str) -> int:
        if sk == "J":
            return 0
        return Hand1.evaluate_card(self, sk)

    def evaluate_strength(self, contents: str) -> int:
        def test_jokers(contents: str, index: int) -> int:
            while (index < len(contents)) and (contents[index] != "J"):
                index += 1
            if index >= len(contents):
                return Hand1.evaluate_strength(self, contents)
          
            best = 0
            for test in "23456789TQKA":
                contents = contents[:index] + test + contents[index + 1:]
                best = max(best, test_jokers(contents, index + 1))
            return best

        return test_jokers(contents, 0)


def part(fname, cls):
    rank = []
    for line in open(fname, "rt"):
        (contents, bid) = line.split()
        rank.append((cls(contents), int(bid)))

    rank.sort()
    total = 0
    for (value, (hand, bid)) in enumerate(rank):
        total += bid * (value + 1)
        
    return total

def main():
    assert part("test", Hand1) == 6440
    print(part("input", Hand1))
    assert part("test", Hand2) == 5905
    print(part("input", Hand2))

if __name__ == "__main__":
    main()
