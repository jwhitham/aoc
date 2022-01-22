import re
import json

INPUT = open("input", "rt").read()


def elf_count(obj):
    if type(obj) == dict:
        if "red" in obj.values():
            return 0
        else:
            return sum([elf_count(child) for child in obj.values()])
    
    elif type(obj) == list:
        return sum([elf_count(child) for child in obj])

    elif type(obj) == int:
        return obj

    elif type(obj) == str:
        return 0

    assert False, ("unknown object type: " + str(type(obj)))

def main():
    print("part 1:", sum([int(x) for x in re.findall("-?\d+", INPUT)]))

    print("part 2:", elf_count(json.loads(INPUT)))


if __name__ == "__main__":
    main()
