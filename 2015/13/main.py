
import re
import typing

EDGE = re.compile(r"^(\w+) would (gain|lose) (\d+) hap.*to (\w+)\.")

class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.edges: typing.List["Edge"] = []
        self.before: typing.Optional["Edge"] = None
        self.after: typing.Optional["Edge"] = None

    def is_connected(self) -> bool:
        return self.after is not None

    def connect(self, other: "Node") -> None:
        assert self.after is None
        assert other.before is None

        once = False
        for edge in self.edges:
            if edge.p1 is other:
                assert edge.p2 is self
                assert not once
                self.after = edge
                other.before = edge
                once = True
            if edge.p2 is other:
                assert edge.p1 is self
                assert not once
                self.after = edge
                other.before = edge
                once = True
        assert once

    def disconnect(self, other: "Node") -> None:
        assert self.after is not None
        if self.after.p2 is self:
            assert other is self.after.p1
        else:
            assert other is self.after.p2

        assert other.before is self.after
        other.before = None
        self.after = None

    def get_bound(self) -> int:
        upper_bound = 0
        connections = 0
        ordered = []
        for edge in self.edges:
            if (edge is self.after) or (edge is self.before):
                # Edge connected here - value is known
                upper_bound += edge.value
                connections += 1
            elif edge.is_connected():
                # Edge connected somewhere - can't be connected here
                pass
            else:
                # Edge unconnected and could be chosen
                ordered.append(edge)

        ordered.sort(key=lambda edge: edge.value)
        assert connections <= 2
        for i in range(min(len(ordered), 2 - connections)):
            upper_bound += ordered[-1 - i].value

        return upper_bound

class Edge:
    def __init__(self, p1: Node, p2: Node) -> None:
        self.p1 = p1
        self.p2 = p2
        self.value = 0
        p1.edges.append(self)
        p2.edges.append(self)

    def is_connected(self) -> bool:
        return ((self.p1.after is self)
                or (self.p1.before is self)
                or (self.p2.after is self)
                or (self.p2.before is self))


class Graph:
    def __init__(self, filename: str) -> None:
        # read graph
        self.node_map: typing.Dict[str, Node] = {}
        self.edge_map: typing.Dict[typing.Tuple[str, str], Edge] = {}
        for line in open(filename, "rt"):
            m = EDGE.match(line)
            assert m, line
            p1 = self.get_node(m.group(1))
            p2 = self.get_node(m.group(4))
            value = int(m.group(3))
            if m.group(2) == "lose":
                value = -value

            edge = self.get_edge(p1, p2)
            edge.value += value

        self.all_nodes = sorted(self.node_map.values(), key=lambda p: p.name)

    def get_node(self, name: str) -> Node:
        node = self.node_map.get(name, None)
        if node is None:
            self.node_map[name] = node = Node(name)
        return node

    def get_edge(self, p1: Node, p2: Node) -> Edge:
        edge = self.edge_map.get((p1.name, p2.name), None)
        if edge is None:
            edge = self.edge_map.get((p2.name, p1.name), None)
        if edge is None:
            self.edge_map[(p1.name, p2.name)] = edge = Edge(p1, p2)
        return edge

    def add_node_with_zero_edges(self) -> None:
        p1 = self.get_node("Me")
        for p2 in self.all_nodes:
            self.get_edge(p1, p2)
        self.all_nodes.append(p1)

class Solver:
    def __init__(self, filename):
        self.graph = Graph(filename)

    def get_bound(self) -> int:
        upper_bound = 0
        for node in self.graph.all_nodes:
            upper_bound += node.get_bound()

        return upper_bound // 2

    def solve(self) -> int:
        self.assigned_nodes: typing.List[Node] = [self.graph.all_nodes[0]]
        self.unassigned_nodes = self.graph.all_nodes[1:]
        self.best_solution_score = -(1 << 31)
        self.best_solution_copy: typing.List[Node] = []
        self.explore()
        return self.best_solution_score

    def explore(self) -> None:
        previous = self.assigned_nodes[-1]

        # Which node is next?
        for i in range(len(self.unassigned_nodes)):
            node = self.unassigned_nodes[i]
            assert not node.is_connected()

            self.unassigned_nodes.pop(i)
            self.assigned_nodes.append(node)
            previous.connect(node)

            upper_bound = self.get_bound()
            if upper_bound > self.best_solution_score:
                self.explore()

            previous.disconnect(node)
            self.assigned_nodes.pop()
            self.unassigned_nodes.insert(i, node)

        # Detect end of problem
        if len(self.unassigned_nodes) == 0:
            node = self.assigned_nodes[0]
            previous.connect(node)
            upper_bound = self.get_bound()
            if upper_bound > self.best_solution_score:
                self.best_solution_score = upper_bound
                self.best_solution_copy = self.assigned_nodes[:]
            previous.disconnect(node)


if __name__ == "__main__":
    assert Solver("testinput").solve() == 330
    s = Solver("input")
    print("part 1:", s.solve())
    s.graph.add_node_with_zero_edges()
    print("part 2:", s.solve())

    
