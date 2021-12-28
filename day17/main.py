import itertools
import math
import re
import time
import timeit
from contextlib import redirect_stderr
from typing import Tuple, List

import numba as nb
import numpy as np
import joblib

np.set_printoptions(edgeitems=30, linewidth=100000)


def parse_input(path: str) -> Tuple[int, int, int, int]:
    with open(path) as f:
        line = f.readline()
        (x_min, x_max), (y_min, y_max) = re.findall(r"\w=(-?\d+)\.\.(-?\d+)", line)
    return int(x_min), int(x_max), int(y_min), int(y_max)


@nb.jit(nb.int64(nb.int64), nopython=True)
def cumsum(n: int) -> int:
    return int(n * (n + 1) / 2)


@nb.jit(nb.float64(nb.int64), nopython=True)
def cumsum_inverse(n: int) -> float:
    return 0.5 * (math.sqrt(8 * n + 1) - 1)


@nb.njit
def change_velocity(vx, vy):
    return vx - 1 if vx > 0 else vx + 1 if vx < 0 else vx, vy - 1


def plot_trajectory(vx, vy, x_min, x_max, y_min, y_max):
    def print_array(data):
        print(data)
        for row in data:
            for v in row:
                if v == 0:
                    c = "."
                elif v == 1:
                    c = "T"
                elif v == 2 or v == 4:
                    c = "#"
                elif v == 3:
                    c = "X"
                else:
                    raise NotImplementedError(str(v))
                print(c, end="")
            print()
            # print("".join(["." if v == 0 else "#" if v == 1 else "T" for v in row.tolist()]))

    arr, _ = calc_trajectory_target_array(vx, vy, x_min, x_max, y_min, y_max)
    print_array(arr)


@nb.njit
def calc_trajectory_target_array(vx: int, vy: int, x_min: int, x_max: int, y_min: int, y_max: int)\
        -> Tuple[np.ndarray, int]:
    xs, ys = get_trajectory_steps(vx, vy, x_max, y_min)
    max_x_pos = max(max(xs) + 1, x_max + 1)
    min_y_pos, max_y_pos = min(min(ys) - 1, y_min - 1), max(max(ys), y_max + 1)
    y_offset = max_y_pos
    arr = np.zeros((max_y_pos - min_y_pos, max_x_pos), dtype=np.int8)
    arr[-y_max + y_offset: -y_min + y_offset + 1, x_min: x_max + 1] = 1
    for y, x in zip(ys, xs):
        arr[-y + y_offset, x] += 2
    return arr, y_offset


@nb.njit
def get_trajectory_steps(vx: int, vy: int, x_max: int, y_min: int) -> Tuple[List[int], List[int]]:
    x_pos = 0
    y_pos = 0
    xs = [0]
    ys = [0]
    while not (x_pos > x_max or y_pos <= y_min):
        x_pos += vx
        y_pos += vy

        xs.append(x_pos)
        ys.append(y_pos)

        vx, vy = change_velocity(vx, vy)
    return xs, ys


def trajectory_hits(xs, ys, x_min, x_max, y_min, y_max):
    return any([x_min <= x <= x_max and y_min <= y <= y_max for x, y in zip(xs, ys)])


def get_min_vx(x_min, x_max):
    vx = 0
    while True:
        if x_min <= cumsum(vx) <= x_max:
            break
        vx += 1
    return vx


def get_vxs(x_min, x_max):
    return [int(cumsum_inverse(x)) for x in range(x_min, x_max + 1) if cumsum_inverse(x).is_integer()]


def get_vys_brute_force(y_min, y_max, upper_bound=100000):
    ys = []
    for vy in range(upper_bound):
        if hits_y(vy, y_min, y_max):
            ys.append(vy)
    return ys


@nb.njit
def get_max_vy(y_min, y_max, upper_bound=100000):
    last_hit_vy = None
    for vy in range(upper_bound):
        if hits_y(vy, y_min, y_max):
            last_hit_vy = vy
    return last_hit_vy


@nb.njit
def get_max_height(vy):
    return cumsum(vy)


@nb.njit
def hits_y(vy, y_min, y_max):
    max_height = cumsum(vy)
    return math.floor(cumsum_inverse(max_height - y_min)) >= cumsum_inverse(max_height - y_max)


@nb.njit
def hits_x(vx, x_max, x_min):
    max_width = cumsum(vx)
    return max_width >= x_min and math.floor(cumsum_inverse(x_max)) >= cumsum_inverse(x_min)


def hits(vx, vy, x_min, x_max, y_min, y_max):
    # todo failes if it enters horizontally and leaves vertically (or vice versa) (fine for part 1 but not part 2)
    return hits_x(vx, x_max, x_min) and hits_y(vy, y_min, y_max)


def test_part_1():
    target = parse_input("./data/example.txt")
    vx = get_min_vx(target[0], target[1])
    vy = get_max_vy(target[2], target[3])
    # plot_trajectory(vx, vy, *target)

    solution = get_max_height(vy)
    correct = 45
    assert correct == solution, f"{correct} != {solution}"


def part_1():
    target = parse_input("./data/input.txt")
    vx = get_min_vx(target[0], target[1])
    vy = get_max_vy(target[2], target[3])

    plot_trajectory(vx, vy, *target)

    solution = get_max_height(vy)
    print("Solution part 1:")
    print(solution)


def parse_part_2_solutions(path: str):
    solutions = []
    with open(path) as f:
        while line := f.readline():
            vx, vy = map(int, line.split(","))
            solutions.append((vx, vy))

    return sorted(solutions)


def brute_force_get_all_vs_joblib(target: Tuple[int, int, int, int]) -> int:
    def iter_vys(vx, min_vy, max_vy, target):
        local_solution = 0
        for vy in range(min_vy, max_vy + 1):
            arr, y_offset = calc_trajectory_target_array(vx, vy, *target)
            target_arr = arr[-target[3] + y_offset: -target[2] + y_offset + 1, target[0]: target[1] + 1]
            if np.any(target_arr == 3):
                local_solution += 1
        return local_solution

    min_vx = int(np.ceil(cumsum_inverse(target[0])))
    max_vx = cumsum(target[1])
    min_vy = target[2]
    max_vy = get_max_vy(target[2], target[3])
    result = joblib.Parallel(n_jobs=11)(joblib.delayed(iter_vys)(vx, min_vy, max_vy, target)
                                        for vx in range(min_vx, max_vx))
    return sum(result)


@nb.jit(nb.int64(nb.int64, nb.int64, nb.int64, nb.int64), nopython=True)
def brute_force_get_all_vs_numba(x_min: int, x_max: int, y_min: int, y_max: int) -> int:
    min_vx = int(np.ceil(cumsum_inverse(x_min)))
    max_vx = cumsum(x_max)
    min_vy = y_min
    max_vy = get_max_vy(y_min, y_max)

    total = 0
    for vx in nb.prange(min_vx, max_vx):
        inner_sum = 0
        for vy in nb.prange(min_vy, max_vy + 1):
            arr, y_offset = calc_trajectory_target_array(vx, vy, x_min, x_max, y_min, y_max)
            target_arr = arr[-y_max + y_offset: -y_min + y_offset + 1, x_min: x_max + 1]
            if np.any(target_arr == 3):
                inner_sum += 1

        total += inner_sum
    return total


def test_part_2():
    target = parse_input("./data/example.txt")
    solution = brute_force_get_all_vs_numba(*target)

    correct = 112
    assert correct == solution, f"{correct} != {solution}"


def part_2():
    target = parse_input("./data/input.txt")
    # Both brute force methods are extremely inefficient, but they work...
    solution = brute_force_get_all_vs_numba(*target)

    print("Solution part 2:")
    print(solution)


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
