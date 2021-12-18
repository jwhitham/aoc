# lots of TDD needed here

import typing
import subprocess
import sys

EXPLODE_DEPTH = 5


OPEN = -1
CLOSE = -2
FlatNumber = typing.List[int]
RawNumber = typing.List[typing.Any]

def r2f(raw_number: RawNumber) -> FlatNumber:
    number: FlatNumber = []
  
    def flatten(s):
        if isinstance(s, int):
            number.append(s)
        else:
            number.append(OPEN)
            for v in s:
                flatten(v)
            number.append(CLOSE)
    
    flatten(raw_number)
    return number

def f2r(flat_number: FlatNumber) -> RawNumber:
    stack: RawNumber = [[]]
    for v in flat_number:
        if v == OPEN:
            stack.append([])
        elif v == CLOSE:
            sub = stack.pop()
            stack[-1].append(sub)
        else:
            stack[-1].append(v)

    return stack[0][0]

def explode(flat_number: FlatNumber) -> bool:
    depth = 0
    start_explode = -1
    end_explode = -1

    for i in range(len(flat_number)):
        if flat_number[i] == OPEN:
            depth += 1
            assert depth <= EXPLODE_DEPTH
            if depth == EXPLODE_DEPTH:
                start_explode = i
        elif flat_number[i] == CLOSE:
            if start_explode >= 0:
                assert depth == EXPLODE_DEPTH
                end_explode = i
                break
            depth -= 1
            assert depth >= 0

    if start_explode < 0:
        return False

    # get exploding pair
    assert (start_explode + 3) == end_explode
    assert flat_number[start_explode + 0] == OPEN
    left = flat_number[start_explode + 1]
    right = flat_number[start_explode + 2]
    assert flat_number[start_explode + 3] == CLOSE

    # go left and add
    for i in range(start_explode - 1, -1, -1):
        if flat_number[i] >= 0:
            flat_number[i] += left
            break

    # go right and add
    for i in range(end_explode + 1, len(flat_number), 1):
        if flat_number[i] >= 0:
            flat_number[i] += right
            break

    # remove middle
    flat_number[start_explode:start_explode + 4] = [0]

    return True

def split(flat_number: FlatNumber) -> bool:
    for i in range(len(flat_number)):
        if flat_number[i] >= 10:
            # split here
            value = flat_number[i]
            left = value // 2
            right = (value + 1) // 2
            assert (left + right) == value
            flat_number[i:i+1] = [OPEN, left, right, CLOSE]
            return True

    return False

def normalise(flat_number: FlatNumber) -> None:
    while explode(flat_number) or split(flat_number):
        pass

def magnitude(flat_number: FlatNumber) -> int:
    def magnitude2(sub) -> int:
        if isinstance(sub, int):
            return sub
        else:
            assert len(sub) == 2
            return (magnitude2(sub[0]) * 3) + (magnitude2(sub[1]) * 2)

    return magnitude2(f2r(flat_number))

def addition(n1: FlatNumber, n2: FlatNumber) -> FlatNumber:
    v = [OPEN] + n1 + n2 + [CLOSE]
    normalise(v)
    return v

def test_r2f2r() -> None:
    x = [[[[[9,8],1],2],3],4]
    assert f2r(r2f(x)) == x

def test_explode() -> None:
    def t(raw_number: RawNumber) -> RawNumber:
        flat_number = r2f(raw_number)
        explode(flat_number)
        raw_number = f2r(flat_number)
        return raw_number

    assert t((([[[[[9,8],1],2],3],4]))) ==  [[[[0,9],2],3],4]
    assert t((([7,[6,[5,[4,[3,2]]]]]))) ==  [7,[6,[5,[7,0]]]]
    assert t((([[6,[5,[4,[3,2]]]],1]))) ==  [[6,[5,[7,0]]],3]
    assert t((([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]))) ==  [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
    assert t((([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]))) ==  [[3,[2,[8,0]]],[9,[5,[7,0]]]]

def test_split() -> None:
    def t(raw_number: RawNumber) -> RawNumber:
        flat_number = r2f(raw_number)
        split(flat_number)
        raw_number = f2r(flat_number)
        return raw_number

    assert t([[[[0,7],4],[15,[0,13]]],[1,1]]) == [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
    assert t([[[[0,7],4],[[7,8],[0,13]]],[1,1]]) == [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]

def test_normalise() -> None:
    def t(raw_number: RawNumber) -> RawNumber:
        flat_number = r2f(raw_number)
        normalise(flat_number)
        raw_number = f2r(flat_number)
        return raw_number

    assert t([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]) == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

def test_addition() -> None:

    n1 = r2f([[[[4,3],4],4],[7,[[8,4],9]]])
    n2 = r2f([1,1])

    # after addition: [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
    n = [OPEN] + n1 + n2 + [CLOSE]
    assert f2r(n) == [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]

    # after explode:  [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
    rc = explode(n)
    assert rc
    assert f2r(n) == [[[[0,7],4],[7,[[8,4],9]]],[1,1]]

    # after explode:  [[[[0,7],4],[15,[0,13]]],[1,1]]
    rc = explode(n)
    assert rc
    assert f2r(n) == [[[[0,7],4],[15,[0,13]]],[1,1]]

    # after split:    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
    rc = split(n)
    assert rc
    assert f2r(n) == [[[[0,7],4],[[7,8],[0,13]]],[1,1]]

    # after split:    [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
    rc = split(n)
    assert rc
    assert f2r(n) == [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]

    # after explode:  [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
    rc = explode(n)
    assert rc
    assert f2r(n) == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

def test_more_addition() -> None:
    def t(*nl) -> RawNumber:
        total = r2f(nl[0])
        for n in nl[1:]:
            total = addition(total, r2f(n))
        
        return f2r(total)

    assert t([[[[4,3],4],4],[7,[[8,4],9]]], [1,1]) == (
        [[[[0,7],4],[[7,8],[6,0]]],[8,1]])

    assert t([1,1],
    [2,2],
    [3,3],
    [4,4]) == [[[[1,1],[2,2]],[3,3]],[4,4]]


    assert t([1,1],
    [2,2],
    [3,3],
    [4,4],
    [5,5]) == [[[[3,0],[5,3]],[4,4]],[5,5]]

    assert t([1,1],
    [2,2],
    [3,3],
    [4,4],
    [5,5],
    [6,6]) == [[[[5,0],[7,4]],[5,5]],[6,6]]

    assert t([[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
    [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
    [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
    [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
    [7,[5,[[3,8],[1,4]]]],
    [[2,[2,2]],[8,[8,1]]],
    [2,9],
    [1,[[[9,3],9],[[9,0],[0,7]]]],
    [[[5,[7,4]],7],1],
    [[[[4,2],2],6],[8,7]]) == [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]

def test_magnitude() -> None:
    def t(n) -> int:
        return magnitude(r2f(n))

    assert t([9,1]) == 29
    assert t([1,9]) == 21
    assert t([[9,1],[1,9]]) == 129
    assert t([[1,2],[[3,4],5]]) == 143
    assert t([[[[0,7],4],[[7,8],[6,0]]],[8,1]]) == 1384
    assert t([[[[1,1],[2,2]],[3,3]],[4,4]]) == 445
    assert t([[[[3,0],[5,3]],[4,4]],[5,5]]) == 791
    assert t([[[[5,0],[7,4]],[5,5]],[6,6]]) == 1137
    assert t([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]) == 3488

def test_part_1() -> None:
    def t(*nl) -> RawNumber:
        total = r2f(nl[0])
        for n in nl[1:]:
            total = addition(total, r2f(n))
        
        return f2r(total)
    n = t([[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]],
        [[[5,[2,8]],4],[5,[[9,9],0]]],
        [6,[[[6,2],[5,6]],[[7,6],[4,7]]]],
        [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]],
        [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]],
        [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]],
        [[[[5,4],[7,7]],8],[[8,3],8]],
        [[9,3],[[9,9],[6,[4,9]]]],
        [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]],
        [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]])
    assert n == [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
    assert magnitude(r2f(n)) == 4140

def part_1() -> None:
    with open("input", "rt") as fd:
        total = r2f(eval(fd.readline()))
        for line in fd:
            total = addition(total, r2f(eval(line)))
        print("part 1:", magnitude(total))

def part_2() -> None:
    numbers = []
    with open("input", "rt") as fd:
        for n in fd:
            numbers.append(r2f(eval(n)))

    best_v = 0
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            v = magnitude(addition(numbers[i], numbers[j]))
            if v > best_v and (i != j):
                best_v = v

    print("part 2:", best_v)

if __name__ == "__main__":
    subprocess.check_call([sys.executable, "-m", "mypy", sys.argv[0]])
    subprocess.check_call([sys.executable, "-m", "pytest", sys.argv[0]])
    part_1()
    part_2()

