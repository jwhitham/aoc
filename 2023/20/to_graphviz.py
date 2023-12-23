
from main import Problem, BROADCASTER, FF, Component, NAND
import typing

def main() -> None:
    problem = Problem("input")
    stateful = problem.get_stateful_list()

    with open("input.dot", "wt") as fd:
        seen: typing.Set[str] = set()

        fd.write("digraph G {\n")
        def convert(c: Component) -> None:
            if c.name in seen:
                return

            seen.add(c.name)
            k = "yellow"
            i = ""
            if c.kind == FF:
                k = "blue"
                i = " {}".format(stateful.index(c))
            elif c.kind == NAND:
                k = "red"

            fd.write(f"{c.name} [color={k},label=\"{c.name}{i}\",shape=\"rect\"]\n")

            for o in c.outputs:
                convert(o.target)
                fd.write(f"{c.name} -> {o.target.name}\n")

        root = problem.components[BROADCASTER]
        convert(root)
        fd.write("}\n")


if __name__ == "__main__":
    main()
