from typing import List, Iterable, Tuple
import pyparsing
from pyparsing import ZeroOrMore, Forward, Literal, OneOrMore, Optional, ParserElement
from tqdm import tqdm


pyparsing.ParserElement.enablePackrat()


class BracketMismatchException(Exception):
    def __init__(self, s, loc, toks):
        self.open_bracket = toks[0]
        self.close_bracket = toks[-1]
        self.position = pyparsing.col(loc, s) + len(toks) - 1

        message = f"Opening bracket {self.open_bracket} does not match closing bracket {self.close_bracket} on column "\
                  f"{self.position}:\r\n" \
                  f"{s}\r\n" \
                  f"{' ' * (self.position - 1)}^ here"

        super().__init__(message)


class Part_One_Parser:
    match_bracket = {
        "[": "]",
        "(": ")",
        "{": "}",
        "<": ">",
    }

    def __init__(self):
        self.missing_brackets = []
        opener = self._xor_literals(self.match_bracket.keys())
        closer = self._xor_literals(self.match_bracket.values())

        closed_expr = Forward()
        opened_expr = Forward()

        closed_expr <<= (opener + ZeroOrMore(closed_expr) + closer).set_parse_action(self._check_match)
        opened_expr <<= (opener ^ opener + ZeroOrMore(closed_expr ^ opened_expr)).set_parse_action(
            lambda s, loc, toks: self._store_missing(s, loc, toks)
        )

        self.expr = opened_expr ^ (OneOrMore(closed_expr) + Optional(opened_expr))

    @staticmethod
    def _check_match(s, loc, toks):
        if toks[-1] != Part_One_Parser.match_bracket[toks[0]]:
            raise BracketMismatchException(s, loc, toks)

    def _store_missing(self, s, loc, toks):
        self.missing_brackets.append(self.match_bracket[toks[0]])

    @staticmethod
    def _xor_literals(iterable: Iterable[str]):
        iterator = iterable.__iter__()
        result = Literal(next(iterator))
        for i in iterator:
            result ^= Literal(i)
        return result

    def parse(self, string: str) -> ParserElement:
        return self.expr.parse_string(string, parse_all=True)

    def parse_get_missing(self, string: str) -> Tuple[ParserElement, List[str]]:
        self.missing_brackets = []
        return self.expr.parse_string(string, parse_all=True), self.missing_brackets


def get_parse_points(mismatch: BracketMismatchException) -> int:
    score_dict = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    return score_dict[mismatch.close_bracket]


def get_completion_points(missing: List[str]) -> int:
    score_dict = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    score = 0
    for m in missing:
        score = score * 5 + score_dict[m]
    return score


def get_parse_score(lines: List[str]):
    parser = Part_One_Parser()
    score = 0
    for line in tqdm(lines):
        try:
            parser.parse(line)
        except BracketMismatchException as e:
            score += get_parse_points(e)

    return score


def parse_input(path: str) -> List[str]:
    lines = []
    with open(path) as f:
        while line := f.readline():
            lines.append(line.strip())
    return lines


def test_part_1():
    lines = parse_input("./data/example.txt")
    solution = get_parse_score(lines)
    correct = 26397
    assert correct == solution, f"{correct} != {solution}"


def part_1():
    lines = parse_input("./data/input.txt")
    solution = get_parse_score(lines)

    print("Solution part 1:")
    print(solution)


def get_completion_score(lines: List[str]) -> int:
    parser = Part_One_Parser()
    scores = []
    for line in tqdm(lines):
        try:
            _, missing = parser.parse_get_missing(line)
            scores.append(get_completion_points(missing))
        except BracketMismatchException as e:
            continue

    scores = sorted(scores)
    return scores[len(scores) // 2]


def test_part_2():
    lines = parse_input("./data/example.txt")
    solution = get_completion_score(lines)
    correct = 288957
    assert correct == solution, f"{correct} != {solution}"


def part_2():
    lines = parse_input("./data/input.txt")
    solution = get_completion_score(lines)

    print("Solution part 2:")
    print(solution)


if __name__ == '__main__':
    test_part_1()
    part_1()
    print()
    test_part_2()
    part_2()
