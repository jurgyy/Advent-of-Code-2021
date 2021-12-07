from typing import List, Tuple
import numpy as np


def parse_input(path: str, board_size=5) -> Tuple[List[int], List[np.ndarray]]:
    boards = []
    with open(path) as f:
        draws = f.readline().split(sep=",")
        draws = [int(d) for d in draws]
        while f.readline():
            board = []
            for _ in range(board_size):
                board.append(list(map(int, f.readline().strip().split())))
            boards.append(np.array(board))

    return draws, boards


def calc_board_score(board: np.ndarray, mask: np.ndarray, last_draw: int) -> int:
    s = np.sum(board[~mask])
    return s * last_draw


def has_won(board, mask):
    if np.any(np.sum(mask, axis=0) == board.shape[0]):
        return True
    if np.any(np.sum(mask, axis=1) == board.shape[1]):
        return True
    return False


def get_empty_masks(shape: Tuple, n: int) -> List[np.ndarray]:
    return [np.zeros(shape, dtype=bool) for _ in range(n)]


def bingo(draws: List[int], boards: List[np.ndarray]) -> int:
    masks = get_empty_masks(boards[0].shape, len(boards))

    for d in draws:
        for board, mask in zip(boards, masks):
            mask[board == d] = True

            if has_won(board, mask):
                return calc_board_score(board, mask, d)
    raise Exception("No winner")


def bingo_lose(draws: List[int], boards: List[np.ndarray]) -> int:
    masks = get_empty_masks(boards[0].shape, len(boards))

    for d in draws:
        pops = []
        for i, (board, mask) in enumerate(zip(boards, masks)):
            mask[board == d] = True
            if has_won(board, mask):
                pops.append(i)

        for i, pop in enumerate(pops):
            if len(boards) == 1:
                return calc_board_score(boards[0], masks[0], d)
            boards.pop(pop - i)
            masks.pop(pop - i)

    raise Exception("No loser")


def test_part_1():
    draws, boards = parse_input("./data/example.txt")
    score = bingo(draws, boards)
    correct_score = 4512
    assert correct_score == score, f"{correct_score} != {score}"


def part_1():
    draws, boards = parse_input("./data/input.txt")
    score = bingo(draws, boards)
    print("Solution part 1:")
    print(f"Board score: {score}")


def test_part_2():
    draws, boards = parse_input("./data/example.txt")
    score = bingo_lose(draws, boards)
    correct_score = 1924
    assert correct_score == score, f"{correct_score} != {score}"


def part_2():
    draws, boards = parse_input("./data/input.txt")
    score = bingo_lose(draws, boards)
    print("Solution part 2:")
    print(f"Board score: {score}")


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
