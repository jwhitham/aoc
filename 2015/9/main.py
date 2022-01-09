
import typing
import re


PARSER = re.compile(r"^(\w+) to (\w+) = (\d+)\s*$")
MAX_DIST = 1 << 31

class Edge:
    def __init__(self, v1: "Vertex", v2: "Vertex", dist: int) -> None:
        self.v1 = v1
        self.v2 = v2
        self.dist = dist
        self.v1.edges.append(self)
        self.v2.edges.append(self)


class Vertex:
    def __init__(self, name: str) -> None:
        self.name = name
        self.edges: typing.List[Edge] = []
        self.visited = False

    def get_min_dist(self, to_visit: int) -> int:
        if to_visit <= 1:
            # Been everywhere now!
            return 0

        to_visit -= 1
        self.visited = True
        min_dist = MAX_DIST
        for e in self.edges:
            if (e.v1 is self) and (not e.v2.visited):
                min_dist = min(min_dist, e.v2.get_min_dist(to_visit) + e.dist)
            elif (e.v2 is self) and (not e.v1.visited):
                min_dist = min(min_dist, e.v1.get_min_dist(to_visit) + e.dist)

        self.visited = False
        return min_dist

    def get_max_dist(self, to_visit: int) -> int:
        if to_visit <= 1:
            # Been everywhere now!
            return 0

        to_visit -= 1
        self.visited = True
        max_dist = -1
        for e in self.edges:
            if (e.v1 is self) and (not e.v2.visited):
                max_dist = max(max_dist, e.v2.get_max_dist(to_visit) + e.dist)
            elif (e.v2 is self) and (not e.v1.visited):
                max_dist = max(max_dist, e.v1.get_max_dist(to_visit) + e.dist)

        self.visited = False
        return max_dist


def main() -> None:
    find_vertex: typing.Dict[str, Vertex] = {}
    edges: typing.List[Edge] = []

    for line in open("input", "rt"):
        m = PARSER.match(line)
        if m:
            n1 = m.group(1)
            v1 = find_vertex.get(n1, None)
            if v1 is None:
                find_vertex[n1] = v1 = Vertex(n1)

            n2 = m.group(2)
            v2 = find_vertex.get(n2, None)
            if v2 is None:
                find_vertex[n2] = v2 = Vertex(n2)

            e = Edge(v1, v2, int(m.group(3)))
            edges.append(e)

    vertexes = list(find_vertex.values())
    min_dist = MAX_DIST
    for start in vertexes:
        min_dist = min(min_dist, start.get_min_dist(len(vertexes)))

    print("part 1:", min_dist)

    max_dist = -1
    for start in vertexes:
        max_dist = max(max_dist, start.get_max_dist(len(vertexes)))

    print("part 2:", max_dist)

if __name__ == "__main__":
    main()


