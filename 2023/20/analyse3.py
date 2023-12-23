
import typing

"""
There are 48 flip flops. They are organised into 4 groups of 12.
The groups act as chaotic state machines, but I only really want to
know how often they generate a signal as the output.

The outputs go via nodes labelled "vf", "dh", "mk", "rn".

Day 8 again? Least common multiple?

"""

def main() -> None:
    seen_before: typing.Dict[int, int] = {}
    seen_first: typing.Dict[int, int] = {}
    period: typing.Dict[int, int] = {}
    for (i, line) in enumerate(open("part2.txt", "rt")):
        for (j, value) in enumerate(line.split()[1]):
            if value == "B":
                print(f"counter {j} triggers at {i}", end="")
                if j in seen_before:
                    p = i - seen_before[j]
                    print(f" period {p}")
                    if j in period:
                        assert period[j] == p
                    else:
                        period[j] = p
                else:
                    print()
                seen_before[j] = i
                if j not in seen_first:
                    seen_first[j] = i

    for j in range(4):
        print(f"Counter {j} triggers at {seen_first[j]} + {period[j]} * x")

    for j in range(4):
        # Well, this is convenient...
        assert seen_first[j] == period[j]

    c1 = period[0]
    for i in range(1, len(period)):
        c2 = period[i]
        c1 = lcm(c1, c2)

    print("LCM", c1)

def lcm(a, b):
    m = a * b
    if not m: return 0
    while True:
        a %= b
        if not a: return m // b
        b %= a
        if not b: return m // a

    

if __name__ == "__main__":
    main()
