from typing import Tuple
import numpy as np


def bit_array_to_base_10(bits: np.ndarray) -> int:
    return sum([v << i for i, v in enumerate(bits[::-1])])


def power_consumption(path) -> Tuple[int, int]:
    lines = 0
    arr_sum = None
    with open(path) as f:
        while line := f.readline().strip():
            lines += 1
            arr = np.array(list(line), dtype=int)

            if arr_sum is None:
                arr_sum = arr
            else:
                arr_sum += arr

    bits = arr_sum > lines / 2
    gamma = bit_array_to_base_10(bits)
    eps = bit_array_to_base_10(np.invert(bits))
    return gamma, eps


def test_part_1():
    gamma, epsilon = power_consumption("./data/example.txt")
    correct_g = 22
    correct_e = 9
    assert correct_g == gamma, f"{correct_g} != {gamma}"
    assert correct_e == epsilon, f"{correct_e} != {epsilon}"


def part_1():
    gamma, epsilon = power_consumption("./data/input.txt")
    print("Solution part 1:")
    print(f"Gamma: {gamma}")
    print(f"Epsilon: {epsilon}")
    print(f"Mult: {gamma * epsilon}")


def do_masking(matrix: np.ndarray, oxygen=True) -> int:
    # I'm certain a specific set of bitwise operations can also work
    n_lines, n_bits = matrix.shape

    mask = np.ones(n_lines, dtype=bool)
    masked = matrix

    for i in range(n_bits):
        if oxygen:
            most_common = np.sum(masked[:, i]) >= len(masked) / 2
        else:
            most_common = np.sum(masked[:, i]) < len(masked) / 2

        mask = mask & (matrix[:, i] == most_common)
        masked = matrix[mask]

        if len(masked) == 1:
            return bit_array_to_base_10(masked[0])
        if len(masked) == 0:
            raise Exception("No lines remaining")


def calc_co2_oxy(path: str) -> Tuple[int, int]:
    lines = []

    with open(path) as f:
        while line := f.readline().strip():
            lines.append([int(v) for v in line])

    matrix = np.array(lines)
    return do_masking(matrix, oxygen=False), do_masking(matrix, oxygen=True)


def test_part_2():
    co2, ox = calc_co2_oxy("./data/example.txt")
    correct_ox = 23
    assert correct_ox == ox, f"{correct_ox} != {ox}"


def part_2():
    co2, ox = calc_co2_oxy("./data/input.txt")
    print("Solution part 2:")
    print(f"CO2: {co2}")
    print(f"Oxygen: {ox}")
    print(f"Mult: {co2 * ox}")


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
