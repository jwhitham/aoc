
import struct, sys

from_tape_2 = open("part2.mt2", "rb")
expected = open("x2", "rt")
expected.readline()

while True:
    pos = from_tape_2.tell()
    b = from_tape_2.read(4)
    if len(b) == 0:
        break
  
    (size, ) = struct.unpack("<I", b)
    print("{:08x} {:08x} ".format(pos, size))
    data = from_tape_2.read(size)

    assert len(data) == size, (len(data), size)
    b = from_tape_2.read(4)
    (check, ) = struct.unpack("<I", b)
    assert check == size

    line = expected.readline().strip()
  
    assert len(line) == size
    for i in range(size):
        v = data[i]
        if v < 10:
            # numerical
            assert int(line[i]) == v
        elif v == 59:
            # "."
            assert line[i] == "."
        else:
            assert False
            print(line[i])
            print(v)


