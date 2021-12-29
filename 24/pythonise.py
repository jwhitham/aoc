
import typing
import sys

from preprocess import Instruction, REGS


class ConvInstruction(Instruction):
    def conv(self):
        if self.op == "inp":
            return "inp"
        elif self.op == "zero":
            return "0"
        elif self.op == "endblock":
            assert False

        if self.value is None:
            operand = self.inputs[1]
        else:
            operand = str(self.value)

        if self.op == "add":
            return self.inputs[0] + " + " + operand

        elif self.op == "mul":
            return self.inputs[0] + " * " + operand

        elif self.op == "eql":
            return "int(" + self.inputs[0] + " == " + operand + ")"

        elif self.op == "div":
            return "div_round_toward_zero(" + self.inputs[0] + ", " + operand + ")"

        elif self.op == "mod":
            return "mod_round_toward_zero(" + self.inputs[0] + ", " + operand + ")"

        else:
            assert False, "unknown operation " + self.op

def main():
    blocks = []
    instructions = []
    inp_count = 0
    for line in open("processed", "rt"):
        inst = ConvInstruction(line)
        instructions.append(inst)
        if inst.op == "endblock":
            instructions.pop()
            if (inp_count > 0) and (inst.output == "z"):
                blocks.append(instructions)
                instructions = []
                assert inp_count == 1
                inp_count = 0
        elif inst.op == "inp":
            inp_count += 1

    assert inp_count == 0
    assert len(instructions) == 0

    with open("pythonised.py", "wt") as fd:
        fd.write("""
class Invalid(Exception):
    pass
def div_round_toward_zero(a: int, b: int) -> int:
    if b == 0:
        raise Invalid()
    if (a < 0) != (b < 0):
        # One is negative
        return -((-a) // b)
    else:
        # Neither or both is negative
        return a // b
def mod_round_toward_zero(a: int, b: int) -> int:
    if (b <= 0) or (a < 0):
        raise Invalid()
    return a % b
""")
        for (i, instructions) in enumerate(blocks):
            fd.write(f"def calc{i}(inp: int, z: int) -> int:\n")
            for inst in instructions:
                fd.write(f"    {inst.output} = {inst.conv()}\n")
            fd.write(f"    return z\n")


if __name__ == "__main__":
    main()
