from typing import Tuple


def parse_line(line: str) -> Tuple[str, int]:
    direction, count = line.split()
    return direction, int(count)


def move(path) -> Tuple[int, int]:
    forwards, depth = 0, 0

    with open(path) as f:
        while line := f.readline():
            direction, count = parse_line(line)
            if direction == "forward":
                forwards += count
            elif direction == "down":
                depth += count
            else:
                depth -= count

    return forwards, depth


def move_aimed(path) -> Tuple[int, int]:
    forwards, depth = 0, 0
    aim = 0

    with open(path) as f:
        while line := f.readline():
            direction, count = parse_line(line)
            if direction == "forward":
                forwards += count
                depth += count * aim
            elif direction == "down":
                aim += count
            else:
                aim -= count

    return forwards, depth


def test_part_1():
    f, d = move("./data/example.txt")
    correct_f = 15
    correct_d = 10
    assert correct_f == f, f"{correct_f} != {f}"
    assert correct_d == d, f"{correct_d} != {d}"


def test_part_2():
    f, d = move_aimed("./data/example.txt")
    correct_f = 15
    correct_d = 60
    assert correct_f == f, f"{correct_f} != {f}"
    assert correct_d == d, f"{correct_d} != {d}"


def part_1():
    f, d = move("./data/input.txt")
    print("Solution part 1:")
    print(f"Forwards: {f}")
    print(f"Depth: {d}")
    print(f"Multiplication: {f * d}")


def part_2():
    f, d = move_aimed("./data/input.txt")
    print("Solution part 2:")
    print(f"Forwards: {f}")
    print(f"Depth: {d}")
    print(f"Multiplication: {f * d}")


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
