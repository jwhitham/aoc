

import re
import typing
import collections

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
        self.value_now = False
        self.value_next = False
        self.pulse_now = False
        self.pulse_next = False

class Pulse:
    def __init__(self, wire: Wire, value: bool) -> None:
        self.wire = wire
        self.value = value

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
        trigger: typing.Deque[Pulse] = collections.deque()

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
            trigger.append(Pulse(w, False))
            low_total += 1
            assert len(trigger) == 1

            # Simulation
            while len(trigger) != 0:
                # Pulse arrives
                p = trigger.popleft()
                w = p.wire
                w.value_now = p.value
                w.pulse_now = True
                c = w.target
                c.update()
                w.pulse_now = False

                # Outgoing pulses are processed
                for w in c.outputs:
                    if not w.pulse_next:
                        continue

                    p = Pulse(w, w.value_next)
                    if w.value_next:
                        high_total += 1
                        if debug:
                            print(f"{w.source.name} -high-> {w.target.name}")
                    else:
                        low_total += 1
                        if debug:
                            print(f"{w.source.name} -low-> {w.target.name}")

                    w.pulse_next = False
                    w.value_next = False
                    trigger.append(p)

        return high_total * low_total


def main() -> None:
    assert Problem("test1").part1() == 32000000
    assert Problem("test2").part1() == 11687500
    print(Problem("input").part1())

if __name__ == "__main__":
    main()
