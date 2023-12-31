

import typing

Position = typing.Tuple[int, int]
DIRECTION_TABLE = {
    (1, 0): ">",
    (-1, 0): "<",
    (0, -1): "^",
    (0, 1): "v",
}
DEBUG = False

class Node:
    def __init__(self, position: Position, symbol: str) -> None:
        self.position = position
        self.symbol = symbol
        self.edges: typing.List[Edge] = []
        self.visited = False
        self.max_distance = 0

    def __str__(self) -> str:
        return "N" + str((self.symbol, self.position))

    def simplify(self) -> None:
        # Look at each edge in turn, repeatedly attempting to simplify
        i = 0
        while i < len(self.edges):
            if not simplify_edge(self, i):
                i += 1

    def compute_distances(self, distance: int) -> None:
        n1 = self
        assert not n1.visited
        n1.max_distance = max(n1.max_distance, distance)
        n1.visited = True
        for e in n1.edges:
            if e.visited:
                continue

            if (not e.bidirectional) and (n1 != e.n1):
                # Cannot traverse - edge is one-way
                continue

            n2 = e.find_other(n1)
            if n2.visited:
                continue

            e.visited = True
            n2.compute_distances(e.distance + distance)
            e.visited = False

        n1.visited = False

    def find_edge(self, n: "Node") -> typing.Optional["Edge"]:
        for e in self.edges:
            if e.n1 == self and e.n2 == n:
                return e
            if e.n2 == self and e.n1 == n:
                return e
        return None

class Edge:
    def __init__(self, n1: Node, n2: Node, distance: int) -> None:
        self.n1 = n1
        self.n2 = n2
        self.distance = distance
        self.visited = False
        self.bidirectional = False

    def __str__(self) -> str:
        if self.bidirectional:
            return f"E({self.n1} <-{self.distance}-> {self.n2})"
        else:
            return f"E({self.n1} -{self.distance}-> {self.n2})"

    def find_other(self, n: Node) -> Node:
        if n == self.n1:
            return self.n2
        elif n == self.n2:
            return self.n1
        raise Exception(f"Edge {self} has no node {n}")


def simplify_edge(n0: Node, edge_index: int) -> bool:
    e01 = n0.edges[edge_index]

    # Follow this edge to n1
    n1 = e01.find_other(n0)
    if len(n1.edges) != 2:
        # n1 is a dead end, junction, or one-way connection - can't simplify
        return False
    if n1 == n0:
        # This is a cycle - can't simplify
        return False
    if not e01.bidirectional:
        # Needs to be a bidirectional edge
        return False

    # Identify the edges as e01 and e12
    (e1x, e1y) = n1.edges
    if e1x == e01:
        e12 = e1y
    elif e1y == e01:
        e12 = e1x
    else:
        # There is no edge n1 -> n0, so n1 is a junction with no back edge - can't simplify
        return False

    # Look at n2 - does it have a back edge to n1?
    n2 = e12.find_other(n1)
    if not e12.bidirectional:
        # Needs to be a bidirectional edge
        return False
    assert e12 == n2.find_edge(n1)

    # n1 is diconnected
    n1.edges.remove(e01)
    n1.edges.remove(e12)

    # New connections skip n1
    e02 = Edge(n0, n2, e01.distance + e12.distance)
    assert n0.edges[edge_index] == e01
    n0.edges[edge_index] = e02
    n2.edges.remove(e12)
    n2.edges.append(e02)
    e02.bidirectional = True
    return True

class Problem:
    def __init__(self, fname: str) -> None:
        # Capture area as a 2D grid
        self.width = -1
        self.height = -1
        self.nodes: typing.Dict[Position, Node] = {}
        with open(fname, "rt") as fd:
            for (y, line) in enumerate(fd):
                for (x, col) in enumerate(line.rstrip()):
                    if col != "#":
                        self.nodes[(x, y)] = Node((x, y), col)
                    self.width = max(self.width, x + 1)
                self.height = max(self.height, y + 1)

        # Find start and end
        self.start: typing.Optional[Node] = None
        self.end: typing.Optional[Node] = None
        for x in range(self.width):
            if self.start is None:
                y = 0
                self.start = self.nodes.get((x, y), None)
            if self.end is None:
                y = self.height - 1
                self.end = self.nodes.get((x, y), None)

        assert self.start is not None
        assert self.end is not None

    def convert_to_graph(self, allow_travel: typing.Callable[[str, int, int], bool]) -> None:
        # Remove edges
        for n in self.nodes.values():
            n.edges.clear()

        # Convert to a graph (add edges)
        for y in range(self.height):
            for x in range(self.width):
                n1 = self.nodes.get((x, y), None)
                if n1 is not None:
                    for (dx, dy) in DIRECTION_TABLE:
                        if allow_travel(n1.symbol, dx, dy):
                            n2 = self.nodes.get((x + dx, y + dy), None)
                            if n2 is not None:
                                e = n2.find_edge(n1)
                                if e is not None:
                                    e.bidirectional = True
                                else:
                                    e = Edge(n1, n2, 1)
                                n1.edges.append(e)

        # Remove non-branching parts of the graph
        for n in self.nodes.values():
            n.simplify()

        if DEBUG:
            edges: typing.Set[Edge] = set()
            for y in range(self.height):
                for x in range(self.width):
                    n1 = self.nodes.get((x, y), None)
                    if n1 is not None:
                        edges.update(n1.edges)

            for e in sorted(edges, key=lambda e: e.n1.position):
                print(e)

    def part1(self) -> int:
        self.convert_to_graph(lambda symbol, dx, dy:
                        (symbol == ".") or (symbol == DIRECTION_TABLE[(dx, dy)]))
        return self.compute_distances()

    def part2(self) -> int:
        self.convert_to_graph(lambda symbol, dx, dy: True)
        return self.compute_distances()

    def compute_distances(self) -> int:
        # Reset maximum distance
        for n in self.nodes.values():
            n.max_distance = 0

        assert self.start is not None
        assert self.end is not None
        self.start.compute_distances(0)
        assert self.end.max_distance > 0
        if DEBUG:
            print(self.end.max_distance)
        return self.end.max_distance


def main():
    assert Problem("test").part1() == 94
    print(Problem("input").part1())
    assert Problem("test").part2() == 154
    print(Problem("input").part2())

if __name__ == "__main__":
    main()
