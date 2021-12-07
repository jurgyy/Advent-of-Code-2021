def calc_n_larger(path: str) -> int:
    n_larger = 0

    with open(path) as f:
        prev = int(f.readline())

        while val := f.readline():
            val = int(val)
            if prev < val:
                n_larger += 1
            prev = val

    return n_larger


def calc_n_larger_sliding(path: str, size: int) -> int:
    n_larger = 0

    with open(path) as f:
        window = []
        for _ in range(size):
            window.append(int(f.readline()))

        prev = sum(window)

        while line := f.readline():
            line = int(line)
            window.pop(0)
            window.append(line)

            val = sum(window)
            if prev < val:
                n_larger += 1

            prev = val

    return n_larger


def test_part_1():
    n = calc_n_larger("./data/example.txt")
    correct = 7
    assert correct == n, f"{correct} != {n}"


def part_1():
    print("Solution part 1:")
    print(calc_n_larger("./data/input.txt"))


def test_part_2():
    n = calc_n_larger_sliding("./data/example.txt", size=3)
    correct = 5
    assert correct == n, f"{correct} != {n}"


def part_2():
    print("Solutin part 2:")
    print(calc_n_larger_sliding("./data/input.txt", size=3))


if __name__ == '__main__':
    test_part_1()
    part_1()

    test_part_2()
    part_2()
