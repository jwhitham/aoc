YEAR = 2021
DAY = 16
PART = 3
 
from pathlib import Path
import unittest
import typing
import subprocess
import collections
import sys
import os

INPUT = Path("input")

class PacketReader:
    def __init__(self, lump: str) -> None:
        self.bits: typing.Deque[int] = collections.deque()
        for hex_char in lump:
            try:
                hex_val = int(hex_char, 16)
            except Exception:
                continue

            for i in range(4):
                self.bits.append(((hex_val << i) >> 3) & 0x1)

    def get(self) -> int:
        return self.bits.popleft()

    def get_n(self, n: int) -> int:
        p = 0
        for i in range(n):
            p = p << 1
            p |= self.get()
        return p

    @property
    def remaining(self) -> int:
        return len(self.bits)

VALUE = 4

class Packet:
    def __init__(self, pr: PacketReader) -> None:
        self.version = pr.get_n(3)
        self.ptype = pr.get_n(3)
        self.value = 0
        self.subpackets: typing.List[Packet] = []

        if self.ptype == VALUE:
            while pr.get() == 1:
                self.value = self.value << 4
                self.value |= pr.get_n(4)

            self.value = self.value << 4
            self.value |= pr.get_n(4)

        else:
            # read length type id 
            if pr.get() == 0:
                length = pr.get_n(15)
                while length > 0:
                    start = pr.remaining
                    self.subpackets.append(Packet(pr))
                    finish = pr.remaining
                    assert finish < start
                    length -= (start - finish)
                    assert length >= 0
            else:
                count = pr.get_n(11)
                for i in range(count):
                    self.subpackets.append(Packet(pr))

    def version_sum(self) -> int:
        s = self.version
        for p in self.subpackets:
            s += p.version_sum()
        return s

    def calculate(self) -> int:
        if self.ptype == 4:
            return self.value

        s = self.subpackets[0].calculate()
        if self.ptype == 0:
            for p in self.subpackets[1:]:
                s += p.calculate()

        elif self.ptype == 1:
            for p in self.subpackets[1:]:
                s *= p.calculate()

        elif self.ptype == 2:
            for p in self.subpackets[1:]:
                s = min(s, p.calculate())

        elif self.ptype == 3:
            for p in self.subpackets[1:]:
                s = max(s, p.calculate())

        elif self.ptype == 5:
            s = 1 if s > self.subpackets[1].calculate() else 0

        elif self.ptype == 6:
            s = 1 if s < self.subpackets[1].calculate() else 0

        else:
            s = 1 if s == self.subpackets[1].calculate() else 0

        return s

def test1() -> None:
    h = "D2FE28"
    b = "110100101111111000101000"
    assert PacketReader(h).get_n(len(b)) == int(b, 2)
    p = Packet(PacketReader(h))
    assert p.version == 6
    assert p.ptype == VALUE
    assert p.value == 2021

def test2() -> None:
    h = "38006F45291200"
    b = "00111000000000000110111101000101001010010001001000000000"
    assert PacketReader(h).get_n(len(b)) == int(b, 2)
    p = Packet(PacketReader(h))
    assert p.version == 1
    assert p.ptype == 6
    assert len(p.subpackets) == 2
    p0 = p.subpackets[0]
    p1 = p.subpackets[1]
    assert p0.ptype == VALUE
    assert p0.value == 10
    assert p1.ptype == VALUE
    assert p1.value == 20

def test3() -> None:
    h = "EE00D40C823060"
    b = "11101110000000001101010000001100100000100011000001100000"
    assert PacketReader(h).get_n(len(b)) == int(b, 2)
    p = Packet(PacketReader(h))
    assert p.version == 7
    assert p.ptype == 3
    assert len(p.subpackets) == 3
    p0 = p.subpackets[0]
    p1 = p.subpackets[1]
    p2 = p.subpackets[2]
    assert p0.ptype == VALUE
    assert p0.value == 1
    assert p1.ptype == VALUE
    assert p1.value == 2
    assert p2.ptype == VALUE
    assert p2.value == 3

def test4() -> None:
    def t(s: str) -> int:
        return Packet(PacketReader(s)).version_sum()

    assert t("8A004A801A8002F478") == 16
    assert t("620080001611562C8802118E34") == 12
    assert t("C0015000016115A2E0802F182340") == 23
    assert t("A0016C880162017C3686B18A3D4780") == 31

def thing1(filename: Path) -> int:
    return Packet(PacketReader(open(filename, "rt").read())).version_sum()

def test5() -> None:
    def t(s: str) -> int:
        return Packet(PacketReader(s)).calculate()

    assert t("C200B40A82") == 3
    assert t("04005AC33890") == 54
    assert t("880086C3E88112") == 7
    assert t("CE00C43D881120") == 9
    assert t("D8005AC2A8F0") == 1
    assert t("F600BC2D8F") == 0
    assert t("9C005AC2F8F0") == 0
    assert t("9C0141080250320F1802104A08") == 1
    assert t("D2FE28") == 2021

def thing2(filename: Path) -> int:
    return Packet(PacketReader(open(filename, "rt").read())).calculate()

def main() -> None:
    if not INPUT.exists():
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY), "download"])
        return

    subprocess.check_call([sys.executable, "-m", "mypy", sys.argv[0]])
    subprocess.check_call([sys.executable, "-m", "pytest", sys.argv[0]])

    answer = thing1(INPUT)
    print("part 1:", answer)

    if PART == 1:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "1", str(answer)])
        return

    answer = thing2(INPUT)
    print("part 2:", answer)

    if PART == 2:
        subprocess.check_call(["aoc", "-y", str(YEAR), "-d", str(DAY),
                               "submit", "2", str(answer)])
        return


if __name__ == "__main__":
    main()


