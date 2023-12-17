import itertools  # combinations
import typing
import unittest
from copy import copy

from moszir_utils.position import Position
from moszir_utils.math import min_max


class Solution:
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            self.map = [line.strip() for line in test_input.readlines()]
            self.height = len(self.map)
            self.width = len(self.map[0])
            assert all((len(line) == self.width for line in self.map))

            self.empty_lines: typing.List[int] = [
                row_idx
                for row_idx, row in enumerate(self.map)
                if '#' not in row]
            self.empty_columns: typing.List[int] = [
                col_idx
                for col_idx, column in enumerate(zip(*self.map))
                if '#' not in column]
            self.galaxies: typing.List[Position] = [
                Position(row=row_idx, column=col_idx)
                for row_idx, row in enumerate(self.map)
                for col_idx, spot in enumerate(row)
                if spot == '#'
            ]

    def galaxy_distance(self, galaxy_1: Position, galaxy_2: Position, empty_line_value: int = 1) -> int:
        sr, lr = min_max(galaxy_1.r, galaxy_2.r)  # smaller row index, larger row index
        sc, lc = min_max(galaxy_1.c, galaxy_2.c)  # smaller column index, larger column index
        rd = lr - sr + (empty_line_value - 1) * sum((1 for row in self.empty_lines if sr < row < lr))
        cd = lc - sc + (empty_line_value - 1) * sum((1 for col in self.empty_columns if sc < col < lc))
        return rd + cd

    def solve(self, empty_line_value: int = 1) -> int:
        return sum((
            self.galaxy_distance(*pair, empty_line_value=empty_line_value)
            for pair in itertools.combinations(self.galaxies, r=2)
        ))

    def solve_a(self) -> int:
        return self.solve(empty_line_value=2)

    def solve_b(self) -> int:
        return self.solve(empty_line_value=1_000_000)


class Solution2:
    """ Solution with faster run time.

    Rather than counting the number of expanding rows/columns for each pair of galaxies,
    it first calculates the expanded positions by iterating over the expanding rows/columns.
    """
    def __init__(self, file_name: str):
        with open(file_name) as test_input:
            self.map = [line.strip() for line in test_input.readlines()]
            self.galaxies: typing.List[Position] = [
                Position(row=row_idx, column=column_idx)
                for row_idx, row in enumerate(self.map)
                for column_idx, c in enumerate(row)
                if c == '#'
            ]

    def expand_universe(self, factor: int) -> typing.Iterable[Position]:
        expansion = {g: copy(g) for g in self.galaxies}  # original position |-> expanded position
        for row_index, row in enumerate(self.map):
            if '#' not in row:
                for op, ep in expansion.items():
                    if row_index < op.r:
                        ep.r += factor - 1

        for column_index, column in enumerate(zip(*self.map)):
            if '#' not in column:
                for op, ep in expansion.items():
                    if column_index < op.c:
                        ep.c += factor - 1
        return expansion.values()

    def solve(self, factor: int = 1) -> int:
        return sum((
            Position.manhattan_distance(*pair)
            for pair in itertools.combinations(self.expand_universe(factor=factor), r=2)
        ))

    def solve_a(self) -> int:
        return self.solve(factor=2)

    def solve_b(self) -> int:
        return self.solve(factor=1_000_000)


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(374, Solution('example.txt').solve_a())

    def test_a_example_2(self):
        self.assertEqual(374, Solution2('example.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(10494813, Solution('input.txt').solve_a())

    def test_a_input_2(self):
        self.assertEqual(10494813, Solution2('input.txt').solve_a())

    def test_b_example(self):
        self.assertEqual(82000210, Solution('example.txt').solve_b())

    def test_b_example_2(self):
        self.assertEqual(82000210, Solution2('example.txt').solve_b())

    def test_b_input(self):
        self.assertEqual(840988812853, Solution('input.txt').solve_b())

    def test_b_input_2(self):
        self.assertEqual(840988812853, Solution2('input.txt').solve_b())


if __name__ == '__main__':
    unittest.main()
