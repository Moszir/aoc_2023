import pathlib
import typing
import unittest

from moszir_utils.position import Position as P
from moszir_utils.string_table import StringTable


class Beam(typing.NamedTuple):
    p: P
    d: P  # direction, i.e. (-1, 0), (1, 0), (0, -1), (0, 1)

    def step(self) -> 'Beam':
        return Beam(self.p + self.d, self.d)

    def hit_backslash(self) -> 'Beam':
        return Beam(self.p, P(self.d.c, self.d.r))

    def hit_slash(self) -> 'Beam':
        return Beam(self.p, P(-self.d.c, -self.d.r))

    def process(self, spot: str) -> typing.List['Beam']:
        return (
            [self.hit_backslash().step()] if spot == '\\' else
            [self.hit_slash().step()] if spot == '/' else
            [self.hit_slash().step(), self.hit_backslash().step()] if (
                (spot == '|' and self.d.c != 0) or (spot == '-' and self.d.r != 0)) else
            [self.step()])


class Solution:
    def __init__(self, path: pathlib.Path):
        self.table = StringTable(path.read_text().splitlines())

    def count_energized_beams(self, starting_beam: Beam) -> int:
        energized = set()
        beams = [starting_beam]
        seen = set()
        while beams:
            beam = beams.pop()
            if beam in seen or not self.table.valid_index(beam.p):
                continue
            seen.add(beam)
            energized.add(beam.p)
            beams.extend(beam.process(self.table[beam.p]))
        return len(energized)

    def solve_a(self) -> int:
        return self.count_energized_beams(Beam(P(0, 0), P(0, 1)))

    def solve_b(self) -> int:
        return max((
            self.count_energized_beams(beam)
            for beam in (
                *(Beam(p, P(1, 0)) for p in self.table.top()),
                *(Beam(p, P(-1, 0)) for p in self.table.bottom()),
                *(Beam(p, P(0, 1)) for p in self.table.left()),
                *(Beam(p, P(0, -1)) for p in self.table.right())
            )))


class Tests(unittest.TestCase):
    @staticmethod
    def example():
        return Solution(pathlib.Path('example.txt'))

    @staticmethod
    def real_input():
        return Solution(pathlib.Path('input.txt'))

    def test_a_example(self):
        self.assertEqual(46, self.example().solve_a())

    def test_a_input(self):
        self.assertEqual(6_921, self.real_input().solve_a())

    def test_b_example(self):
        self.assertEqual(51, self.example().solve_b())

    def test_b_input(self):
        self.assertEqual(7_594, self.real_input().solve_b())  # 2.6s, good enough


if __name__ == '__main__':
    unittest.main()
