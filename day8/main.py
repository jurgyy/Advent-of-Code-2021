from typing import List, Tuple, Iterable
from collections import Counter
from constraint import Problem, InSetConstraint
import itertools as it


#  dddd
# e    a
# e    a
#  ffff
# g    b
# g    b
#  cccc

len_map = {
    2: 1,
    3: 7,
    4: 4,
    7: 8
}


def parse_input(path: str) -> List[Tuple[List[str], List[str]]]:
    lines = []
    with open(path) as f:
        while line := f.readline():
            inp, outp = line.split("|")
            inp = inp.strip().split()
            outp = outp.strip().split()
            lines.append((inp, outp))

    return lines


def decode_word(word: str):
    if len(word) in len_map:
        return len_map[len(word)]
    return word


def count_decoded_output(lines):
    counter = Counter()
    for inp, outp in lines:
        for word in outp:
            counter[decode_word(word)] += 1
    return counter


def test_part_1():
    lines = parse_input("./data/example.txt")
    counter = count_decoded_output(lines)

    solution = counter[1] + counter[4] + counter[7] + counter[8]
    correct = 26
    assert correct == solution, f"{correct} != {solution}"


def part_1():
    lines = parse_input("./data/input.txt")
    counter = count_decoded_output(lines)

    solution = counter[1] + counter[4] + counter[7] + counter[8]
    print("Solution part 1:")
    print(solution)


def initialize_constraint_problem() -> Problem:
    def intersection_is_length(a: Iterable, b: Iterable, length: int) -> bool:
        return len(set(a).intersection(set(b))) == length

    problem = Problem()

    # Add per digit all possible permutations of segments
    letters = "abcdefg"
    problem.addVariable(0, list(map("".join, it.permutations(letters, r=6))))
    problem.addVariable(1, list(map("".join, it.permutations(letters, r=2))))
    problem.addVariable(2, list(map("".join, it.permutations(letters, r=5))))
    problem.addVariable(3, list(map("".join, it.permutations(letters, r=5))))
    problem.addVariable(4, list(map("".join, it.permutations(letters, r=4))))
    problem.addVariable(5, list(map("".join, it.permutations(letters, r=5))))
    problem.addVariable(6, list(map("".join, it.permutations(letters, r=6))))
    problem.addVariable(7, list(map("".join, it.permutations(letters, r=3))))
    problem.addVariable(8, list(map("".join, it.permutations(letters, r=7))))
    problem.addVariable(9, list(map("".join, it.permutations(letters, r=6))))

    # Per digit add constraint for the number of overlapping segments with all other digits
    # 0
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 2), [0, 1])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 4), [0, 2])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 4), [0, 3])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 3), [0, 4])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 4), [0, 5])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 5), [0, 6])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 3), [0, 7])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 6), [0, 8])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 5), [0, 9])

    # 1
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 1), [1, 2])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 2), [1, 3])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 2), [1, 4])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 1), [1, 5])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 1), [1, 6])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 2), [1, 7])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 2), [1, 8])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 2), [1, 9])

    # 2
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 4), [2, 3])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 2), [2, 4])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 3), [2, 5])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 4), [2, 6])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 2), [2, 7])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 5), [2, 8])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 4), [2, 9])

    # 3
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 3), [3, 4])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 4), [3, 5])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 4), [3, 6])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 3), [3, 7])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 5), [3, 8])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 5), [3, 9])

    # 4
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 3), [4, 5])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 3), [4, 6])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 2), [4, 7])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 4), [4, 8])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 4), [4, 9])

    # 5
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 5), [5, 6])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 2), [5, 7])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 5), [5, 8])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 5), [5, 9])

    # 6
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 2), [6, 7])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 6), [6, 8])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 5), [6, 9])

    # 7
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 3), [7, 8])
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 3), [7, 9])

    # 8
    problem.addConstraint(lambda a, b: intersection_is_length(a, b, 6), [8, 9])

    return problem


def add_problem_data_constraint(problem: Problem, data: List[str]):
    problem.addConstraint(InSetConstraint(set(data)))


def decode_problem(problem: Problem, encoded: List[str]) -> int:
    decode_dict = {}
    for s in problem.getSolutions():
        for k, v in s.items():
            decode_dict["".join(sorted(v))] = k

    digits = []
    for w in encoded:
        digits.append(decode_dict["".join(sorted(w))])

    # [a, b, c, d] -> sum([d + 10c + 100b + 1000a]) == abcd
    return sum([d * 10**i for i, d in enumerate(digits[::-1])])


def test_part_2():
    lines = parse_input("./data/example.txt")
    solution = []
    for line in lines:
        inp, outp = line
        problem = initialize_constraint_problem()
        add_problem_data_constraint(problem, inp)
        d = decode_problem(problem, outp)
        solution.append(d)

    correct = [8394, 9781, 1197, 9361, 4873, 8418, 4548, 1625, 8717, 4315]
    assert correct == solution, f"{correct} != {solution}"


def part_2():
    lines = parse_input("./data/input.txt")
    solution = []
    for line in lines:
        inp, outp = line
        problem = initialize_constraint_problem()
        add_problem_data_constraint(problem, inp)
        d = decode_problem(problem, outp)
        solution.append(d)

    print("Solution part 2:")
    print(sum(solution))


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
