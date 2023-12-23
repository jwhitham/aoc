

import re
import typing
import collections
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
        self.was_low = self.was_high = False
        self.counter = 0

    def update_none(self, i: "Wire") -> None:
        if not i.value:
            self.counter += 1

    def update_broadcaster(self, i: "Wire") -> None:
        value = i.value
        self.send(value)

    def send(self, value: bool) -> None:
        for o in self.outputs:
            o.send(value)

    def update_ff(self, i: "Wire") -> None:
        if not i.value:
            self.ff_state = not self.ff_state
            self.send(self.ff_state)

    def update_nand(self, i: "Wire") -> None:
        all_inputs_high = True
        for i in self.inputs:
            if not i.value:
                all_inputs_high = False
        if all_inputs_high:
            self.was_low = True
        else:
            self.was_high = True
        self.send(not all_inputs_high)

class Wire:
    def __init__(self, source: Component, target: Component, parent: "Problem") -> None:
        self.source = source
        self.target = target
        self.parent = parent
        self.reset()

    def reset(self) -> None:
        self.value = False

    def send(self, value: bool) -> None:
        def update() -> None:
            self.value = value
            if self.value:
                self.parent.high_total += 1
                if self.parent.debug:
                    print(f"{self.source.name} -high-> {self.target.name}")
            else:
                self.parent.low_total += 1
                if self.parent.debug:
                    print(f"{self.source.name} -low-> {self.target.name}")
            self.target.update(self)
        self.parent.pulse_queue.append(update)

class Problem:
    def __init__(self, fname: str) -> None:
        self.pulse_queue: typing.Deque[typing.Callable[[], None]] = collections.deque()

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

                w = Wire(c, c2, self)
                c.outputs.append(w)
                c2.inputs.append(w)
                self.wires.append(w)

        self.debug = False
        self.reset()

    def reset(self) -> None:
        self.high_total = 0
        self.low_total = 0
        self.pulse_queue.clear()
        for w in self.wires:
            w.reset()
       
        for c in self.components.values():
            c.reset()

    def part1(self) -> int:
        self.reset()
        for i in range(1000):
            self.simulate()
        return self.high_total * self.low_total

    def get_stateful_list(self) -> typing.List[Component]:
        stateful = [c for c in self.components.values() if c.kind == FF]
        stateful.sort(key = lambda c: c.name)
        return stateful

    def part2(self, output="rx") -> int:
        self.reset()
        i = 0
        stateful = self.get_stateful_list()
        special = [c for c in self.components.values() if c.name in
                    ["vf", "dh", "mk", "rn"]]
        with open("part2.txt", "wt") as fd:
            while self.components[output].counter == 0:
                self.simulate()
                bit = 0
                for c in stateful:
                    bit = bit << 1
                    if c.ff_state:
                        bit |= 1
                fd.write(f"{bit:016x} ")
                for c in special:
                    if c.was_low and c.was_high:
                        fd.write("B")
                    elif c.was_low:
                        fd.write("L")
                    elif c.was_high:
                        fd.write("H")
                    else:
                        fd.write("-")
                    c.was_high = c.was_low = False
                fd.write("\n")
                i += 1
        return i

    def simulate(self) -> None:
        c = self.components[BROADCASTER]
        w = c.inputs[0]
        w.send(False)
        while len(self.pulse_queue) != 0:
            self.pulse_queue.popleft()()

def main() -> None:
    assert Problem("test1").part1() == 32000000
    assert Problem("test2").part1() == 11687500
    assert Problem("input").part1() == 861743850
    assert Problem("test2").part2(OUTPUT) == 1
    print(Problem("input").part1())
    print(Problem("input").part2())

if __name__ == "__main__":
    main()
