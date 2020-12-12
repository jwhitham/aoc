
import struct, sys

x = open(sys.argv[1], "rb")
while True:
    pos = x.tell()
    b = x.read(4)
    if len(b) == 0:
        break
  
    (size, ) = struct.unpack("<I", b)
    print("{:08x} {:08x} ".format(pos, size), end="")
    data = x.read(size)

    assert len(data) == size, (len(data), size)
    b = x.read(4)
    gap = 0
    while True:
        assert len(b) == 4
        (check, ) = struct.unpack("<I", b)
        if check == size:
            break

        b = b[1:] + x.read(1) 
        gap += 1

    if pos > 0:
        data = data.replace(b"#", b"L")   # unoccupied (coincidence: 1401 is not ASCII)
        data = data.replace(b";", b".")   # floor
        data = data.replace(b"\x0b", b"#")# occupied
        text = data.decode("ascii", errors="ignore")
    else:
        text = repr(data)
    print (gap, text)
    


