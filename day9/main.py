from typing import Tuple, List, Set

import numpy as np
from util import Colors


def parse_input(path: str) -> np.ndarray:
    with open(path) as f:
        data = []
        while line := f.readline():
            data.append(list(map(int, list(line.strip()))))
        return np.array(data)


def local_minimum(data: np.ndarray) -> np.ndarray:
    mask = []
    for y, row in enumerate(data):
        mask.append([])
        for x, val in enumerate(row):
            a = val < data[y - 1, x] if y > 0 else True
            b = val < data[y + 1, x] if y < data.shape[0] - 1 else True
            d = val < data[y, x - 1] if x > 0 else True
            c = val < data[y, x + 1] if x < data.shape[1] - 1 else True
            mask[-1].append(a and b and c and d)
    return np.array(mask)


def get_risk(data: np.ndarray, mask: np.ndarray) -> int:
    return np.sum(data[mask] + 1)


def test_part_1():
    data = parse_input("./data/example.txt")
    mask = local_minimum(data)
    solution = get_risk(data, mask)
    correct = 15
    assert correct == solution, f"{correct} != {solution}"


def part_1():
    data = parse_input("./data/input.txt")
    solution = get_risk(data, local_minimum(data))
    print("Solution part 1:")
    print(solution)


def breath_first_search(data: np.ndarray, rooty: int, rootx: int) -> Set[Tuple[int, int]]:
    queue = []
    root = (rooty, rootx)
    explored = {root}
    queue.append(root)

    while queue:
        vy, vx = queue.pop(0)

        tx, ty = vx, vy + 1
        bx, by = vx, vy - 1
        lx, ly = vx - 1, vy
        rx, ry = vx + 1, vy

        for x, y in [(tx, ty), (bx, by), (lx, ly), (rx, ry)]:
            if x < 0 or x >= data.shape[1] or y < 0 or y >= data.shape[0]:
                continue
            if data[y, x] < 9 and not (y, x) in explored:
                explored.add((y, x))
                queue.append((y, x))
    return explored


def get_basins(data: np.ndarray, mask: np.ndarray) -> List[List[Tuple[int, int]]]:
    basins = []
    for point in np.argwhere(mask):
        if any([tuple(point) in basin for basin in basins]):
            # overlapping basins
            continue

        basin_coords = breath_first_search(data, *point)
        basins.append(list(basin_coords))

    return basins


def get_basin_sizes(basins: List[List[Tuple[int, int]]]) -> List[int]:
    return list(map(len, basins))


def get_prod_largest_n(sizes: List[int], n: int) -> int:
    sizes = sorted(sizes, reverse=True)
    return np.prod(sizes[:n])


def print_basins(data: np.ndarray, basins: List[List[Tuple[int, int]]]):
    masks = []
    for basin in basins:
        masks.append(np.zeros(data.shape, dtype=bool))
        for y, x in basin:
            masks[-1][y, x] = True

    colors = [Colors.fgBlue, Colors.fgRed, Colors.fgCyan, Colors.fgGreen,
              Colors.fgBrightBlue, Colors.fgBrightRed, Colors.fgBrightCyan, Colors.fgBrightGreen,
              Colors.fgBrightMagenta, Colors.fgMagenta, Colors.fgYellow, Colors.fgBrightYellow]

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            printed = False
            for i, mask in enumerate(masks):
                color = colors[i % len(colors)]

                if mask[y, x]:
                    printed = True
                    print(f"{color}{data[y,x]}{Colors.reset}", end='')

            if data[y, x] == 9:
                print(".", end="")
            elif not printed:
                print({data[y, x]}, end='')
        print()


def test_part_2():
    data = parse_input("./data/example.txt")
    mask = local_minimum(data)
    basins = get_basins(data, mask)
    print_basins(data, basins)
    sizes = get_basin_sizes(basins)
    solution = get_prod_largest_n(sizes, 3)

    correct = 1134
    assert correct == solution, f"{correct} != {solution}"


def part_2():
    data = parse_input("./data/input.txt")
    mask = local_minimum(data)
    basins = get_basins(data, mask)
    print_basins(data, basins)

    sizes = get_basin_sizes(basins)
    solution = get_prod_largest_n(sizes, 3)

    print("Solution part 2:")
    print(solution)


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
