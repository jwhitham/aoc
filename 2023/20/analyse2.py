
from main import Problem, BROADCASTER, FF, Component
import typing

"""
There are 48 flip flops.

They seem to be organised as 4 * 12 bit counters.

This program makes a map of the counters.
"""

def main() -> None:
    problem = Problem("input")
    root = problem.components[BROADCASTER]
    stack: typing.List[Component] = []
    ff_seen: typing.Set[Component] = set()
    route: typing.Dict[str, typing.List[Component]] = {}

    def visit(c: Component) -> None:
        if c.name == FF:
            if c in ff_seen:
                return
            ff_seen.add(c)

        if ((c.name == "rx") and (len(stack) >= 1)
        and (len(stack) > len(route.get(stack[0].name, [])))):
            route[stack[0].name] = stack[:]

        if c in stack:
            return

        if c.kind == FF:
            stack.append(c)
            
        for o in c.outputs:
            visit(o.target)

        if c.kind == FF:
            stack.pop()

    visit(root)
    for name in sorted(route):
        stack = route[name]
        print("root", end="")
        for c1 in stack:
            print(f" -> {c1.name}", end="")
        print(" -> rx")

    stateful = problem.get_stateful_list()
    counter_bit_map: typing.Dict[str, typing.List[int]] = {}
    counter_names = sorted(route)
    for name in counter_names:
        counter_bit_map[name] = []
        for c in reversed(route[name]):
            counter_bit_map[name].append(stateful.index(c))
        print(f" {name:3s}", end="")
    print("")

    for line in open("part2.txt", "rt"):
        all_bits = int(line.strip(), 16)
        for name in counter_names:
            value = 0
            for i in counter_bit_map[name]:
                value = value << 1
                value |= (all_bits >> i) & 1
            print(f" {value:03x}", end="")
        print("")

if __name__ == "__main__":
    main()
