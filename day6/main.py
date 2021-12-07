from typing import List


def parse_input(path: str) -> List[int]:
    with open(path) as f:
        line = f.readline()
        state = line.split(",")
        state = [int(s) for s in state]
    return state


def growth(initial_state: List[int], days: int, reset_timer=6, spawn_timer=8) -> int:
    state_count = {k: 0 for k in range(max(reset_timer, spawn_timer) + 1)}
    for s in initial_state:
        state_count[s] += 1

    for _ in range(days):
        new_state_count = {k: 0 for k in range(max(reset_timer, spawn_timer) + 1)}
        for days, count in state_count.items():
            if days == 0:
                new_state_count[reset_timer] += count
                new_state_count[spawn_timer] += count
            else:
                new_state_count[days - 1] += count
        state_count = new_state_count

    return sum(state_count.values())


def test_part_1():
    solution = growth(parse_input("./data/example.txt"), 80)
    correct = 5934
    assert correct == solution, f"{solution} != {correct}"


def part_1():
    solution = growth(parse_input("./data/input.txt"), 80)
    print("Solution part 1:")
    print(solution)


def test_part_2():
    solution = growth(parse_input("./data/example.txt"), 256)
    correct = 26984457539
    assert correct == solution, f"{correct} != {solution}"


def part_2():
    solution = growth(parse_input("./data/input.txt"), 256)
    print("Solution part 2:")
    print(solution)


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
