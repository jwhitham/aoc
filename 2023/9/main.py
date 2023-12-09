
def compute_next(history):
    d_history = []
    for i in range(1, len(history)):
        d_history.append(history[i] - history[i - 1])

    if 0 == max(d_history) == min(d_history):
        return history[-1]
    else:
        return history[-1] + compute_next(d_history)

def part1(fname):
    total = 0
    for line in open(fname, "rt"):
        history = [int(x) for x in line.split()]
        total += compute_next(history)
    return total

def part2(fname):
    total = 0
    for line in open(fname, "rt"):
        history = [int(x) for x in line.split()]
        history.reverse()
        total += compute_next(history)
    return total

def main():
    assert 18 == compute_next([int(x) for x in "0 3 6 9 12 15".split()])
    assert part1("test") == 114
    print(part1("input"))
    assert part2("test") == 2
    print(part2("input"))

if __name__ == "__main__":
    main()
