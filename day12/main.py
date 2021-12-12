from typing import Dict, Set


class Cave:
    def __init__(self, name: str):
        self.name = name
        self.is_large = name.isupper()
        self.neighbours: Set["Cave"] = set()
        self.is_start = name == "start"
        self.is_end = name == "end"

    def __repr__(self):
        return f"{self.name}: {[c.name for c in self.neighbours]}"

    def __hash__(self):
        return hash(self.name)


def parse_input(path: str) -> Dict[str, Cave]:
    caves: Dict[str, Cave] = {}

    with open(path) as f:
        while line := f.readline():
            l, r = line.strip().split("-")
            for name in (l, r):
                if name not in caves:
                    caves[name] = Cave(name)

            caves[l].neighbours.add(caves[r])
            caves[r].neighbours.add(caves[l])

    return caves


def count_all_paths(caves: Dict[str, Cave], small_cave_visits: int = 0):
    def depth_first_search_count(current: Cave, destination: Cave, visited: Dict[Cave, bool],
                                 remaining_small_visists: int, is_extra_visit: bool = False):
        visited[current] = True
        if current == destination:
            n_paths = 1
        else:
            n_paths = 0
            for i in current.neighbours:
                if not i.is_large and visited[i] and remaining_small_visists > 0 and not (i.is_start or i.is_end):
                    # Extra small cave visit
                    n_paths += depth_first_search_count(i, destination, visited, remaining_small_visists - 1, True)
                elif i.is_large or not visited[i]:
                    n_paths += depth_first_search_count(i, destination, visited, remaining_small_visists)

        # TODO will not work for small_cave_visits > 1
        if not is_extra_visit:
            visited[current] = False
        
        return n_paths

    return depth_first_search_count(caves["start"], caves["end"], {c: False for c in caves.values()}, small_cave_visits)


def test_part_1():
    solution_small = count_all_paths(parse_input("./data/example_small.txt"))
    correct_small = 10
    assert correct_small == solution_small, f"{correct_small} != {solution_small}"

    solution_medium = count_all_paths(parse_input("./data/example_medium.txt"))
    correct_medium = 19
    assert correct_medium == solution_medium, f"{correct_medium} != {solution_medium}"

    solution_large = count_all_paths(parse_input("./data/example_large.txt"))
    correct_large = 226
    assert correct_large == solution_large, f"{correct_large} != {solution_large}"


def part_1():
    solution = count_all_paths(parse_input("./data/input.txt"))
    print("Solution part 1:")
    print(solution)


def test_part_2():
    solution_small = count_all_paths(parse_input("./data/example_small.txt"), 1)
    correct_small = 36
    assert correct_small == solution_small, f"{correct_small} != {solution_small}"
    
    solution_medium = count_all_paths(parse_input("./data/example_medium.txt"), 1)
    correct_medium = 103
    assert correct_medium == solution_medium, f"{correct_medium} != {solution_medium}"

    solution_large = count_all_paths(parse_input("./data/example_large.txt"), 1)
    correct_large = 3509
    assert correct_large == solution_large, f"{correct_large} != {solution_large}"


def part_2():
    solution = count_all_paths(parse_input("./data/input.txt"), 1)
    print("Solution part 2:")
    print(solution)


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
