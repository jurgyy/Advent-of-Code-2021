from typing import Tuple
import numpy as np


def bit_array_to_base_10(bits: np.ndarray) -> int:
    return sum([v << i for i, v in enumerate(bits[::-1])])


def power_consumption(path) -> Tuple[int, int, int]:
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
    return gamma, eps, gamma * eps


def test_part_1():
    gamma, epsilon, m = power_consumption("./data/example.txt")
    correct_g = 22
    correct_e = 9
    correct_m = correct_g * correct_e
    assert correct_g == gamma, f"{correct_g} != {gamma}"
    assert correct_e == epsilon, f"{correct_e} != {epsilon}"
    assert correct_m == m, f"{correct_m} != {m}"


def part_1():
    gamma, epsilon, m = power_consumption("./data/input.txt")
    print("Solution part 1:")
    print(f"Gamma: {gamma}")
    print(f"Epsilon: {epsilon}")
    print(f"Mult: {m}")


if __name__ == '__main__':
    test_part_1()
    part_1()
