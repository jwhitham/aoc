import struct

problem = open("input", "rb")
out = open("part1.mt1", "wb")

data = []
for line in problem:
    data.append(line.strip().replace(b".", b";"))

def encode_digit(value):
    value %= 10
    if value == 0:
        return b"\x0a"
    else:
        return struct.pack("<B", value)

def encode_word(value):
    assert 0 <= value < 1000
    return (b"\x1d" +
                encode_digit(value // 100) +
                encode_digit(value // 10) +
                encode_digit(value))

def encode_block(data, pad):
    size = len(data)
    return struct.pack("<I", size) + data + (b"\x00" * pad) + struct.pack("<I", size)

width = len(data[0])
height = len(data)

header = (b"\x1d\x39\x1d" +
          b"\x0a\x01\x02\x03\x04\x05\x06\x07" +
          b"\x08\x09\x31\x32\x33\x34\x35\x36" +
          encode_word(width) +
          encode_word(height) +
          encode_word(0) +
          encode_word(0))

out.write(encode_block(header, 1))

line = b";" * width
out.write(encode_block(line, 0))

for line in data:
    out.write(encode_block(line, 0))

line = b";" * width
out.write(encode_block(line, 0))
