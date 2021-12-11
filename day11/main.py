from typing import List, Union


class Octopus:
    def __init__(self, starting_energy: Union[int, str]):
        self.energy = int(starting_energy)
        self._neighbours: List[Octopus] = []

    def add_neighbour(self, neighbour: "Octopus"):
        self._neighbours.append(neighbour)

    def increment_energy(self):
        self.energy += 1
        if self.energy == 10:
            for neighbour in self._neighbours:
                neighbour.increment_energy()

    def resolve_energy(self, cave: "Cave"):
        if self.energy > 9:
            cave.flashes += 1
            self.energy = 0

    def __repr__(self):
        return f"O({self.energy}) with {len(self._neighbours)} neighbours"


class Cave:
    def __init__(self, grid: List[List[int]]):
        self._octopusses: List[List[Octopus]] = []
        self.n_octopuses = 0
        self.flashes = 0
        self.step = 0

        for row in grid:
            self._octopusses.append([])
            for val in row:
                self._octopusses[-1].append(Octopus(val))
                self.n_octopuses += 1

        for y, row in enumerate(self._octopusses):
            for x, octopus in enumerate(row):
                neighbours = []
                t = y > 0
                l = x > 0
                r = x < len(row) - 1
                b = y < len(grid) - 1
                if t:
                    neighbours.append(self._octopusses[y - 1][x])
                    if l:
                        neighbours.append(self._octopusses[y - 1][x - 1])
                    if r:
                        neighbours.append(self._octopusses[y - 1][x + 1])
    
                if l:
                    neighbours.append(self._octopusses[y][x - 1])
                if r:
                    neighbours.append(self._octopusses[y][x + 1])
    
                if b:
                    neighbours.append(self._octopusses[y + 1][x])
                    if l:
                        neighbours.append(self._octopusses[y + 1][x - 1])
                    if r:
                        neighbours.append(self._octopusses[y + 1][x + 1])
    
                for neighbour in neighbours:
                    octopus.add_neighbour(neighbour)

    def __iter__(self):
        for row in self._octopusses:
            for octopus in row:
                yield octopus

    def print_energy(self):
        for row in self._octopusses:
            print("".join([str(o.energy) for o in row]))

    def update(self) -> int:
        self.step += 1
        starting_flashes = self.flashes
        for row in self._octopusses:
            for o in row:
                o.increment_energy()

        for row in self._octopusses:
            for o in row:
                o.resolve_energy(self)

        return self.flashes - starting_flashes


def parse_input(path: str) -> Cave:
    lines = []
    with open(path) as f:
        while line := f.readline():
            lines.append(list(map(int, list(line.strip()))))

    return Cave(lines)


def test_part_1():
    cave = parse_input("./data/example.txt")
    for _ in range(10):
        cave.update()

    solution = cave.flashes
    correct = 204
    assert correct == solution, f"{correct} != {solution}"

    for _ in range(90):
        cave.update()

    solution = cave.flashes
    correct = 1656
    assert correct == solution, f"{correct} != {solution}"


def part_1():
    cave = parse_input("./data/input.txt")
    for _ in range(100):
        cave.update()

    print("Solution part 1:")
    print(cave.flashes)


def test_part_2():
    cave = parse_input("./data/example.txt")

    while cave.update() != cave.n_octopuses:
        cave.update()

    solution = cave.step
    correct = 195
    assert correct == solution, f"{correct} != {solution}"


def part_2():
    cave = parse_input("./data/input.txt")

    while cave.update() != cave.n_octopuses:
        cave.update()

    print("Solution part 2:")
    print(cave.step)


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
