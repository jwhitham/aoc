# This program checks the log tape which is tape 4 (part2.mt4)
# against the data produced by part2a.py

import struct, sys

from_tape_4 = open("part2.mt4", "rb")
tapecheck_data = open("tapecheck.data", "rt")
height = 0
problem = open("input", "rt")
for line in problem:
    height += 1

count = 0
error = 0

while True:
    pos = from_tape_4.tell()
    b = from_tape_4.read(4)
    if len(b) == 0:
        break
  
    (size, ) = struct.unpack("<I", b)
    data = from_tape_4.read(size)

    y = count % height
    if ((count // height) % 2) == 0:
        print("tapecheck line {}: NTS pass {} line {}".format(count + 1, (count // height) // 2, y))
    else:
        y = height - 1 - y
        print("tapecheck line {}: STN pass {} line {}".format(count + 1, (count // height) // 2, y))
    count += 1

    assert len(data) == size, (len(data), size)
    b = from_tape_4.read(4)
    (check, ) = struct.unpack("<I", b)
    assert check == size

    line = tapecheck_data.readline().strip()
  
    assert len(line) == size
    for x in range(size):
        bad = False
        got = data[x]
        expected = line[x]
        if 0 < got < 10:
            # numerical
            if expected != str(got):
                bad = True
        elif got == 10:
            if expected != "0":
                bad = True
        elif got == 59:
            if expected != ".":
                bad = True
        elif got == 21:
            if expected != "V":
                bad = True
        else:
            bad = True

        if bad:
            print("location y = {} x = {} expected = {} got = {}".format(y, x, expected, got))
            error += 1
            assert error < 10


