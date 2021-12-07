import re
from typing import List, Tuple

import numpy as np


def is_diagonal(x1: int, y1: int, x2: int, y2: int) -> bool:
    return abs(x1 - x2) == abs(y1 - y2)


def parse_input(path: str, allow_diagonal=False) -> Tuple[List[Tuple[int, int, int, int]], int, int]:
    lines = []
    max_x = 0
    max_y = 0

    with open(path) as f:
        while line := f.readline():
            m = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line)
            x1, y1, x2, y2 = m.groups()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            if x1 != x2 and y1 != y2:
                if not allow_diagonal or not is_diagonal(x1, y1, x2, y2):
                    continue

            lines.append((x1, y1, x2, y2))

            if x1 > max_x:
                max_x = x1
            if x2 > max_x:
                max_x = x2
            if y1 > max_y:
                max_y = y1
            if y2 > max_y:
                max_y = y2

    return lines, max_x, max_y


def draw_diagonal(arr: np.ndarray, x1: int, y1: int, x2: int, y2: int):
    x_stride = -1 if x1 > x2 else 1
    y_stride = -1 if y1 > y2 else 1

    for x, y in zip(range(x1, x2 + x_stride, x_stride), range(y1, y2 + y_stride, y_stride)):
        arr[y, x] += 1


def draw_lines(lines: List[Tuple[int, int, int, int]], max_x: int, max_y: int) -> np.ndarray:
    arr = np.zeros((max_y + 1, max_x + 1), dtype=int)
    for line in lines:
        x1, y1, x2, y2 = line
        if is_diagonal(x1, y1, x2, y2):
            draw_diagonal(arr, x1, y1, x2, y2)
        else:
            if x2 < x1:
                x1, x2 = x2, x1
            if y2 < y1:
                y1, y2 = y2, y1

            arr[y1:y2 + 1, x1:x2 + 1] += 1
    return arr


def count_dangerous(arr: np.ndarray, min_dangerous: int) -> int:
    return np.sum(arr >= min_dangerous)


def print_danger(arr: np.ndarray):
    print("  0123456789")
    for i, a in enumerate(arr):
        print(i, "".join([str(v) if v > 0 else "." for v in a]))


def find_danger(path: str, allow_diagonal=False) -> int:
    lines, max_x, max_y = parse_input(path, allow_diagonal)
    arr = draw_lines(lines, max_x, max_y)
    return count_dangerous(arr, 2)


def test_part_1():
    solution = find_danger("./data/example.txt")
    correct = 5
    assert correct == solution, f"{correct} != {solution}"


def part_1():
    solution = find_danger("./data/input.txt")
    print("Solution part 1:")
    print(solution)


def test_part_2():
    solution = find_danger("./data/example.txt", allow_diagonal=True)
    correct = 12
    assert correct == solution, f"{correct} != {solution}"


def part_2():
    solution = find_danger("./data/input.txt", allow_diagonal=True)
    print("Solution part 2:")
    print(solution)


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
