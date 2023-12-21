

import re
import typing
import sys

PARSE_COMPONENT = re.compile(r"^(%|&|)(\w+) -> (.*)$")
BROADCASTER = "broadcaster"
BUTTON = "button"
OUTPUT = "output"
FF = "%"
NAND = "&"

class Component:
    def __init__(self, text: str) -> None:
        m = PARSE_COMPONENT.match(text)
        assert m is not None
        self.kind = m.group(1)
        self.name = m.group(2)
        self.output_names = m.group(3).split(", ")

        if self.output_names == ['']:
            self.kind = OUTPUT
        elif self.kind == "":
            assert self.name in (BROADCASTER, BUTTON)
            self.kind = self.name

        self.outputs: typing.List["Wire"] = []
        self.inputs: typing.List["Wire"] = []
        self.update = {
            BROADCASTER: self.update_broadcaster,
            FF: self.update_ff,
            NAND: self.update_nand,
            OUTPUT: self.update_none,
            BUTTON: self.update_none,
        }[self.kind]
        self.reset()

    def reset(self) -> None:
        self.ff_state = False
        self.counter = 0

    def update_none(self, i: "Wire") -> None:
        if not i.value:
            self.counter += 1

    def update_broadcaster(self, i: "Wire") -> None:
        value = i.value

        for o in self.outputs:
            o.value = value
        for o in self.outputs:
            o.update()

    def update_ff(self, i: "Wire") -> None:
        if not i.value:
            self.ff_state = not self.ff_state
            for o in self.outputs:
                o.value = self.ff_state
            for o in self.outputs:
                o.update()

    def update_nand(self, i: "Wire") -> None:
        all_inputs_high = True
        for i in self.inputs:
            if not i.value:
                all_inputs_high = False

        for o in self.outputs:
            o.value = not all_inputs_high
        for o in self.outputs:
            o.update()

class Wire:
    def __init__(self, source: Component, target: Component) -> None:
        self.source = source
        self.target = target
        self.counters: typing.Optional[Problem] = None
        self.reset()

    def reset(self) -> None:
        self.value = False

    def update(self) -> None:
        if self.counters:
            if self.value:
                self.counters.high_total += 1
                if self.counters.debug:
                    print(f"{self.source.name} -high-> {self.target.name}")
            else:
                self.counters.low_total += 1
                if self.counters.debug:
                    print(f"{self.source.name} -low-> {self.target.name}")
        self.target.update(self)

class Problem:
    def __init__(self, fname: str) -> None:
        # Read components
        self.components: typing.Dict[str, Component] = {}
        for line in open(fname, "rt"):
            c = Component(line)
            assert c.name not in self.components
            self.components[c.name] = c

        assert BROADCASTER in self.components
        self.components[BUTTON] = Component(f"{BUTTON} -> {BROADCASTER}")
        all_with_outputs = list(self.components.values())

        # Make connections
        self.wires: typing.List[Wire] = []
        for c in all_with_outputs:
            for name in c.output_names:
                if name not in self.components:
                    # Component without an output
                    self.components[name] = c2 = Component(f"{name} -> ")
                else:
                    # Component with an output
                    c2 = self.components[name]

                w = Wire(c, c2)
                c.outputs.append(w)
                c2.inputs.append(w)
                self.wires.append(w)

        self.debug = False
        self.reset()

    def reset(self) -> None:
        self.high_total = 0
        self.low_total = 0
        for w in self.wires:
            w.reset()
            w.counters = None
       
        for c in self.components.values():
            c.reset()

    def part1(self) -> int:
        self.reset()
        for w in self.wires:
            w.counters = self
        for i in range(1000):
            self.simulate()
        return self.high_total * self.low_total

    def part2(self, output="rx") -> int:
        self.reset()
        i = 0
        while self.components[output].counter == 0:
            self.simulate()
            i += 1
        return i

    def simulate(self) -> None:
        c = self.components[BROADCASTER]
        w = c.inputs[0]
        w.value = False
        w.update()

def main() -> None:
    assert Problem("test1").part1() == 32000000
    assert Problem("test2").part1() == 11687500
    print(Problem("input").part1())
    assert Problem("input").part1() == 861743850
    assert Problem("test2").part2(OUTPUT) == 1
    print(Problem("input").part2())

if __name__ == "__main__":
    main()
