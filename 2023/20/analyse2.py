
from main import Problem, BROADCASTER, FF, Component
import typing

"""
There are 48 flip flops.

They seem to be organised as 4 * 12 bit counters.

This program makes a map of the counters.
"""

class CounterGroup:
    def __init__(self, name: str) -> None:
        self.name = name
        self.value_list: typing.List[int] = []
        self.bit_index: typing.List[int] = []
        self.value_set: typing.Set[int] = set()
        self.final_new_index = -1

def main() -> None:
    problem = Problem("input")
    root = problem.components[BROADCASTER]
    seen: typing.Set[str] = set()
    stateful = problem.get_stateful_list()
    counter_groups: typing.List[CounterGroup] = []

    def find_root_ff(c: Component) -> None:
        if c.name in seen:
            return

        seen.add(c.name)

        if c.kind != FF:
            for o in c.outputs:
                find_root_ff(o.target)
            return

        seen2: typing.Set[str] = set()
        counter_group = CounterGroup(c.name)
        counter_groups.append(counter_group)

        def find_counter(c: Component) -> None:
            if c.name in seen2:
                return

            seen2.add(c.name)
            if c.kind == FF:
                counter_group.bit_index.append(len(stateful) - 1 - stateful.index(c))


            for o in c.outputs:
                find_counter(o.target)
       
        find_counter(c)

    find_root_ff(root)

    for line in open("part2.txt", "rt"):
        all_bits = int(line.split()[0], 16)
        for counter_group in counter_groups:
            value = 0
            for i in counter_group.bit_index:
                value = value << 1
                value |= (all_bits >> i) & 1

            if value not in counter_group.value_set:
                counter_group.value_set.add(value)
                counter_group.final_new_index = len(counter_group.value_list)

            counter_group.value_list.append(value)

    for counter_group in counter_groups:
        print(f"Group {counter_group.name} has {len(counter_group.value_set)} unique, "
              f"last new index is {counter_group.final_new_index} "
              f"of {len(counter_group.value_list)}")

    for counter_group in counter_groups:
        x = 10000
        capture = counter_group.value_list[-x:]
        k = 0
        for j in range(len(counter_group.value_list) - x, counter_group.final_new_index, -1):
            if counter_group.value_list[j:j+x] == capture:
                print(f"Group {counter_group.name} repeat found at {j}")
                k += 1
                if k > 4:
                    break
        
    for counter_group in counter_groups:
        with open(f"part2.{counter_group.name}.txt", "wt") as fd:
            for (i, value) in enumerate(counter_group.value_list):
                fd.write(f"{value:03x}\n")

if __name__ == "__main__":
    main()
