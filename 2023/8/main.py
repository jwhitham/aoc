
import re
from rosetta_crm import chinese_remainder

def parse(fname):
    with open(fname, "rt") as in_fd:
        directions = in_fd.readline().strip()
        in_fd.readline() # blank line

        pattern = re.compile(r"^(\w+) = \((\w+), (\w+)\)\s*$")
        graph = {}
        for line in in_fd:
            m = pattern.match(line)
            if m is not None:
                (node, left, right) = m.groups()
                graph[node] = (left, right)

    return (directions, graph)

def part1(fname):
    (directions, graph) = parse(fname)
    node = "AAA"
    i = 0
    j = 0
    while node != "ZZZ":
        assert node in graph
        if directions[i] == "L":
            node = graph[node][0]
        else:
            assert directions[i] == "R"
            node = graph[node][1]
        i += 1
        if i >= len(directions):
            i = 0
        j += 1

    return j


def part2(fname):
    (directions, graph) = parse(fname)
    start_nodes = set([node for node in graph.keys() if node.endswith("A")])
    end_nodes = set([node for node in graph.keys() if node.endswith("Z")])

    cycle_data = []
    for start_node in start_nodes:
        # Analyse each path
        # 1. Each (node, dir_index) is labelled with the number of steps
        #    taken to reach it for the first time.
        # 2. Find the cycle (what step from? what step to?)
        # 3. Find any end nodes (what step?)
        end_steps = []
        node = start_node
        label = {}
        step_count = 0
        dir_index = 0
        while not ((node, dir_index) in label):
            label[(node, dir_index)] = step_count
            if node in end_nodes:
                end_steps.append(step_count)
            step_count += 1 
            node = graph[node][0 if directions[dir_index] == "L" else 1]
            dir_index += 1
            if dir_index >= len(directions):
                dir_index = 0

        # Reached a point where the cycle repeats; record information about the repeat
        cycle_from_step = step_count
        cycle_to_step = label[(node, dir_index)]
        cycle_length = cycle_from_step - cycle_to_step

        # If the end is reached more than once, but with different dir_index,
        # the cycle can be shortened
        assert len(end_steps) != 0
        assert (cycle_length % len(end_steps)) == 0
        cycle_length //= len(end_steps)
        first_end_step = end_steps[0]

        assert first_end_step == cycle_length

        cycle_data.append(cycle_length)

    # my algorithm
    c1 = cycle_data[0]
    for i in range(1, len(cycle_data)):
        c2 = cycle_data[i]

        # a * c1 = b * c2       <-- find integers a and b
        a = b = 1
        while True:
            # Find b, given a
            b = (a * c1) // c2
            if (a * c1) == (b * c2):
                break
            assert (a * c1) > (b * c2)
            b += 1

            # Find a, given b
            a = (b * c2) // c1
            if (a * c1) == (b * c2):
                break
            assert (a * c1) < (b * c2)
            a += 1

        # Got integers a and b
        assert (a * c1) == (b * c2)
        c1 = a * c1

    result = c1

    # It looked like a Chinese remainder problem, but all of the remainders are zero..
    #
    #   In mathematics, the Chinese remainder theorem states that if one knows the
    #   remainders a[i] of the Euclidean division of an integer R by several integers n[i],
    #   then one can determine uniquely the remainder of the division of R by the
    #   product of these integers n[i], under the condition that the divisors are pairwise
    #   coprime (no two divisors share a common factor other than 1). 
    #
    # R = point where everything lines up
    # n = cycle lengths
    # a = 0
    # 
    # As all the remainders are zero the value of R = 0 which is true but unhelpful.
    # The algorithm doesn't work as-is.
    # Least common multiple is better for the special case where all remainders are 0.

    c1 = cycle_data[0]
    for i in range(1, len(cycle_data)):
        c2 = cycle_data[i]
        c1 = lcm(c1, c2)

    assert c1 == result
    return result

def lcm(a, b):
    m = a * b
    if not m: return 0
    while True:
        a %= b
        if not a: return m // b
        b %= a
        if not b: return m // a


def main():
    assert part1("test") == 2
    print(part1("input"))
    assert part2("test2") == 6
    print(part2("input"))

# R = chinese_remainder(n, a)
# R is the smallest value where:
# \forall i  \exists x in Integers  R = a[i] + (x * n[i])

if __name__ == "__main__":
    main()
