
import collections

def part1(fname):
    data = {}
    width = height = 0
    for (y1, line) in enumerate(open(fname, "rt")):
        for (x1, col) in enumerate(line.rstrip()):
            data[(y1, x1)] = col
            width = x1 + 1
        height = y1 + 1

    total = 0
    checked = set()
    for y1 in range(height):
        for x1 in range(width):
            if (y1, x1) in checked:
                # Already checked
                continue

            checked.add((y1, x1))
            if not data.get((y1, x1), ".").isdigit():
                # No number here
                continue

            # Find end of number
            x2 = x1 + 1
            while (x2 < width) and data.get((y1, x2), ".").isdigit():
                checked.add((y1, x2))
                x2 += 1

            # Decode the number
            number = 0
            for x in range(x1, x2):
                number *= 10
                number += int(data.get((y1, x), "."))

            # Is this number near to a symbol?
            symbol = False
            for x in range(x1 - 1, x2 + 1):
                for y in range(y1 - 1, y1 + 2):
                    v = data.get((y, x), ".")
                    if not (v.isdigit() or v == '.'):
                        symbol = True
                   
            if symbol:
                total += number

    return total

def part2(fname):
    data = {}
    width = height = 0
    for (y1, line) in enumerate(open(fname, "rt")):
        for (x1, col) in enumerate(line.rstrip()):
            data[(y1, x1)] = col
            width = x1 + 1
        height = y1 + 1

    checked = set()
    gear = collections.defaultdict(lambda: [])
    for y1 in range(height):
        for x1 in range(width):
            if (y1, x1) in checked:
                # Already checked
                continue

            checked.add((y1, x1))
            if not data.get((y1, x1), ".").isdigit():
                # No number here
                continue

            # Find end of number
            x2 = x1 + 1
            while (x2 < width) and data.get((y1, x2), ".").isdigit():
                checked.add((y1, x2))
                x2 += 1

            # Decode the number
            number = 0
            for x in range(x1, x2):
                number *= 10
                number += int(data.get((y1, x), "."))

            # Is this number near to a '*' symbol?
            for x in range(x1 - 1, x2 + 1):
                for y in range(y1 - 1, y1 + 2):
                    if data.get((y, x), ".") == '*':
                        gear[(y, x)].append(number)

    total = 0
    for number_list in gear.values():
        assert len(number_list) <= 2
        if len(number_list) == 2:
            total += number_list[0] * number_list[1]

    return total

def main():
    assert part1("test") == 4361
    print(part1("input"))
    assert part2("test") == 467835
    print(part2("input"))

if __name__ == "__main__":
    main()


        
