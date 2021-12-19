from abc import ABC, abstractmethod
from functools import reduce
from typing import List, Optional, Iterable
from io import StringIO

import numpy as np


class CountedStringIO(StringIO):
    def __init__(self, string, limit: Optional[int] = None):
        super().__init__(string)
        self.read_bytes = ""
        self.limit = limit

    def read(self, __size: Optional[int] = ...) -> str:
        if self.limit and len(self.read_bytes) + __size > self.limit:
            raise Exception("Limit exceeded")

        string = super().read(__size)
        self.read_bytes += string
        return string


class Packet(ABC):
    def __init__(self, bitstream: CountedStringIO, version=None, type_id=None):
        self.bitstream = bitstream
        if version is None:
            self.version = self._get_version()
        else:
            self.version = version

        if type_id is None:
            self.type_id = self._get_type_id()
        else:
            self.type_id = type_id

    @property
    @abstractmethod
    def value(self):
        ...

    def _get_version(self) -> int:
        binary = self.bitstream.read(3)
        return int(binary, 2)

    def _get_type_id(self):
        binary = self.bitstream.read(3)
        return int(binary, 2)

    def __iter__(self):
        yield self


class LiteralPacket(Packet):
    def __init__(self, bitstream: CountedStringIO, version=None, type_id=None):
        super().__init__(bitstream, version, type_id)
        if self.type_id != 4:
            raise Exception("LiteralPacket initialized with value other than 4")

        self._value = self._get_value()

    @property
    def value(self):
        return self._value

    def _get_value(self) -> int:
        binary = ""

        while bits := self.bitstream.read(5):
            cont = bool(int(bits[0]))
            binary += bits[1:]

            if not cont:
                return int(binary, 2)
        raise Exception("No bits or they don't end")

    def __repr__(self):
        return f"{{LiteralPacket V: {self.version}, T: {self.type_id}, Value: {self.value}}}"


class OperatorPacket(Packet):
    def __init__(self, bitstream: CountedStringIO, version=None, type_id=None):
        super().__init__(bitstream, version, type_id)
        self.sub_packets = self._get_sub_packets()
        self._value = self.value

    @property
    def value(self):
        def prod(values: List[int]):
            return reduce((lambda x, y: x * y), values)

        def gt(values: Iterable):
            return reduce((lambda x, y: x > y), values)

        def lt(values: Iterable):
            return reduce((lambda x, y: x < y), values)

        def eq(values: Iterable):
            return reduce((lambda x, y: x == y), values)

        if self.type_id == 0:
            op = sum
        elif self.type_id == 1:
            op = prod
        elif self.type_id == 2:
            op = min
        elif self.type_id == 3:
            op = max
        elif self.type_id == 5:
            op = gt
        elif self.type_id == 6:
            op = lt
        elif self.type_id == 7:
            op = eq
        else:
            raise Exception(f"Invalid type_id {self.type_id}")
        return op([p.value for p in self.sub_packets])

    def _get_length_type_id(self) -> int:
        return int(self.bitstream.read(1), 2)

    def _get_packet_length(self, length_type: int) -> int:
        if length_type == 0:
            return int(self.bitstream.read(15), 2)
        return int(self.bitstream.read(11), 2)

    def _get_sub_packets(self) -> List[Packet]:
        length_type = self._get_length_type_id()
        packet_length = self._get_packet_length(length_type)
        if length_type == 0:
            return PacketFactory.parse_bits(self.bitstream, packet_length)
        if length_type == 1:
            return [PacketFactory.parse_single_packet(self.bitstream) for _ in range(packet_length)]

    def __repr__(self):
        return f"{{OperatorPacket V: {self.version}, T: {self.type_id}, Subpackets: {self.sub_packets}}}"

    def __iter__(self):
        yield self
        for sub_packet in self.sub_packets:
            for packet in sub_packet:
                yield packet


class PacketFactory:
    @staticmethod
    def parse_packets(bitstream: CountedStringIO, packet_limit: Optional[int] = 1) -> List[Packet]:
        packets = []
        for _ in range(packet_limit):
            packet = PacketFactory.parse_single_packet(bitstream)
            packets.append(packet)
            if packet_limit:
                if len(packets) == packet_limit:
                    break
                if len(packets) > packet_limit:
                    raise Exception("Packet limit exceeded")

        return packets

    @staticmethod
    def parse_bits(bitstream: CountedStringIO, size: int) -> List[Packet]:
        packets = []
        start_count = len(bitstream.read_bytes)
        while True:
            packet = PacketFactory.parse_single_packet(bitstream)
            packets.append(packet)
            read_bytes = len(bitstream.read_bytes) - start_count

            if read_bytes == size:
                return packets
            if read_bytes > size:
                raise Exception("Exceeded read limit")

    @staticmethod
    def parse_single_packet(bitstream: CountedStringIO) -> Packet:
        version = PacketFactory._get_version(bitstream)
        type_id = PacketFactory._get_type_id(bitstream)
        if type_id == 4:
            return LiteralPacket(bitstream, version, type_id)
        return OperatorPacket(bitstream, version, type_id)

    @staticmethod
    def _get_version(bitstream) -> int:
        binary = bitstream.read(3)
        if binary == "":
            return 0
        return int(binary, 2)

    @staticmethod
    def _get_type_id(bitstream):
        binary = bitstream.read(3)
        return int(binary, 2)


def parse_input(path: str) -> str:
    with open(path) as f:
        return f.readline().strip()


def hex_to_bin(hexa: str) -> str:
    binary = np.base_repr(int(hexa, 16), base=2)

    # left pad the right number of zeroes
    binary = "0" * (len(hexa) * 4 - len(binary)) + binary
    return binary


def test_example_1():
    inp = parse_input("data/example.txt")
    bits = hex_to_bin(inp)

    packet = PacketFactory.parse_single_packet(CountedStringIO(bits))

    assert type(packet) is LiteralPacket, f"Packet not parsed as a LiteralPacket"

    version = packet.version
    assert 6 == version, f"Incorrect version, expected 6 but got {version}"

    type_id = packet.type_id
    assert 4 == type_id, f"Incorrect type ID, expected 4 but got {type_id}"

    literal = packet.value
    assert 2021 == literal, f"Incorrect literal, expected 2021 but got {literal}"


def test_example_2(hexa):
    bits = hex_to_bin(hexa)
    packet = PacketFactory.parse_single_packet(CountedStringIO(bits))

    assert type(packet) is OperatorPacket, f"Packet not parsed as a OperatorPacket"

    version = packet.version
    assert 1 == version, f"Incorrect version, expected 1 but got {version}"

    type_id = packet.type_id
    assert 6 == type_id, f"Incorrect type ID, expected 6 but got {type_id}"

    packets = [p for p in packet]
    expected = [10, 20]
    for packet, expected_value in zip(packets[1:], expected):
        assert type(packet) is LiteralPacket, f"Packet not parsed as a Literal"
        assert expected_value == packet.value, f"Incorrect literal, expected {expected_value} but got {packet.value}"


def test_example_3(hexa):
    bits = hex_to_bin(hexa)
    packet = PacketFactory.parse_single_packet(CountedStringIO(bits))

    packets = [p for p in packet]

    assert 4 == len(packets), f"Expected 4 packets instead of {len(packets)}"
    expected_types = [OperatorPacket, LiteralPacket, LiteralPacket, LiteralPacket]
    expected_versions = [7, 2, 4, 1]
    expected_type_ids = [3, 4, 4, 4]
    for packet, t, v, tid in zip(packets, expected_types, expected_versions, expected_type_ids):
        assert type(packet) is t, f"Packet parsed as {type(packet)} instead of {type(t)}"
        assert v == packet.version, f"Expected version to be {v} instead it is {packet.version}"
        assert tid == packet.type_id, f"Expected typeID to be {tid} instead it is {packet.type_id}"


def test_part_one_example(hexa, expected_sum):
    bits = hex_to_bin(hexa)
    packet = PacketFactory.parse_single_packet(CountedStringIO(bits))
    versions = [p.version for p in packet]
    version_sum = sum(versions)
    assert expected_sum == version_sum, f"Example {hexa}: Expected sum to be {expected_sum}, " \
                                        f"got {version_sum} ({versions})"


def part_1():
    inp = parse_input(f"./data/input.txt")
    bits = hex_to_bin(inp)
    packet = PacketFactory.parse_single_packet(CountedStringIO(bits))
    solution = sum([p.version for p in packet])
    print("Solution Part 1:")
    print(solution)


def test_part_two_example(hexa, expected_result):
    bits = hex_to_bin(hexa)
    packet = PacketFactory.parse_single_packet(CountedStringIO(bits))
    assert expected_result == packet.value, f"Example {hexa}: Expected result to be {expected_result}, " \
                                            f"got {packet.value} ({packet})"


def part_2():
    inp = parse_input(f"./data/input.txt")
    bits = hex_to_bin(inp)
    packet = PacketFactory.parse_single_packet(CountedStringIO(bits))
    solution = packet.value
    print("Solution Part 2:")
    print(solution)


if __name__ == '__main__':
    test_example_1()
    test_example_2("38006F45291200")
    test_example_3("EE00D40C823060")
    test_part_one_example("8A004A801A8002F478", 16)
    test_part_one_example("620080001611562C8802118E34", 12)
    test_part_one_example("C0015000016115A2E0802F182340", 23)
    test_part_one_example("A0016C880162017C3686B18A3D4780", 31)
    part_1()
    print()
    test_part_two_example("C200B40A82", 3)
    test_part_two_example("04005AC33890", 54)
    test_part_two_example("880086C3E88112", 7)
    test_part_two_example("CE00C43D881120", 9)
    test_part_two_example("D8005AC2A8F0", 1)
    test_part_two_example("F600BC2D8F", 0)
    test_part_two_example("9C005AC2F8F0", 0)
    test_part_two_example("9C0141080250320F1802104A08", 1)
    part_2()
