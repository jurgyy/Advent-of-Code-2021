from operator import itemgetter
from typing import Tuple, List

import numpy as np


def parse_input(path: str) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    with open(path) as f:
        part1 = True
        coords = []
        folds = []
        while line := f.readline():
            line = line.strip()
            if line == "":
                part1 = False
                continue

            if part1:
                x, y = line.split(",")
                coords.append((int(x), int(y)))
            else:
                fold = line.split(" ")[-1]
                axis, position = fold.split("=")

                # [y=7, x=5] --> [(0, 7), (1, 5)]
                folds.append((int(axis == "x"), int(position)))

    return coords, folds


def coords_to_array(coords: List[Tuple[int, int]]):
    max_x, _ = max(coords, key=itemgetter(0))
    _, max_y = max(coords, key=itemgetter(1))

    arr = np.zeros((max_y + 1, max_x + 1), dtype=bool)

    for x, y in coords:
        arr[y, x] = True

    return arr


def print_array(arr: np.ndarray):
    for row in arr:
        for val in row:
            print("#" if val else ".", end="")
        print()


def do_fold(arr: np.ndarray, position: int, axis: int) -> np.ndarray:
    if axis == 0:
        u = arr[: position, :]
        d = np.flip(arr[position + 1:, :], axis=axis)

        if u.shape[axis] > d.shape[axis]:
            pad_size = u.shape[axis] - d.shape[axis]
            d = np.pad(d, ((pad_size, 0), (0, 0)), "constant", constant_values=False)
        else:
            pad_size = d.shape[axis] - u.shape[axis]
            u = np.pad(u, ((pad_size, 0), (0, 0)), "constant", constant_values=False)

        return u + d
    else:
        l = arr[:, : position]
        r = np.flip(arr[:, position + 1:], axis=axis)

        if l.shape[axis] > r.shape[axis]:
            pad_size = l.shape[axis] - r.shape[axis]
            r = np.pad(r, ((0, 0), (pad_size, 0)), "constant", constant_values=False)
        else:
            pad_size = r.shape[axis] - l.shape[axis]
            l = np.pad(l, ((0, 0), (pad_size, 0)), "constant", constant_values=False)

        return l + r


def test_part_1():
    coords, folds = parse_input("./data/example.txt")
    arr = coords_to_array(coords)
    axis, position = folds[0]
    arr = do_fold(arr, position, axis)

    solution = np.sum(arr)
    correct = 17
    assert correct == solution, f"{correct} != {solution}"


def part_1():
    coords, folds = parse_input("./data/input.txt")
    arr = coords_to_array(coords)
    axis, position = folds[0]
    arr = do_fold(arr, position, axis)

    solution = np.sum(arr)
    print("Solution part 1:")
    print(solution)


def part_2():
    coords, folds = parse_input("./data/input.txt")
    arr = coords_to_array(coords)

    for axis, position in folds:
        arr = do_fold(arr, position, axis)

    print("Solution part 2:")
    print_array(arr)


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    part_2()
