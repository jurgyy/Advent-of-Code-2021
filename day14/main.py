from collections import Counter
from typing import Tuple, Dict


def parse_input(path: str) -> Tuple[str, Dict[str, str]]:

    insertion_rules = {}
    with open(path) as f:
        polymer_template = f.readline().strip()
        f.readline()

        while line := f.readline():
            k, v = line.strip().split(" -> ")
            insertion_rules[k] = v

    return polymer_template, insertion_rules


def do_step(polymer: str, insertion_rules: Dict[str, str]) -> str:
    prev = polymer[0]
    new_polymer = ""
    for char in polymer[1:]:
        new_polymer += prev + insertion_rules[prev + char]
        prev = char
    new_polymer += polymer[-1]

    return new_polymer


def test_part_1():
    # Using a naive approach
    pol, rules = parse_input("./data/example.txt")
    for _ in range(10):
        pol = do_step(pol, rules)

    mc = Counter(pol).most_common()
    most_char, most_val = mc[0]
    least_char, least_val = mc[-1]

    solution = most_val - least_val
    correct = 1588
    assert correct == solution, f"{correct} != {solution}"


def part_1():
    pol, rules = parse_input("./data/input.txt")
    for _ in range(10):
        pol = do_step(pol, rules)

    mc = Counter(pol).most_common()
    most_char, most_val = mc[0]
    least_char, least_val = mc[-1]

    solution = most_val - least_val
    print("Solution part 1:")
    print(solution)


def recursive_with_cache(pol: str, rules: Dict[str, str], n_iterations: int) -> Counter:
    cache: Dict[Tuple[str, str, int], Counter] = {}

    def recur(a: str, c: str, iteration: int) -> Counter:
        if (a, c, iteration) in cache:
            return cache[(a, c, iteration)]

        b = rules[a + c]
        if iteration < n_iterations:
            counter = Counter(recur(a, b, iteration + 1)) + Counter(recur(b, c, iteration + 1))
            cache[(a, c, iteration)] = counter
            return counter
        else:
            return Counter(a)

    result = Counter()
    for i in range(len(pol) - 1):
        result += recur(pol[i], pol[i + 1], 0)
    result += Counter(pol[-1])

    return result


def test_part_2():
    # Using an optimized approach
    pol, rules = parse_input("./data/example.txt")

    counter = recursive_with_cache(pol, rules, 40)
    mc = counter.most_common()
    most_char, most_val = mc[0]
    least_char, least_val = mc[-1]

    solution = most_val - least_val
    correct = 2188189693529
    assert correct == solution, f"{correct} != {solution}"


def part_2():
    pol, rules = parse_input("./data/input.txt")

    c = recursive_with_cache(pol, rules, 40)

    mc = c.most_common()
    most_char, most_val = mc[0]
    least_char, least_val = mc[-1]

    solution = most_val - least_val
    print("Solution part 2:")
    print(solution)


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
