"""
This is my attempt at a faster general solution to the problem.
I still have some assumptions about the input:
* division by 26
* the program can be divided into 14 blocks, one per input,
  and only the "z" register is "live" between the blocks
"""

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

        if self.op == "inp":
            self.inputs = []
        if self.op == "mul" and self.value == 0:
            self.inputs = []
            self.op = "zero"


    def __str__(self):
        if self.op == "inp":
            return "{} {}".format(self.op, self.output)
        elif self.value is not None:
            return "{} {} {}".format(self.op, self.output, self.value)
        else:
            return "{} {} {}".format(self.op, self.output, self.inputs[1])

    def evaluate(self, state):
        if self.op == "inp":
            return state["inp"]
        if self.op == "zero":
            return 0

        if self.value is None:
            operand = state[self.inputs[1]]
        else:
            operand = self.value

        if self.op == "add":
            return state[self.inputs[0]] + operand

        elif self.op == "mul":
            return state[self.inputs[0]] * operand

        elif self.op == "eql":
            return int(state[self.inputs[0]] == operand)

        elif self.op == "div":
            return state[self.inputs[0]] // operand

        elif self.op == "mod":
            return state[self.inputs[0]] % operand

        else:
            assert False, "unknown operation " + self.op

class Block:
    def __init__(self):
        self.instructions = []
        self.can_pop = False

    def append(self, inst):
        self.instructions.append(inst)

    def evaluate(self, state):
        for inst in self.instructions:
            state[inst.output] = inst.evaluate(state)

    def analyse(self):
        for z_in in range(26, 26 * 26):
            for inp in range(1, 10):
                state = {"w": 0, "x": 0, "y": 0, "z": z_in, "inp": inp}
                self.evaluate(state)
                z_out = state["z"]
                if z_out < 26:
                    self.can_pop = True
                    return


def main():
    # read instructions
    instructions = []
    for line in open("input", "rt"):
        instructions.append(Instruction(line))

    # generate "live set" (registers in use)
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

    # split instructions into blocks
    i = 1
    inp_count = 0
    blocks = []
    blocks.append(Block())
    for inst in instructions:
        if len(inst.live_set) == 1 and inp_count >= 1:
            assert inp_count == 1
            blocks.append(Block())
            inp_count = 0

        if inst.op == "inp":
            inp_count += 1

        blocks[-1].append(inst)
        i += 1

    # For each block, determine the behaviour (push/pop)
    for block in blocks:
        block.analyse()

    scan = [9 for i in range(len(blocks))]
    overflow = False
    last = []
    first = True
    while not overflow:
        state = {"w": 0, "x": 0, "y": 0, "z": 0}
        bad = -1
        for i in range(len(blocks)):
            state["inp"] = scan[i]
            zin = state["z"]
            blocks[i].evaluate(state)
            zout = state["z"]
            if blocks[i].can_pop:
                if zout != (zin // 26):
                    # did not pop: advance now
                    bad = i
                    break

        if bad < 0:
            if state["z"] == 0:
                if first:
                    first = False
                    print("largest", scan, flush=True)
                last = scan[:]
            bad = len(blocks) - 1

        assert 0 <= bad < len(blocks)
        scan[bad] -= 1
        for j in range(bad + 1, len(blocks)):
            scan[j] = 9

        while scan[bad] < 1:
            scan[bad] = 9
            bad -= 1
            if bad < 0:
                overflow = True
                break
            else:
                scan[bad] -= 1
    
    print("smallest", last, flush=True)

if __name__ == "__main__":
    main()
