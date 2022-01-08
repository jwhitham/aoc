
import typing
import sys


REGS = "wxyz"

class Instruction:
    def __init__(self, line):
        self.fields = line.split()
        self.op = self.fields[0]
        self.inputs = [x for x in self.fields[1:] if x in REGS]
        self.output = self.fields[1]
        assert self.output in REGS
        self.live_set = set()
        self.value = None
        if (len(self.fields) >= 3) and not (self.fields[2] in REGS):
            self.value = int(self.fields[2])

        if (self.op == "mul") and (self.value == 0):
            self.op = "zero"

        if self.op in ("inp", "zero"):
            self.inputs = []


    def __str__(self):
        if self.op in ("inp", "zero", "endblock"):
            return "{} {}".format(self.op, self.output)
        elif self.value is not None:
            return "{} {} {}".format(self.op, self.output, self.value)
        else:
            return "{} {} {}".format(self.op, self.output, self.inputs[1])

def main():
    instructions = []
    for line in open("input", "rt"):
        instructions.append(Instruction(line))

    source = {} 
    for i in range(len(instructions)):
        for reg in instructions[i].inputs:
            j = source.get(reg, None)
            if j is not None:
                j += 1
                while j <= i:
                    instructions[j].live_set.add(reg)
                    j += 1

        source[instructions[i].output] = i

    i = 1
    while i < len(instructions):
        dead = instructions[i - 1].live_set - instructions[i].live_set
        if len(instructions[i].live_set) == 1:
            reg = list(instructions[i].live_set)[0]
            new = Instruction("endblock {}".format(reg))
            new.live_set = set(instructions[i].live_set)
            instructions.insert(i, new)
            i += 1

        i += 1

    new = Instruction("endblock z")
    new.live_set = set(instructions[-1].live_set)
    instructions.append(new)

    with open("processed", "wt") as fd:
        for i in range(len(instructions)):
            fd.write(str(instructions[i]))
            fd.write("\n")


if __name__ == "__main__":
    main()
