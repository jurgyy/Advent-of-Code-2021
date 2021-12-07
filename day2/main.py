from typing import Tuple


def parse_line(line: str) -> Tuple[str, int]:
    direction, count = line.split()
    return direction, int(count)


def move(path) -> Tuple[int, int, int]:
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

    return forwards, depth, forwards * depth


def move_amied(path) -> Tuple[int, int, int]:
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

    return forwards, depth, forwards * depth


def test_part_1():
    f, d, m = move("./data/example.txt")
    correct_f = 15
    correct_d = 10
    correct_m = correct_d * correct_f
    assert correct_f == f, f"{correct_f} != {f}"
    assert correct_d == d, f"{correct_d} != {d}"
    assert correct_m == m, f"{correct_m} != {m}"


def test_part_2():
    f, d, m = move_amied("./data/example.txt")
    correct_f = 15
    correct_d = 60
    correct_m = correct_d * correct_f
    assert correct_f == f, f"{correct_f} != {f}"
    assert correct_d == d, f"{correct_d} != {d}"
    assert correct_m == m, f"{correct_m} != {m}"


def part_1():
    f, d, m = move("./data/input.txt")
    print("Solution part 1:")
    print(f"Forwards: {f}")
    print(f"Depth: {d}")
    print(f"Multiplication: {m}")


def part_2():
    f, d, m = move_amied("./data/input.txt")
    print("Solution part 2:")
    print(f"Forwards: {f}")
    print(f"Depth: {d}")
    print(f"Multiplication: {m}")


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
