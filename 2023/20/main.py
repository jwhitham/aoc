

import re
import typing

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

    def update_none(self) -> None:
        pass

    def update_broadcaster(self) -> None:
        any_received = False
        value = False
        for i in self.inputs:
            if i.pulse_now:
                any_received = True
                value = i.value_now

        if any_received:
            for o in self.outputs:
                assert not o.pulse_next
                o.pulse_next = True
                o.value_next = value

    def update_ff(self) -> None:
        low_received = False
        for i in self.inputs:
            if i.pulse_now and not i.value_now:
                low_received = True

        if low_received:
            self.ff_state = not self.ff_state
            for o in self.outputs:
                assert not o.pulse_next
                o.pulse_next = True
                o.value_next = self.ff_state

    def update_nand(self) -> None:
        all_inputs_high = True
        any_received = False
        for i in self.inputs:
            if i.pulse_now:
                any_received = True

            if not i.value_now:
                all_inputs_high = False

        if any_received:
            for o in self.outputs:
                assert not o.pulse_next
                o.pulse_next = True
                o.value_next = not all_inputs_high

class Wire:
    def __init__(self, source: Component, target: Component) -> None:
        self.source = source
        self.target = target
        self.reset()

    def reset(self) -> None:
        self.pulse_now = False
        self.pulse_next = False
        self.value_now = False
        self.value_next = False

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

    def part1(self, debug=False) -> int:
        high_total = 0
        low_total = 0
        comp_now: typing.Set[Component] = set()
        comp_next: typing.Set[Component] = set()
        wire_now: typing.Set[Wire] = set()
        wire_next: typing.Set[Wire] = set()

        for w in self.wires:
            w.reset()
       
        for c in self.components.values():
            c.reset()

        for i in range(1000):
            if debug:
                print("")
                print(f"Simulation {i}")

            # Initial pulse
            c = self.components[BROADCASTER]
            w = c.inputs[0]
            w.pulse_now = True
            w.value_now = False
            comp_now.add(c)
            wire_now.add(w)
            low_total += 1
            assert len(wire_now) == 1
            assert len(wire_next) == 0
            assert len(comp_now) == 1
            assert len(comp_next) == 0

            # Simulation
            while len(comp_now) != 0:
                if debug:
                    print("")

                for c in comp_now:
                    c.update()
                    for w in c.outputs:
                        if w.pulse_next:
                            wire_next.add(w)

                for w in wire_next | wire_now:
                    if w.pulse_next:
                        if w.value_next:
                            high_total += 1
                            if debug:
                                print(f"{w.source.name} -high-> {w.target.name}")
                        else:
                            low_total += 1
                            if debug:
                                print(f"{w.source.name} -low-> {w.target.name}")
                        comp_next.add(w.target)
                        w.value_now = w.value_next

                    w.pulse_now = w.pulse_next
                    w.pulse_next = False

                (comp_now, comp_next) = (comp_next, comp_now)
                (wire_now, wire_next) = (wire_next, wire_now)
                comp_next.clear()
                wire_next.clear()

        return high_total * low_total


def main() -> None:
    assert Problem("test1").part1() == 32000000
    assert Problem("test2").part1() == 11687500
    print(Problem("input").part1())

if __name__ == "__main__":
    main()
