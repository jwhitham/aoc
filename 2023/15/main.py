
import typing

def hash_algo(cmd: str) -> int:
    total = 0
    for c in cmd:
        total += ord(c)
        total *= 17
        total %= 256
    return total

def part1(fname: str) -> int:
    total = 0
    data = open(fname, "rt", encoding="ascii").read().replace("\n", "")
    for cmd in data.split(","):
        total += hash_algo(cmd)
    return total

Label = str
FocalLength = str
Contents = typing.Tuple[Label, FocalLength]
AllContents = typing.List[Contents]

def part2(fname: str) -> int:
    data = open(fname, "rt", encoding="ascii").read().replace("\n", "")
    all_contents: AllContents = [[] for i in range(256)]
    for cmd in data.split(","):
        (label, operation, focal) = cmd.partition("=")
        if operation != "=":
            (label, operation, nothing) = cmd.partition("-")
            assert operation == "-"
            assert nothing == ""
            focal = ""

        contents = all_contents[hash_algo(label)]
        if operation == "-":
            for i in range(len(contents)):
                if contents[i][0] == label:
                    contents.pop(i)
                    break
        else:
            assert operation == "="
            already_present = False
            for i in range(len(contents)):
                if contents[i][0] == label:
                    contents[i] = (label, focal)
                    already_present = True
                    break
            if not already_present:
                contents.append((label, focal))

    total = 0
    for (box_number, contents) in enumerate(all_contents):
        for (slot_number, (label, focal)) in enumerate(contents):
            total += (box_number + 1) * int(focal) * (slot_number + 1)
    return total

def main() -> None:
    assert part1("test") == 1320
    print(part1("input"))
    assert part2("test") == 145
    print(part2("input"))


if __name__ == "__main__":
    main()
