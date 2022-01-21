
import typing

LOWEST = ord("a")
HIGHEST = ord("z")
SIZE = 8

class PassCounter:
    def __init__(self, value: str) -> None:
        self.value: typing.List[int] = [ord(x) for x in value]
        assert len(self.value) == SIZE

    def first_invalid(self) -> int:
        return SIZE

    def increment(self, position) -> bool:
        assert 0 <= position < SIZE

        # reset following
        for i in range(position + 1, SIZE):
            self.value[i] = LOWEST

        while position >= 0:
            # increment
            self.value[position] += 1

            if self.value[position] <= HIGHEST:
                return False

            # carry
            self.value[position] = LOWEST
            position -= 1

        # overflow
        return True
   
    def increment_find_next(self) -> bool:
        overflow = False
        if self.increment(SIZE - 1):
            overflow = True
            
        while True:
            i = self.first_invalid()
            if i >= SIZE:
                return overflow # fully valid

            # invalid number found, skip forwards
            if self.increment(i):
                overflow = True

    def __str__(self) -> str:
        return ''.join([chr(x) for x in self.value])


class TestPassCounter(PassCounter):
    def first_invalid(self) -> int:
        for i in range(SIZE - 2):
            if self.value[i] == self.value[i+1] == self.value[i+2]:
                return i + 2

        return SIZE


NOT_ALLOWED = set([ord("i"), ord("o"), ord("l")])

class Part1Rules(PassCounter):
    def first_invalid(self) -> int:
        bad = pair1 = pair2 = SIZE
        # Passwords may not contain the letters i, o, or l, as these
        # letters can be mistaken for other characters and are therefore
        # confusing.
        for i in range(SIZE):
            if self.value[i] in NOT_ALLOWED:
                bad = min(bad, i)

        # Passwords must contain at least two different, non-overlapping
        # pairs of letters, like aa, bb, or zz.
        # First pair would have to appear at position 4,5 or earlier.
        for i in range(SIZE - 3):
            if self.value[i] == self.value[i+1]:
                pair1 = i
                break

        if pair1 >= SIZE:
            bad = min(bad, SIZE - 3)
        else:
            # Second pair would have to appear at or before position 6,7
            # Second pair would have to appear after first pair
            for i in range(pair1 + 2, SIZE - 1):
                if ((self.value[i] == self.value[i+1])
                and (self.value[i] != self.value[pair1])):
                    pair2 = i
                    break
            if pair2 >= SIZE:
                bad = min(bad, SIZE - 1)

        # Passwords must include one increasing straight of at least
        # three letters, like abc, bcd, cde, and so on, up to xyz.
        # They cannot skip letters; abd doesn't count.
        for i in range(SIZE - 2):
            if self.value[i] == (self.value[i+1] - 1):
                if self.value[i] == (self.value[i+2] - 2):
                    # requirement is met
                    bad_straight = SIZE
                    break
                else:
                    # third letter is wrong
                    bad_straight = i + 2
            else:
                # second letter is wrong
                bad_straight = i + 1

        if bad_straight < SIZE:
            bad = min(bad, bad_straight, SIZE - 2)

        return bad


def test1() -> None:
    # test detection of the three identical items
    x = TestPassCounter("abcdghhh")
    assert x.first_invalid() == SIZE - 1
    x = TestPassCounter("abbbghhh")
    assert x.first_invalid() == 3
    x = TestPassCounter("bbbbghhh")
    assert x.first_invalid() == 2

    # testing carry
    x = TestPassCounter("abcdefyy")
    assert x.first_invalid() == SIZE
    assert str(x) == "abcdefyy"
    rc = x.increment_find_next()
    assert not rc
    assert str(x) == "abcdefyz"
    rc = x.increment_find_next()
    assert not rc
    assert str(x) == "abcdefza"
    for i in range(25):
        rc = x.increment_find_next()
        assert not rc
    assert str(x) == "abcdefzz"
    rc = x.increment_find_next()
    assert not rc
    assert str(x) == "abcdegaa"
    
    # test skipping one (next one is invalid)
    x = TestPassCounter("abcdehhg")
    assert x.first_invalid() == SIZE
    rc = x.increment_find_next()
    assert not rc
    assert str(x) == "abcdehhi"

    # test skipping one
    x = TestPassCounter("bbbabcde")
    assert x.first_invalid() == 2
    rc = x.increment_find_next()
    assert not rc
    assert str(x) == "bbcaabaa"

    # test overflow
    x = TestPassCounter("zzzzzzzz")
    assert x.first_invalid() == 2
    rc = x.increment_find_next()
    assert rc
    assert str(x) == "aabaabaa", str(x)

    # test detection of bad things
    assert Part1Rules("hijklmmn").first_invalid() == 1
    # hijklmmn meets the first requirement (because it contains
    # the straight hij) but fails the second requirement requirement
    # (because it contains i and l).

    assert Part1Rules("abbceffg").first_invalid() == 6
    # abbceffg meets the third requirement (because it repeats bb and ff)
    # but fails the first requirement.

    assert Part1Rules("abbcegjk").first_invalid() == 6
    # abbcegjk fails the third requirement, because it only has one double letter (bb).
    # also no straight

    y = Part1Rules("abcdefgh")
    rc = y.increment_find_next()
    assert not rc
    assert str(y) == "abcdffaa"
    # The next password after abcdefgh is abcdffaa.

    y = Part1Rules("ghijklmn")
    rc = y.increment_find_next()
    assert not rc
    assert str(y) == "ghjaabcc"
    # The next password after ghijklmn is ghjaabcc, because
    # you eventually skip all the passwords that start with ghi...,
    # since i is not allowed.

def main():
    p1 = Part1Rules("vzbxkghb")
    rc = p1.increment_find_next()
    assert not rc
    print("part 1:", str(p1))
    rc = p1.increment_find_next()
    assert not rc
    print("part 2:", str(p1))
    

if __name__ == "__main__":
    test1()
    main()
