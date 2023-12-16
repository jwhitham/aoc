


import typing
import hashlib
import struct

Position = typing.Tuple[int, int]

class Problem:
    def __init__(self, fname: str) -> None:
        self.movable: typing.List[Position] = []
        self.used: typing.Set[Position] = set()
        self.height = 0
        self.width = 0
        for (y, line) in enumerate(open(fname, "rt")):
            for (x, col) in enumerate(line.rstrip()):
                if col == "O":
                    self.movable.append((x, y))
                    self.used.add((x, y))
                elif col == "#":
                    self.used.add((x, y))
                self.width = max(x + 1, self.width)
            self.height = max(y + 1, self.height)

        # Add solid border
        for x in range(-1, self.width + 2):
            self.used.add((x, -1))
            self.used.add((x, self.height))
        for y in range(-1, self.height + 2):
            self.used.add((-1, y))
            self.used.add((self.width, y))

    def sort_for(self, dx: int, dy: int) -> None:
        self.movable.sort(key = lambda xy: (- (dx * xy[0]) - (dy * xy[1]), xy))

    def move(self, dx: int, dy: int) -> None:
        self.sort_for(dx, dy)
        moving = True
        while moving:
            moving = False
            for i in range(len(self.movable)):
                (x, y) = self.movable[i]
                while (x + dx, y + dy) not in self.used:
                    # Can move it
                    self.used.remove((x, y))
                    x += dx
                    y += dy
                    self.used.add((x, y))
                    self.movable[i] = (x, y)
                    moving = True

    def part1(self) -> int:
        self.move(0, -1)
        return self.evaluate()

    def evaluate(self) -> int:
        total = 0
        for i in range(len(self.movable)):
            (x, y) = self.movable[i]
            total += self.height - y
        return total

    def hash(self) -> bytes:
        self.sort_for(0, -1)
        s = hashlib.sha256()
        for (x, y) in self.movable:
            s.update(struct.pack("HH", x, y))
        return s.digest()

    def part2(self) -> int:
        known_state: typing.Dict[bytes, int] = {}
        count = 0
        state = self.hash()
        while state not in known_state:
            known_state[state] = count
            self.move(0, -1) # N
            self.move(-1, 0) # W
            self.move(0, 1)  # S
            self.move(1, 0)  # E
            count += 1
            state = self.hash()
       
        same_first = known_state[state]
        same_again = count
        #print(f"State {count} and {known_state[state]} are the same")
        go_to = 1000000000
        same_as_goto = ((go_to - same_first) % (same_again - same_first)) + same_again
        #print(f"Therefore {go_to} and {same_as_goto} are the same")
        #print(f"Wind forward by {same_as_goto - count}")
        assert count <= same_as_goto
        while count < same_as_goto:
            self.move(0, -1) # N
            self.move(-1, 0) # W
            self.move(0, 1)  # S
            self.move(1, 0)  # E
            count += 1

        return self.evaluate()


def main() -> None:
    assert Problem("test").part1() == 136
    print(Problem("input").part1())
    assert Problem("test").part2() == 64
    print(Problem("input").part2())

if __name__ == "__main__":
    main()
