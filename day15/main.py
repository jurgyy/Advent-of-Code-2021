from typing import Tuple

import numpy as np
import numba as nb


def parse_input(path: str) -> np.ndarray:
    data = []
    with open(path) as f:
        while line := f.readline():
            data.append(list(map(int, list(line.strip()))))

    return np.array(data)


@nb.jit(nb.int32[:, :](nb.int32[:, :], nb.int32, nb.int32), nopython=True)
def get_neighbours(data: np.ndarray, row: int, column: int) -> np.ndarray:
    neighbours = []

    if row > 0:
        neighbours.append([row - 1, column])
    if row < data.shape[0] - 1:
        neighbours.append([row + 1, column])
    if column > 0:
        neighbours.append([row, column - 1])
    if column < data.shape[1] - 1:
        neighbours.append([row, column + 1])

    return np.array(neighbours, dtype=np.int32)


@nb.jit(nb.int64[:, :](nb.int32[:, :], nb.types.UniTuple(nb.int64, 2)), nopython=True)
def dijkstra(data: np.ndarray, source: Tuple[int, int]) -> Tuple[np.ndarray, np.ndarray]:
    def argmin(iterable):
        mn = 9999999999
        mn_ind = None
        for idx, val in iterable.items():
            if val < mn:
                mn = val
                mn_ind = idx
        return mn_ind

    max_d = np.sum(data)
    distances = np.ones(data.shape, dtype=np.int32) * max_d

    distances[source[0], source[1]] = 0

    prio_queue = dict()

    # noinspection PyTypeChecker
    for y, x in np.ndindex(data.shape):
        prio_queue[(y, x)] = distances[y, x]

    while prio_queue:
        Uy, Ux = argmin(prio_queue)
        U = prio_queue.pop((Uy, Ux))
        for ny, nx in get_neighbours(data, Uy, Ux):
            temp_distance = distances[Uy, Ux] + data[ny, nx]
            if temp_distance < distances[ny, nx]:
                distances[ny, nx] = temp_distance
                prio_queue[(ny, nx)] = temp_distance

    return distances


def test_part_1():
    data = parse_input("./data/example.txt")
    d = dijkstra(data, (0, 0))

    solution = d[data.shape[0] - 1, data.shape[1] - 1]
    correct = 40
    assert correct == solution, f"{correct} != {solution}"


def part_1():
    data = parse_input("./data/input.txt")
    d = dijkstra(data, (0, 0))

    solution = d[data.shape[0] - 1, data.shape[1] - 1]
    print("Solution part 1:")
    print(solution)


def test_part_2():
    data = parse_input("./data/example.txt")
    tiled_data = np.copy(data)
    for i in range(4):
        tiled_data = np.concatenate((tiled_data, (data + i) % 9 + 1), axis=0)

    data = np.copy(tiled_data)
    for i in range(4):
        tiled_data = np.concatenate((tiled_data, (data + i) % 9 + 1), axis=1)

    d = dijkstra(tiled_data, (0, 0))

    solution = d[tiled_data.shape[0] - 1, tiled_data.shape[1] - 1]
    correct = 315
    assert correct == solution, f"{correct} != {solution}"


def part_2():
    data = parse_input("./data/input.txt")
    tiled_data = np.copy(data)
    for i in range(4):
        tiled_data = np.concatenate((tiled_data, (data + i) % 9 + 1), axis=0)

    data = np.copy(tiled_data)
    for i in range(4):
        tiled_data = np.concatenate((tiled_data, (data + i) % 9 + 1), axis=1)

    d = dijkstra(tiled_data, (0, 0))

    solution = d[tiled_data.shape[0] - 1, tiled_data.shape[1] - 1]
    print("Solution part 2:")
    print(solution)


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
