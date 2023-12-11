import itertools  # combinations
import typing
import unittest

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
                for row_idx in range(len(self.map))
                if '#' not in self.map[row_idx]]
            self.empty_columns: typing.List[int] = [
                col_idx
                for col_idx in range(len(self.map[0]))
                if all((line[col_idx] == '.' for line in self.map))]
            self.galaxies: typing.List[Position] = [
                Position(row=row_idx, column=col_idx)
                for row_idx in range(self.height)
                for col_idx in range(self.width)
                if self.map[row_idx][col_idx] == '#'
            ]

    def galaxy_distance(self, galaxy_1: Position, galaxy_2: Position, empty_line_value: int = 1) -> int:
        sr, lr = min_max(galaxy_1.row, galaxy_2.row)  # smaller row index, larger row index
        sc, lc = min_max(galaxy_1.column, galaxy_2.column)  # smaller column index, larger column index
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


class Tests(unittest.TestCase):
    def test_a_example(self):
        self.assertEqual(374, Solution('example.txt').solve_a())

    def test_a_input(self):
        self.assertEqual(10494813, Solution('input.txt').solve_a())

    def test_b_example(self):
        self.assertEqual(82000210, Solution('example.txt').solve_b())

    def test_b_input(self):
        self.assertEqual(840988812853, Solution('input.txt').solve_b())


if __name__ == '__main__':
    unittest.main()
