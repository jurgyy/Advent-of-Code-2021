from unittest import TestCase

from pyparsing import ParseException

from day10.main import Part_One_Parser, BracketMismatchException


class TestPart_One_Parser(TestCase):
    parser = Part_One_Parser()

    def test_open_bracket(self):
        for b in "[{<(":
            parse_result, missing = self.parser.parse_get_missing(b)
            parse_result = parse_result.as_list()
            expected_parse = [b]
            expected_missing = [self.parser.match_bracket[b]]

            self.assertEqual(parse_result, expected_parse, f"{parse_result} != {expected_parse}")
            self.assertEqual(missing, expected_missing, f"{missing} != {expected_missing}")

    def test_open_close(self):
        for brackets in ["()", "{}", "<>", "[]"]:
            parse_result = self.parser.parse(brackets).as_list()
            expected = list(brackets)
            self.assertEqual(parse_result, expected, f"{parse_result} != {expected}")

    def test_nested_same(self):
        inp = "((()))"
        parse_result = self.parser.parse(inp).as_list()
        expected = list(inp)
        self.assertEqual(parse_result, expected, f"{parse_result} != {expected}")

    def test_nested_different(self):
        inp = "([{<()>}])"
        parse_result = self.parser.parse(inp).as_list()
        expected = list(inp)
        self.assertEqual(parse_result, expected, f"{parse_result} != {expected}")

    def test_nested_unfinished(self):
        inp = "([{<("
        parse_result, missing = self.parser.parse_get_missing(inp)
        parse_result = parse_result.as_list()

        expected_parse = list(inp)
        expected_missing = list(")>}])")
        self.assertEqual(parse_result, expected_parse, f"{parse_result} != {expected_parse}")
        self.assertEqual(missing, expected_missing, f"{missing} != {expected_missing}")

    def test_nested_half_unfinished(self):
        inp = "([{<()><"
        parse_result, missing = self.parser.parse_get_missing(inp)
        parse_result = parse_result.as_list()

        expected_parse = list(inp)
        expected_missing = list(">}])")
        self.assertEqual(parse_result, expected_parse, f"{parse_result} != {expected_parse}")
        self.assertEqual(missing, expected_missing, f"{missing} != {expected_missing}")

    def test_raises_no_open(self):
        inp = ")"
        with self.assertRaises(ParseException):
            self.parser.parse(inp)

    def test_raises_extra_close(self):
        inp = "())"
        with self.assertRaises(ParseException):
            self.parser.parse(inp)

    def test_bracket_mismatch_position(self):
        inp = "(]"
        try:
            self.parser.parse(inp)
        except BracketMismatchException as e:
            self.assertEqual(e.position, 2)

    def test_bracket_mismatch_nested_position(self):
        inp = "((()])"
        try:
            self.parser.parse(inp)
        except BracketMismatchException as e:
            self.assertEqual(e.position, 5)

    def test_multiple_bracket_mismatch_pick_first(self):
        inp = "({>{>)"
        try:
            self.parser.parse(inp)
        except BracketMismatchException as e:
            self.assertEqual(e.position, 3)
