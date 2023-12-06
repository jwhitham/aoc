

import math

def parse(fname):
    with open(fname, "rt") as in_fd:
        time_fields = in_fd.readline().split()
        assert time_fields[0] == "Time:"
        time_fields.pop(0)

        distance_fields = in_fd.readline().split()
        assert distance_fields[0] == "Distance:"
        distance_fields.pop(0)

    return (time_fields, distance_fields)

def part1(fname):
    (time_fields, distance_fields) = parse(fname)
    return calc(time_fields, distance_fields)

def part2(fname):
    (time_fields, distance_fields) = parse(fname)
    time_fields = ["".join(time_fields)]
    distance_fields = ["".join(distance_fields)]
    return calc(time_fields, distance_fields)

def calc(time_fields, distance_fields):
    total = 1
    for i in range(len(time_fields)):
        t = float(time_fields[i])
        s = float(distance_fields[i]) + 0.5

        tmp = math.sqrt((t * t) - (4.0 * s))
        low_h = (-t + tmp) / -2.0
        high_h = (-t - tmp) / -2.0
        subtotal = 1 + int(math.floor(high_h)) - int(math.ceil(low_h))
        total *= subtotal

    return total

def main():
    assert part1("test") == 288
    print(part1("input"))
    assert part2("test") == 71503
    print(part2("input"))

if __name__ == "__main__":
    main()


