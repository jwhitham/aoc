
MASK = (1 << 16) - 1


class Base:
    def __init__(self):
        self.value = None
        self.child = []
        self.strings = []

    def resolve_strings(self, definition):
        self.child = []
        for x in self.strings:
            if x.isdigit():
                self.child.append(Literal(int(x)))
            else:
                self.child.append(definition[x])

    def calc(self):
        pass


class Literal(Base):
    def __init__(self, value):
        Base.__init__(self)
        self.value = value


class Op(Base):
    def __init__(self, x, op, y):
        Base.__init__(self)
        self.strings = [x, y]
        self.op = op

    def calc(self):
        for c in self.child:
            if c.value is None:
                c.calc()

        if self.op == "NAND":
            self.value = ~(self.child[0].value & self.child[1].value) & MASK
        elif self.op == "AND":
            self.value = (self.child[0].value & self.child[1].value) & MASK
        elif self.op == "OR":
            self.value = (self.child[0].value | self.child[1].value) & MASK
        elif self.op == "RSHIFT":
            self.value = (self.child[0].value >> self.child[1].value) & MASK
        elif self.op == "LSHIFT":
            self.value = (self.child[0].value << self.child[1].value) & MASK
        else:
            assert False, self.op


def calc(file_name, root_name) -> int:
    definition = {}
    for line in open(file_name):
        fields = line.split()
        target = fields.pop()
        assign = fields.pop()
        assert assign == "->"
        if len(fields) == 1:
            definition[target] = Op("0", "OR", fields[0])
        elif len(fields) == 2:
            assert fields[0] == "NOT"
            definition[target] = Op(fields[1], "NAND", fields[1])
        else:
            assert len(fields) == 3
            definition[target] = Op(fields[0], fields[1], fields[2])

    for op in definition.values():
        op.resolve_strings(definition)

    root = definition[root_name]
    root.calc()

    return root.value

if __name__ == "__main__":
    assert calc("test1", "d") == 72
    assert calc("test1", "i") == 65079
    part1 = calc("input", "a")
    print("part 1:", part1)
    with open("part2", "wt") as fd:
        fd.write(open("input").read())
        fd.write("{} -> b\n".format(part1))
    part2 = calc("part2", "a")
    print("part 2:", part2)
    


