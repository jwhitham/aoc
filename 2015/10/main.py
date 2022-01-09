
import typing
import re


def iterate(in_state: str) -> str:
    run_length = 1
    out_state: typing.List[str] = []
    for i in range(1, len(in_state)):
        if in_state[i - 1] == in_state[i]:
            run_length += 1
        else:
            out_state.append("{}{}".format(run_length, in_state[i - 1]))
            run_length = 1

    out_state.append("{}{}".format(run_length, in_state[-1]))
    return "".join(out_state)

def main() -> None:
    assert iterate("1") == "11"
    assert iterate("11") == "21"
    assert iterate("21") == "1211"
    assert iterate("1211") == "111221"
    assert iterate("111221") == "312211"

    state = open("input", "rt").read().strip()
    for i in range(40):
        state = iterate(state)
    print("part 1:", len(state))
    for i in range(10):
        state = iterate(state)
    print("part 2:", len(state))

if __name__ == "__main__":
    main()


