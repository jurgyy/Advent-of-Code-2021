from typing import List

import numpy as np


def parse_input(path: str) -> List[int]:
    with open(path) as f:
        return [int(v) for v in f.readline().split(",")]


def calc_cost(source: int, target: int) -> int:
    return abs(source - target)


def cheapest_position_cost(positions: List[int]) -> int:
    positions = sorted(positions)

    mean = positions[len(positions) // 2]
    cost = sum([calc_cost(p, mean) for p in positions])

    return cost


def cheapest_position_cost_exp(positions: List[int]) -> int:
    all_costs = []
    max_v = max(positions)

    # (i + i^2) / 2 where i is the number of steps
    costs = [int((i + i**2) / 2) for i in range(max_v + 1)]

    for p in positions:
        # We stitch the reverse(costs)[-p : 0] with costs[1 : n - p]
        # such that we get the cost from point p to every other point
        all_costs.append(costs[::-1][-p - 1:] + costs[1:len(costs) - p])

    arr = np.array(all_costs)
    return np.min(np.sum(arr, axis=0))


def test_part_1():
    solution = cheapest_position_cost(parse_input("./data/example.txt"))
    correct = 37
    assert correct == solution, f"{correct} != {solution}"


def part_1():
    solution = cheapest_position_cost(parse_input("./data/input.txt"))
    print("Solution part 1:")
    print(solution)


def test_part_2():
    solution = cheapest_position_cost_exp(parse_input("./data/example.txt"))
    correct = 168
    assert correct == solution, f"{correct} != {solution}"


def part_2():
    solution = cheapest_position_cost_exp(parse_input("./data/input.txt"))
    print("Solution part 2:")
    print(solution)


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
